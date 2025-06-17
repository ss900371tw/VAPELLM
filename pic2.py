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

# -------------------- 1. 環境變數 --------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY","")


# -------------------- 2. Prompt --------------------
text_template = """
As an expert classifier of e-cigarette and controlled-substance-selling websites,
you are equipped to analyze the following HTML and categorize it as either:
(1) an e-cigarette/controlled-substance-selling website,
(2) not such a website.

Because there are infinitely many potential products, brand names, or references, you will use
general indicators rather than item-specific keywords. In particular, consider the following:

1) **Context of Use or Claims**:
   - Look for explicit or subtle references to psychoactive, mind-altering, or illicit effects.
   - Check if the product or substance is described as mood-altering, giving a "high," 
     relieving stress in an excessive/unusual manner, or otherwise hinting at controlled-substance properties.

2) **Transactional Cues**:
   - Mentions of pricing, "contact me directly," "secret formula," "LINE for details," or 
     "discrete shipping" may suggest illicit or regulated products.
   - Any site that allows **adding a controlled substance to cart**, submitting a **quick order**, or browsing a **product catalog** must be treated with caution, regardless of the overall appearance of legitimacy.

3) **Legal Categorization or Warnings**:
   - Check for restricted sale notes, age gating, disclaimers limiting sale to licensed buyers, or regional restrictions.
   - Be cautious of disclaimers that are vague or contradictory.

4) **Product or Service Type**:
   - **If a product is a known controlled substance or prescription medication** (e.g., Zopiclone, Diazepam, Fentanyl, Ketamine, Alprazolam, Tramadol, etc.), and is shown alongside features like:
     - "Add to Cart"
     - "Quick Order"
     - SKU or catalog number
     - Price lookup
     - Purchase instructions
     
     → **You must classify it as (1)** — even if the site appears scientific, medical, or intended for research.

   - **⚠️ Scientific context or professional branding does NOT override the fact that the product is a controlled substance offered for sale.**

   - E-cigarette devices and e-liquids should also be classified as (1).

   - If the product is a non-controlled supplement, traditional medicine, or harmless herbal product, classify as (2).

5) **Critical Thought**:
   - Do NOT rely solely on appearance, branding, or stated purpose.
   - Prioritize the **actual product type** and **whether the website facilitates ordering** of a controlled substance.

6) Informational or Educational Context:
   - If the website only provides reference information about a drug (such as usage, side effects, interactions, dosages), and does not offer any purchase, order, or contact mechanism, it should be classified as (2).
   - These may include medical encyclopedias, health information platforms, government resources, or pharmacy guides (e.g., drugs.com, WebMD, NIH, or Mayo Clinic).
   - Even if controlled substances are discussed, the absence of ordering capability, pricing, product SKUs, or transactional elements indicates a non-commercial, informative nature.

🧠 Be especially cautious not to misclassify informational reference sites as sellers.

---
HTML content to classify:
{html}

---
Comprehensive Report:
- Final classification: (1) or (2)
- What general indicators led to your conclusion (based on sections 1–6)?
- If there are any ambiguities (e.g., controlled substance on a professional-looking website), explain how you resolved them.
- **Emphasize the product type and orderability over context or appearance.**
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
Analyze this image and determine whether it contains any of the following:
🚨 **If the image contains ANY of the following, classify it as "Warning: Contains restricted items"** 🚨

- **E-cigarettes, vape pens, e-liquids, or any part of a vaping device** (including mouthpiece, tank, battery compartment, or any identifiable section of an e-cigarette).
- **Brand names or logos of vaping-related products** (even if not shown in promotional content).
- **Vape-related smoke effects** (clouds of vapor that indicate the presence of vaping activity).
- **Controlled substances** (such as marijuana, cocaine, heroin, pills, stimulants, or hallucinogens).
- **Paraphernalia associated with substance use** (rolling papers, bongs, syringes, grinders, etc.).
- **Psychoactive substances** (such as psychedelics, mushrooms, LSD, or DMT).
- **Visual elements commonly associated with drug culture** (e.g., "420" references, 🍁 symbols, psychedelic visuals).
- **Marketing materials promoting vaping products** (ads, discounts, promo banners, or promotional product displays).

✅ **If NONE of the above are present, classify it as "Safe".**

Image URL: {img_url}
"""

def classify_image(img_url: str, model: ChatOpenAI):
    prompt_str = get_image_prompt(img_url)
    result = model.invoke([HumanMessage(content=prompt_str)])
    return result.content

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
            background-color: #fce4ec; /* 柔亮的香蕉黃 */
            padding-top: 2rem;
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
    st.markdown("## 🧠 電子菸網站偵測系統")
    st.markdown("# 利用 OpenAI + 圖片辨識，自動分類電子煙相關網站")
    
    llm_text = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0)
    llm_image = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0)
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
            if "(1)" in text_result or flagged_images > 0:
                st.error("⚠️ 高風險網站：網站可能涉及電子煙或管制藥品販售")
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
                if "(1)" in text_result or flagged_images > 0:
                    high_risk_urls.append(url)
                    st.error("⚠️ 高風險網站")
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
                if "(1)" in text_result or flagged_images > 0:
                    high_risk_urls.append(url)
                    st.error("⚠️ 高風險網站")
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














    
