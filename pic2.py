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
    st.title("電子菸網站偵測系統 - OpenAI 版")

    llm_text = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0)
    llm_image = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0)
    parser = StrOutputParser()
    chain = prompt | llm_text | parser

    mode = st.radio("選擇模式：", ["單一網址分析", "批量網址分析", "GOOGLE 自動搜尋 & 分析"])

    if mode == "單一網址分析":
        url = st.text_input("請輸入網址：")
        if st.button("開始分析"):
            if not url.strip():
                st.warning("請輸入有效網址")
                return
            st.subheader(f"分析網址：{url}")
            text_content = crawl_all_text(url)
            text_result = chain.invoke(text_content)
            st.write("📄 文字分類結果：")
            st.write(text_result)

            image_urls = crawl_images(url)
            st.write("🖼 圖片分析結果：")
            flagged_images = 0
            if not image_urls:
                st.write("(未找到圖片)")
            else:
                sample_size = min(2, len(image_urls))  # 最多只抽現有數量的圖片
                for img in random.sample(image_urls, sample_size):
                    img_result = classify_image(img, llm_image)
                    st.image(img, caption=f"分類結果: {img_result}")
                    if "Warning" in img_result:
                        flagged_images += 1

            if "(1)" in text_result or flagged_images > 0:
                st.subheader("綜合結論：")
                st.write("⚠️ 高風險網站")
            else:
                st.subheader("綜合結論：")
                st.write("✅ 安全網站")

    elif mode == "批量網址分析":
        uploaded_file = st.file_uploader("上傳包含可疑網址的 TXT 檔案", type=["txt"])
        if st.button("開始分析"):
            if uploaded_file is None:
                st.warning("請先上傳 .txt 檔")
                return
            urls = [line.strip().decode("utf-8") for line in uploaded_file.readlines() if line]
            high_risk_urls = []
            for url in urls:
                st.subheader(f"分析網址: {url}")
                text_result = chain.invoke(crawl_all_text(url))
                st.write("📄 文字分類結果：")
                st.write(text_result)
                image_urls = crawl_images(url)
                st.write("🖼 圖片分析結果：")
                flagged_images = 0

                if not image_urls:
                    st.write("(未找到圖片)")
                else:
                    for img in image_urls[:2]:  # 最多兩張
                        img_result = classify_image(img, llm_image)
                        st.image(img, caption=f"分類結果: {img_result}")
                        if "Warning" in img_result:
                            flagged_images += 1

                if "(1)" in text_result or flagged_images > 0:
                    high_risk_urls.append(url)
                    st.write("⚠️ 高風險網站")
                else:
                    st.write("✅ 安全網站")
            if high_risk_urls:
                with open("high_risk_urls.txt", "w", encoding="utf-8") as wf:
                    wf.writelines(url + "\n" for url in high_risk_urls)
                st.success(f"⚠️ 偵測到高風險網址 {len(high_risk_urls)} 筆，已存入 high_risk_urls.txt")
                st.download_button(
        label="📥 下載高風險網址清單",
        data="\n".join(high_risk_urls),
        file_name="high_risk_urls.txt",
        mime="text/plain"
    )
            else:
                st.info("未偵測到高風險網址")

    else:
        st.write("這裡將利用 Google 搜尋大量關鍵字，並自動分析文本/圖片。")
        keywords_text = st.text_area("輸入關鍵字 (每行一個)", "vape\ne-juice\ne-cigarette\n電子煙")
        limit = st.number_input("要搜尋多少組結果? (count參數)", min_value=1, max_value=50, value=10)
        if st.button("執行 Google 搜尋並分析"):
            keywords_list = [kw.strip() for kw in keywords_text.split("\n") if kw.strip()]
            all_urls = []
            for kw in keywords_list:
                found = google_search(kw, count=limit)
                all_urls.extend([url for url in found if url not in all_urls])
            filtered_urls = [url for url in all_urls if not is_blacklisted_url(url)]
            high_risk_urls = []
            for idx, url in enumerate(filtered_urls, start=1):
                st.subheader(f"[{idx}/{len(filtered_urls)}] 分析網址: {url}")
                text_result = chain.invoke(crawl_all_text(url))
                st.write("📄 文字分類結果：")
                st.write(text_result)
                image_urls = crawl_images(url)
                st.write("🖼 圖片分析結果：")
                flagged_images = 0

                if not image_urls:
                    st.write("(未找到圖片)")
                else:
                    for img in image_urls[:2]:  # 最多兩張
                        img_result = classify_image(img, llm_image)
                        st.image(img, caption=f"分類結果: {img_result}")
                        if "Warning" in img_result:
                            flagged_images += 1
                if "(1)" in text_result or flagged_images > 0:
                    high_risk_urls.append(url)
                    st.write("⚠️ 高風險網站")
                else:
                    st.write("✅ 安全網站")
            if high_risk_urls:
                with open("google_high_risk_urls.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(high_risk_urls))
                st.success(f"✅ 偵測到高風險網址 {len(high_risk_urls)} 筆，已儲存至 google_high_risk_urls.txt")
                st.download_button(
        label="📥 下載高風險網址清單",
        data="\n".join(high_risk_urls),
        file_name="google_high_risk_urls.txt",
        mime="text/plain"
    )

            else:
                st.info("未偵測到高風險網址")
                  
if __name__ == "__main__":
    main()














    
