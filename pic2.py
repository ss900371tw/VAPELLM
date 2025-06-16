import streamlit as st
import requests
import os
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import ollama
from googleapiclient.discovery import build

# ---------------------------------------------------------------------------
# 1. 初始化
# ---------------------------------------------------------------------------
load_dotenv()
llm_client = ollama.Client()

# ---------------------------------------------------------------------------
# 2. HTML 分析提示模板
# ---------------------------------------------------------------------------
text_template = """
As an expert classifier of e-cigarette and controlled-substance-selling websites,
you are equipped to analyze the following HTML and categorize it as either:
(1) an e-cigarette/controlled-substance-selling website,
(2) not such a website.

Because there are infinitely many potential products, brand names, or references, you will use
general indicators rather than item-specific keywords. In particular, consider the following:

1) Context of Use or Claims:
   - Psychoactive/mind-altering effects?
   - "High", "relieve stress", unusual health claims?

2) Transactional Cues:
   - "Price", "add to cart", "order now", "discreet shipping", "contact me"?

3) Legal Notes:
   - Age gating, regional restrictions, vague disclaimers?

4) Product Type:
   - Controlled substances (e.g., Diazepam, Tramadol) + Add to Cart = classify as (1)
   - Vape/e-cigarette = classify as (1)
   - Supplements or harmless herbal = (2)

5) Don't be fooled by scientific appearance if sale enabled.

6) Educational/Medical:
   - Only discuss (no order/contact) = (2)

---
HTML content to classify:
{html}

---
Comprehensive Report:
- Final classification: (1) or (2)
- What general indicators led to your conclusion?
- If there are ambiguities, explain how resolved.
"""

# ---------------------------------------------------------------------------
# 3. 本地 OLLAMA 分析函數
# ---------------------------------------------------------------------------
def classify_text_with_ollama(text: str, model_name="gemma3"):
    prompt_filled = text_template.replace("{html}", text)
    response = llm_client.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt_filled}]
    )
    return response['message']['content']

def get_image_prompt(img_url: str) -> str:
    return f"""
Analyze this image and determine whether it contains any of the following:
🚨 **If the image contains ANY of the following, classify it as "Warning: Contains restricted items"** 🚨

- E-cigarettes, vape pens, e-liquids, vape tanks or parts
- Controlled substances (weed, pills, cocaine, heroin, etc.)
- Drug-use paraphernalia (bongs, rolling papers, syringes)
- Visuals like 🍁, "420", psychedelic symbols

✅ If NONE of the above are present, classify it as "Safe".

Image URL: {img_url}
"""

def classify_image(img_url: str, model_name='llama3.2-vision:11b'):
    prompt = get_image_prompt(img_url)
    response = llm_client.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# ---------------------------------------------------------------------------
# 4. 抓取文字與圖片
# ---------------------------------------------------------------------------
def crawl_all_text(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator="\n", strip=True)[:5000]
    except:
        return "[Request failed]"

def crawl_images(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return [requests.compat.urljoin(url, img.get("src"))
                for img in soup.find_all("img")
                if img.get("src") and img.get("src").lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    except:
        return []

# ---------------------------------------------------------------------------
# 5. 黑名單規則
# ---------------------------------------------------------------------------
blacklist_domains = [".edu", ".gov", ".ac.", ".org", ".wiki", "openai.com"]
blacklist_keywords_in_url = ["dictionary", "slang", "download", "passphrases", "pdf", "viewcontent.cgi"]

def is_blacklisted_url(url: str) -> bool:
    url = url.lower()
    return any(d in url for d in blacklist_domains) or any(k in url for k in blacklist_keywords_in_url)

# ---------------------------------------------------------------------------
# 6. Google 搜尋功能
# ---------------------------------------------------------------------------
def google_search(query, count=10):
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        results = []
        fetched = 0
        while fetched < count:
            num = min(10, count - fetched)
            start = fetched + 1
            res = service.cse().list(q=query, cx=cx, num=num, start=start).execute()
            results += [item["link"] for item in res.get("items", [])]
            fetched += len(res.get("items", []))
            if len(res.get("items", [])) < num:
                break
        return results
    except:
        return []

# ---------------------------------------------------------------------------
# 7. 分析單一網址
# ---------------------------------------------------------------------------
def analyze_url(url):
    text = crawl_all_text(url)
    result = classify_text_with_ollama(text)
    st.write("📄 **文字分析結果：**")
    st.write(result)

    flagged = 0
    images = crawl_images(url)
    for img in images[:2]:  # 限制前兩張
        img_result = classify_image(img)
        st.image(img, caption=img_result)
        if "Warning" in img_result:
            flagged += 1

    if "(1)" in result:
        st.success("⚠️ 判定：高風險網站")
    elif flagged > 0:
        st.warning("⚠️ 圖片含疑似內容，需警覺")
    else:
        st.info("✅ 判定：無風險")

# ---------------------------------------------------------------------------
# 8. Streamlit 主介面
# ---------------------------------------------------------------------------
def main():
    st.title("🔍 電子菸 / 管制藥品網站辨識工具 (本地 OLLAMA)")
    mode = st.radio("請選擇模式：", ["單一網址分析", "批量網址分析", "Google 搜尋分析"])

    if mode == "單一網址分析":
        url = st.text_input("輸入網址：")
        if st.button("開始分析") and url:
            analyze_url(url)

    elif mode == "批量網址分析":
        uploaded = st.file_uploader("上傳 TXT 檔（每行一個網址）", type="txt")
        if st.button("開始分析") and uploaded:
            urls = [line.strip().decode("utf-8") for line in uploaded.readlines() if line.strip()]
            for url in urls:
                st.subheader(url)
                analyze_url(url)

    elif mode == "Google 搜尋分析":
        kw_text = st.text_area("輸入關鍵字（每行一個）", "vape\ne-cigarette\n電子煙")
        limit = st.number_input("每關鍵字擷取幾筆結果？", min_value=1, max_value=50, value=10)
        if st.button("開始搜尋與分析"):
            kws = [k.strip() for k in kw_text.splitlines() if k.strip()]
            all_urls = []
            for kw in kws:
                st.write(f"🔎 搜尋關鍵字：{kw}")
                found = google_search(kw, count=limit)
                all_urls.extend(found)

            filtered = [u for u in all_urls if not is_blacklisted_url(u)]
            st.write(f"🧪 共 {len(filtered)} 筆非黑名單網址將被分析")
            for idx, url in enumerate(filtered):
                st.subheader(f"[{idx+1}] {url}")
                analyze_url(url)

if __name__ == "__main__":
    main()







    
