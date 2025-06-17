import streamlit as st
import requests
import os
import shutil
import time
import random
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image

from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from googleapiclient.discovery import build
from PIL import Image
import requests
from io import BytesIO
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
# -------------------- 1. 環境變數 --------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY","")


# -------------------- 2. Prompt --------------------
text_template = """
作為一位專業的電子菸交易網站分類器，
你具備辨識下列 HTML 內容並將其分類的能力：

請依據以下兩類進行分類：

(1) 電子菸銷售網站

(2) 非此類網站

由於產品名稱、品牌或提及方式無窮無盡，請勿依賴特定關鍵字，
而應根據通用指標判斷，特別注意以下幾點：

1）使用情境或宣稱內容
留意明示或暗示具精神活性、致幻效果、或非法用途的描述。

若產品標榜改變情緒、帶來快感、強力舒壓等非一般性用途，可能暗示其具管制屬性。

2）交易性線索
提及價格、像是「私訊我」、「祕密配方」、「加 LINE 詳談」、「隱密出貨」等措辭，
可能與非法或受限產品有關。

若網站提供：

加入購物車

快速下單

產品型錄瀏覽

→ 即便表面合法，也應提高警覺，可能屬於非法販售網站。

3）法律分類或警示訊息
檢查是否有限制販售、年齡驗證、僅限持證人購買、或地區性銷售限制等。

對於模糊不清或自相矛盾的聲明也要保持警惕。

4）產品或服務類型
若產品為已知管制藥品或處方藥品（如：佐沛眠、地西泮、芬太尼、K他命、贊安諾、曲馬多等），
且搭配以下功能：

加入購物車

快速購買

SKU 或型號顯示

查詢價格

提供購買說明

→ 無論該網站看起來多麼專業、科學或醫療，均應判定為 (1)

⚠️ 注意：專業外觀與科學用語無法掩蓋其銷售管制物質的事實。

電子菸裝置與煙油（e-liquid）同樣屬於 (1)。

若產品為非管制補品、中藥材、或無害草本產品，則可歸為 (2)。

5）關鍵思考
不要只看外觀或品牌包裝，更重要的是產品屬性與是否提供下單購買機制。

重點在於：

實際販售的產品是否為管制物質

網站是否具有購買功能或引導購買行為

6）資訊性或教育性網站
若網站僅提供參考資訊（如：用途、副作用、交互作用、劑量說明），
且無提供購買、下單、聯絡方式等功能，應歸為 (2)。

這類網站包含：

醫學百科

健康資訊平台

政府資源

藥品資料庫（如：drugs.com、WebMD、NIH、Mayo Clinic）

即使有提及管制藥品，只要無交易、價格、型號或訂購資訊，就屬資訊性用途。

🧠 特別注意：請勿錯判教育性網站為販售網站。

🔎【待分類 HTML 內容】：

{html}

📋 綜合報告：
最終分類：(1) 電子菸銷售網站  或 (2) 非此類網站

導致此分類的通用判斷依據（根據上面 1～6 條）

若有任何模糊處（例如看起來很專業但其實有販售行為），請說明你的處理方式。


"""
prompt = PromptTemplate.from_template(template=text_template)

# -------------------- 3. 爬取網頁文字 --------------------
def crawl_all_text(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator="\n", strip=True)[:50]
    except requests.exceptions.RequestException as e:
        return f"[Request failed]: {e}"

# -------------------- 4. 爬取圖片 --------------------
def crawl_images(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all("img")
        valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        img_urls = []
        for img in img_tags:
            src = img.get("src")
            if not src:
                continue
            lower_src = src.lower()
            if any(lower_src.endswith(ext) for ext in valid_extensions):
                full_url = requests.compat.urljoin(url, src)
                img_urls.append(full_url)
        return img_urls
    except:
        return []

# -------------------- 5. 下載圖片 --------------------
def download_image(img_url, save_path="images"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    img_name = os.path.join(save_path, os.path.basename(img_url.split("?")[0]))
    try:
        response = requests.get(img_url, stream=True, timeout=10)
        response.raise_for_status()
        with open(img_name, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return img_name
    except:
        return None

# -------------------- 6. 分析圖片 --------------------
def get_image_prompt(img_url: str) -> str:
    return f"""
請提供實際的圖片或圖片網址 {img_url}，我才能分析其中是否包含以下任何受限物品或符號：

電子菸裝置或其零件

電子煙品牌標誌

吸煙煙霧效果

管制藥品或其用具

與藥物文化相關的視覺元素

推廣電子菸的行銷內容等

📷 請上傳圖片，或提供有效的圖片連結，我會立即為你判定是：

🚨 "Warning: Contains restricted items"

✅ "Safe"

Image URL: {img_url}
"""

def classify_image(img_url: str):
    try:
        # 下載圖片並轉為 base64
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
        img_bytes = BytesIO(response.content)
        base64_image = base64.b64encode(img_bytes.read()).decode('utf-8')

        # 傳送給 GPT-4-Vision 分析
        result = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "請判斷這張圖片是否包含電子菸、毒品或相關符號，並只回傳：\n🚨 Warning 或 ✅ Safe"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=50
        )
        return result.choices[0].message.content
    except Exception as e:
        return f"圖片讀取或分析失敗: {e}"
        
# -------------------- 7. Google Search --------------------
def google_search(query, count=10):
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")
    if not api_key or not cx:
        print("❌ GOOGLE_API_KEY 或 GOOGLE_CX 沒有正確設定")
        return []
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        results = []
        fetched = 0
        while fetched < count:
            num = min(10, count - fetched)
            start = fetched + 1
            res = service.cse().list(q=query, cx=cx, num=num, start=start).execute()
            items = res.get("items", [])
            results.extend([item["link"] for item in items])
            fetched += len(items)
            if len(items) < num:
                break
        return results
    except Exception as e:
        print(f"❌ Google 搜尋錯誤：{e}")
        return []

# -------------------- 8. 黑名單 --------------------
blacklist_domains = [
    ".edu", ".gov", ".ac.", ".org", ".wiki", "usask.ca", "su.se", "article",
    "researchgate", "sciencedirect", "osf.io", "digitalcommons",
    "escholarship", "openai.com", "archive.org", "wiktionary",
    "urbandictionary", "dictionary", "bjc-r", "ecprice", "adamrose"
]
blacklist_keywords_in_url = [
    "slang", "street-names", "code-words", "download", "vocab", "wordlist",
    "unigrams", "passphrases", "pdf", "xml", "djvu.txt", "txt", "books",
    "raw/main", "viewcontent.cgi", "novel.pdf", "API/docs", "textfiles",
    "publications"
]

def is_blacklisted_url(url: str) -> bool:
    url_lower = url.lower()
    return any(domain in url_lower for domain in blacklist_domains) or \
           any(kw in url_lower for kw in blacklist_keywords_in_url)

# -------------------- 9. Streamlit 主程式 --------------------
def main():
    st.title("電子菸網站偵測系統")

    st.markdown("""
    <style>
        .stApp {
        background-image: url("https://wallpapers.com/images/hd/dark-grey-aesthetic-iy0yvgt4wq4qafgg.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        }
        h1, h2, h3 {
            color: #00FFFF; /* Electric Blue */
        }
        .stRadio > div {
            flex-direction: row;
            gap: 2rem;
        }
        .stButton > button, .stDownloadButton > button {
            background-color: #3EB489; /* Mint Green */
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
        }
        .stTextInput > div > input,
        .stTextArea > div > textarea {
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)
    st.markdown("## 🧠 利用 OpenAI + 圖片辨識，自動分類電子煙相關網站")
    
    llm_text = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0)
    llm_image = ChatOpenAI(api_key=openai_api_key, model="gpt-4.1", temperature=0)
    parser = StrOutputParser()
    chain = prompt | llm_text | parser

    mode = st.radio("# 選擇模式：", ["單一網址分析", "批量網址分析", "GOOGLE 自動搜尋 & 分析"])

    if mode == "單一網址分析":
        st.markdown("### 🔗 單一網址分析")
        url = st.text_input("請輸入網址：")

        if st.button("🚀 開始分析"):
            if not url.strip():
                st.warning("⚠️ 請輸入有效網址")
                return

            st.markdown(f"### 🔍 正在分析：[{url}]({url})")

            with st.spinner("⏳ 正在讀取網站內容與圖片..."):
                text_content = crawl_all_text(url)
                text_result = chain.invoke(text_content)

                image_urls = crawl_images(url)
                flagged_images = 0

                # 分成兩欄顯示分析結果
                col1,  col2 = st.columns([5,  5])

                with col1:
                    st.markdown("#### 📄 文字分類結果")
                    st.write(text_result)

                with col2:
                    st.markdown("#### 📷 圖像分析結果")
                    if not image_urls:
                        st.write("(未找到圖片)")
                    else:
                        sample_size = min(2, len(image_urls))
                        for img in random.sample(image_urls, sample_size):
                            img_result = classify_image(img, llm_image)
                            st.image(img, caption=f"分類結果: {img_result}")
                            if "Warning" in img_result:
                                flagged_images += 1

            # 綜合結論
            st.markdown("---")
            st.subheader("📋 綜合結論")
            if "(1)" in text_result and flagged_images > 0:
                st.error("⚠️ 高風險網站：網站可能涉及電子煙販售")
            if "(1)" in text_result:
                st.error("⚠️ 高風險網站：網站可能涉及電子煙販售")
            else:
                st.success("✅ 安全網站：未偵測出高風險內容")

    elif mode == "批量網址分析":
        st.markdown("### 📂 批量網址分析")
        uploaded_file = st.file_uploader("請上傳 `.txt` 檔案（每行一個網址）", type=["txt"])

        if st.button("🚀 開始批次分析"):
            if uploaded_file is None:
                st.warning("⚠️ 請先上傳 `.txt` 檔案")
                return

            urls = [line.strip().decode("utf-8") for line in uploaded_file.readlines() if line]
            st.info(f"📄 共有 {len(urls)} 個網址將進行分析")

            high_risk_urls = []

            for idx, url in enumerate(urls, start=1):
                st.markdown(f"---\n### 🔗 [{idx}/{len(urls)}] 分析網址：[{url}]({url})")

                with st.spinner("⏳ 正在分析..."):
                    text_content = crawl_all_text(url)
                    text_result = chain.invoke(text_content)
                    image_urls = crawl_images(url)
                    flagged_images = 0

                    # 左右分區：文字 / 圖像
                    col1,  col2 = st.columns([5, 5])


                    with col1:
                        st.markdown("#### 📄 文字分類結果")
                        st.write(text_result)


                    with col2:
                        st.markdown("#### 📷 圖像分析結果")
                        if not image_urls:
                            st.write("(未找到圖片)")
                        else:
                            for img in image_urls[:2]:
                                img_result = classify_image(img, llm_image)
                                st.image(img, caption=f"分類結果: {img_result}")
                                if "Warning" in img_result:
                                    flagged_images += 1

                # 綜合結論
                if "(1)" in text_result and flagged_images > 0:
                    high_risk_urls.append(url)
                    st.error("⚠️ 高風險網站：網站可能涉及電子煙販售")
                if "(1)" in text_result:
                    high_risk_urls.append(url)
                    st.error("⚠️ 高風險網站：網站可能涉及電子煙販售")
                else:
                    st.success("✅ 安全網站")

            st.markdown("---")
            st.subheader("📋 批次分析總結")

            if high_risk_urls:
                st.warning(f"⚠️ 共偵測到高風險網址 {len(high_risk_urls)} 筆")

                st.download_button(
                    label="📥 下載高風險網址清單",
                    data="\n".join(high_risk_urls),
                    file_name="high_risk_urls.txt",
                    mime="text/plain"
                )
            else:
                st.success("✅ 所有網址皆未偵測到高風險內容")

    else:
        st.markdown("### 🌐 Google 搜尋分析模式")
        st.markdown("> 根據關鍵字自動搜尋網站，並對每個搜尋結果進行 AI 文本與圖像判斷")

        # 輸入關鍵字
        keywords_text = st.text_area(
            "🔤 請輸入搜尋關鍵字（每行一個）",
            "vape\ne-juice\ne-cigarette\n電子煙"
        )

        limit = st.number_input("🔢 每個關鍵字最多擷取幾組網址？", min_value=1, max_value=50, value=10)

        if st.button("🚀 執行 Google 搜尋並分析"):
            if not keywords_text.strip():
                st.warning("⚠️ 請先輸入關鍵字")
                return

            keywords_list = [kw.strip() for kw in keywords_text.split("\n") if kw.strip()]
            st.info(f"🔍 將針對 {len(keywords_list)} 個關鍵字，各擷取 {limit} 組搜尋結果")

            all_urls = []
            for kw in keywords_list:
                st.markdown(f"#### 🔎 搜尋關鍵字：**{kw}**")
                found = google_search(kw, count=limit)
                all_urls.extend([url for url in found if url not in all_urls])

            st.write(f"📥 總共取得 {len(all_urls)} 個原始網址")

            # 過濾黑名單
            filtered_urls = [url for url in all_urls if not is_blacklisted_url(url)]
            st.success(f"✅ 經過過濾後剩下 {len(filtered_urls)} 個可疑網址")

            high_risk_urls = []

            for idx, url in enumerate(filtered_urls, start=1):
                st.markdown(f"---\n### 🔗 [{idx}/{len(filtered_urls)}] 分析網址：[{url}]({url})")

                with st.spinner("⏳ 正在分析..."):
                    text_content = crawl_all_text(url)
                    text_result = chain.invoke(text_content)

                    image_urls = crawl_images(url)
                    flagged_images = 0

                    # 分兩欄顯示文字與圖像
                    col1,  col2 = st.columns([5,  5])

                    with col1:
                        st.markdown("#### 📄 文字分類結果")
                        st.write(text_result)


                    with col2:
                        st.markdown("#### 📷 圖像分析結果")
                        if not image_urls:
                            st.write("(未找到圖片)")
                        else:
                            for img in image_urls[:2]:
                                img_result = classify_image(img, llm_image)
                                st.image(img, caption=f"分類結果: {img_result}")
                                if "Warning" in img_result:
                                    flagged_images += 1

                # 綜合判斷
                if "(1)" in text_result and flagged_images > 0:
                    high_risk_urls.append(url)
                    st.error("⚠️ 高風險網站：網站可能涉及電子煙販售")
                if "(1)" in text_result:
                    high_risk_urls.append(url)
                    st.error("⚠️ 高風險網站：網站可能涉及電子煙販售")
                else:
                    st.success("✅ 安全網站")

            # 總結與下載
            st.markdown("---")
            st.subheader("📋 分析總結")

            if high_risk_urls:
                st.warning(f"⚠️ 偵測到高風險網址：{len(high_risk_urls)} 筆")
                st.download_button(
                    label="📥 下載高風險網址清單",
                    data="\n".join(high_risk_urls),
                    file_name="google_high_risk_urls.txt",
                    mime="text/plain"
                )
            else:
                st.success("✅ 所有搜尋結果均未偵測到高風險內容")

if __name__ == "__main__":
    main()














    
