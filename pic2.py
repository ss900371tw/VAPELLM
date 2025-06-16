import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import shutil
from dotenv import load_dotenv
from PIL import Image
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# 1️⃣ 載入 .env 取得 API Key
load_dotenv()
api_key = os.getenv("OLLAMA_API_KEY", "")

# 2️⃣ 定義 LLM 分析 Prompt
template = """
As an expert classifier of e-cigarette and controlled-substance-selling websites,
you are equipped to analyze the following HTML and categorize it as either:
(1) an e-cigarette/controlled-substance-selling website,
(2) not such a website.

Because there are infinitely many potential products, brand names, or references, you will use
general indicators rather than item-specific keywords. In particular, consider the following:

1) **Context of Use or Claims**:
   - Look for explicit or subtle references to psychoactive, mind-altering, or illicit effects.
   - Check if the product or substance is described as mood-altering, giving a “high,” 
     relieving stress in an excessive/unusual manner, or otherwise hinting at controlled-substance properties.

2) **Transactional Cues**:
   - Mentions of pricing, “contact me directly,” “secret formula,” “LINE for details,” or 
     “discrete shipping” may suggest illicit or regulated products.
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
prompt = PromptTemplate.from_template(template=template)


# 3️⃣ 爬取網頁的文字內容
def crawl_all_text(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator="\n", strip=True)[:1000]  # 限制長度，避免超過 LLM context window
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

# 4️⃣ 爬取網頁的圖片 URL
def crawl_images(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all("img")
        
        valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        return [requests.compat.urljoin(url, img.get("src")) for img in img_tags if img.get("src") and any(img.get("src").lower().endswith(ext) for ext in valid_extensions)]
    except requests.exceptions.RequestException:
        return []

# 5️⃣ 下載圖片（如果需要）
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
    except requests.exceptions.RequestException:
        return None

# 6️⃣ 使用 Vision AI 分析圖片
def classify_image(img_url, model):
    """
    直接使用圖片 URL 分析，如果無法獲取 URL，則轉 Base64 傳遞
    """
    prompt = f"""
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
    from langchain_core.messages import HumanMessage
    result = model.invoke([HumanMessage(content=prompt)])
    return result.content  # 回傳 LLM 結果

# 7️⃣ Streamlit 介面
def main():
    st.title("電子菸/管制物品網站分類器")

    # 提供選擇模式的選單
    mode = st.radio("選擇分析模式", ("單一網址分析", "批量網址分析"))

    # 初始化 LLM
    model = ChatGroq(api_key=api_key, model_name='llama3-8b-8192')
    parser = StrOutputParser()
    chain = prompt | model | parser

    if mode == "單一網址分析":
        # 單一網址輸入
        url = st.text_input("請輸入網址：")
        if st.button("開始分析"):
            if not url.strip():
                st.warning("請輸入有效的 URL。")
                return

            st.subheader(f"分析網址: {url}")

            # 爬取網頁文字
            with st.spinner("文字分析中..."):
                all_text = crawl_all_text(url)
                text_result = chain.invoke(all_text)

            st.write("📄 文字分類結果：")
            st.write(text_result)

            # 爬取圖片
            st.write("🖼 圖片分類結果：")
            image_urls = crawl_images(url)
            flagged_images = 0

            if not image_urls:
                st.write("未找到圖片")
            else:
                for img_url in image_urls[:10]:  # 只分析前 5 張圖片
                    image_result = classify_image(img_url, model)
                    st.image(img_url, caption=f"分類結果: {image_result}")
                    if "Warning" in image_result:
                        flagged_images += 1

            # 綜合判斷
            if flagged_images == 0 and "(2)" in text_result:
                final_decision = "✅ 安全網站"
            elif flagged_images >= 0 and "(1)" in text_result:
                final_decision = "⚠️ 高風險網站"
            st.subheader("綜合分類結果：")
            st.write(final_decision)

    elif mode == "批量網址分析":
        uploaded_file = st.file_uploader("上傳包含可疑網址的 TXT 檔案", type=["txt"])
        
        if st.button("開始分析"):
            if uploaded_file is None:
                st.warning("請上傳一個 .txt 檔案")
                return

            # 讀取檔案內容
            urls = [line.strip().decode("utf-8") for line in uploaded_file.readlines() if line]

            if not urls:
                st.warning("檔案中沒有找到有效網址")
                return

            st.write(f"📌 共讀取 {len(urls)} 個網址")

            high_risk_urls = []  # 存放高風險網址

            for url in urls:
                st.subheader(f"分析網址: {url}")

                # 爬取網頁文字
                with st.spinner("文字分析中..."):
                    all_text = crawl_all_text(url)
                    text_result = chain.invoke(all_text)

                st.write("📄 文字分類結果：")
                st.write(text_result)

                # 爬取圖片
                st.write("🖼 圖片分類結果：")
                image_urls = crawl_images(url)
                flagged_images = 0

                if not image_urls:
                    st.write("未找到圖片")
                else:
                    for img_url in image_urls[:5]:  # 只分析前 5 張圖片
                        image_result = classify_image(img_url, model)
                        st.image(img_url, caption=f"分類結果: {image_result}")
                        if "Warning" in image_result:
                            flagged_images += 1

                if "(1)" in text_result and flagged_images >= 0:
                    high_risk_urls.append(url)

            # 儲存高風險網址
            if high_risk_urls:
                with open("high_risk_urls.txt", "w", encoding="utf-8") as file:
                    file.writelines(url + "\n" for url in high_risk_urls)
                st.success("✅ 高風險網址已存入 `high_risk_urls.txt`")

if __name__ == "__main__":
    main()


























    