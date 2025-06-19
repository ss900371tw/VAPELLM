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
from googleapiclient.discovery import build
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from urllib.parse import urljoin
import pickle
from googleapiclient.discovery import build
from PIL import Image
from io import BytesIO
from langchain_core.messages import AIMessage
from playwright.sync_api import sync_playwright
import sys
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import pickle
from bs4 import BeautifulSoup
import requests
import time
import sys
from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc

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


import subprocess
import os

# 確保瀏覽器已安裝（僅首次部署會觸發）
def ensure_playwright_browser():
    chromium_path = os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome")
    if not os.path.exists(chromium_path):
        try:
            print("⚙️ 安裝 Playwright 瀏覽器中...")
            subprocess.run(["playwright", "install", "chromium"], check=True)
        except Exception as e:
            print("❌ Playwright 安裝失敗:", e)

ensure_playwright_browser()

from urllib.parse import urlparse
import pickle
import time
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession

from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import pickle
from bs4 import BeautifulSoup
import requests
import time

from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import pickle
from bs4 import BeautifulSoup
import requests
import time



import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pickle
import asyncio
from playwright.async_api import async_playwright


import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pickle
import time
import undetected_chromedriver as uc  # ✅ 保留這個，不使用也不刪除
import asyncio
from playwright.async_api import async_playwright


from bs4 import BeautifulSoup
import requests
import pickle
import time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright


import requests
from bs4 import BeautifulSoup
import pickle
import time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import undetected_chromedriver as uc

import os
import requests
import pickle
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import undetected_chromedriver as uc

from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import pickle
from bs4 import BeautifulSoup
import requests



import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import undetected_chromedriver as uc
import pickle
import time


import undetected_chromedriver as uc
import time
import pickle

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

# save_cookie.py
import asyncio
from playwright.async_api import async_playwright
import pickle
import os

from seleniumbase import SB
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pickle
import time
from playwright.sync_api import sync_playwright

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import pickle
import os



def crawl_all_text(url: str, cookie_file: str = "cookies.pkl"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator="\n", strip=True)[:50]

    except requests.exceptions.RequestException as e:
        if "403" in str(e):
            print("⚠️ HTTP 403 Forbidden - 切換為 Playwright 繞過驗證")

            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=False)  # 建議 debug 時先用非 headless
                    context = browser.new_context()

                    parsed = urlparse(url)
                    base_url = f"{parsed.scheme}://{parsed.netloc}/"

                    # 先開首頁，建立 domain context
                    page = context.new_page()
                    page.goto(base_url, timeout=30000)
                    time.sleep(3)

                    # 載入 cookies（如有）
                    try:
                        with open(cookie_file, "rb") as f:
                            cookies = pickle.load(f)
                            for cookie in cookies:
                                if 'domain' not in cookie:
                                    cookie['domain'] = "." + parsed.hostname
                            context.add_cookies(cookies)
                    except Exception as err:
                        print("⚠️ Cookie 載入失敗:", err)

                    # 跳轉到目標頁面
                    page.goto(url, timeout=30000)
                    time.sleep(5)
                    html = page.content()
                    browser.close()

                    soup = BeautifulSoup(html, "html.parser")
                    for tag in soup(["script", "style"]):
                        tag.decompose()

                    body_text = soup.get_text(separator="\n", strip=True)
                    if "驗證您是人類" in body_text or "Enable JavaScript and cookies to continue" in body_text:
                        return "[⚠️ Cloudflare Verification Failed] Cookie 可能失效或未正確附加"

                    return body_text[:50]

            except Exception as e:
                return f"{url}"



# ---------------------------------------------------------------------------
# 4. 爬取網頁的圖片 URL
# ---------------------------------------------------------------------------


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def is_image_url(url: str) -> bool:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36"
        }
        resp = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        return resp.headers.get("Content-Type", "").lower().startswith("image/")
    except:
        return False

def normalize_src(src: str, base_url: str) -> str:
    if not src:
        return ""
    if src.startswith("//"):
        return "https:" + src
    return urljoin(base_url, src)

def crawl_images(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all("img")

        valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        seen = set()
        img_urls = []

        for img in img_tags:
            src_candidates = [
                img.get("src"),
                img.get("data-src"),
                img.get("data-original"),
                img.get("data-image"),
                img.get("data-lazy"),
            ]

            for src in src_candidates:
                if not src:
                    continue
                full_url = normalize_src(src, url)
                if full_url in seen or len(full_url) < 10 or "base64" in full_url:
                    continue
                seen.add(full_url)

                lower_url = full_url.lower()
                if any(lower_url.endswith(ext) for ext in valid_extensions):
                    img_urls.append(full_url)
                    break
                elif is_image_url(full_url):
                    img_urls.append(full_url)
                    break

        return img_urls
    except Exception as e:
        print(f"[crawl_images error]: {e}")
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

def classify_image(image_input, model):
    """
    image_input 可以是：
    - 圖片網址 (str)
    - BytesIO 圖片資料（目前不支援）
    - 本地檔案路徑 (str)
    model: ChatOpenAI 類型模型（如 gpt-4-vision-preview）
    """
    try:
        # 如果是網址
        if isinstance(image_input, str) and image_input.startswith("http"):
            message = HumanMessage(
                content=[
                    {"type": "text", "text": "請判斷這張圖片是否包含電子菸、毒品或相關符號，回傳：🚨 Warning 或 ✅ Safe"},
                    {"type": "image_url", "image_url": {"url": image_input}},
                ]
            )
        elif isinstance(image_input, BytesIO):
            raise ValueError("LangChain 不支援 BytesIO 圖片輸入，請改用 OpenAI SDK")
        else:
            raise TypeError("不支援的圖片輸入類型")

        result = model.invoke([message])
        return result.content

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
    st.markdown("<h1 style='text-align:center;color:white;'>電子菸網站偵測系統</h1>", unsafe_allow_html=True)
    # 使用 OpenAI GPT-4o 模型


    # 背景樣式與主題文字
    st.markdown("""
    <style>
        .stApp {
            background-image: url("https://raw.githubusercontent.com/ss900371tw/VAPELLM/refs/heads/main/%E9%9B%BB%E5%AD%90%E8%8F%B8%E7%B6%B2%E7%AB%99%E5%81%B5%E6%B8%AC%E7%B3%BB%E7%B5%B1%20bg.png");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        h1, h2, h3 {
            color: #00FFFF;
        }
        .stButton > button {
            background-color: #3EB489;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center; font-size: 24px; color: white;'>🧠 利用 OpenAI + 圖片辨識，自動分類電子煙相關網站</p>
    """, unsafe_allow_html=True)
    llm_text = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0)
    llm_image = ChatOpenAI(api_key=openai_api_key, model="gpt-4.1", temperature=0)
    parser = StrOutputParser()
    chain = prompt | llm_text | parser
    # 初始化
    if "selected_mode" not in st.session_state:
        st.session_state.selected_mode = None


                
    def render_card(icon, title, desc, key):
        selected = st.session_state.get("selected_mode") == title
        border = "4px solid #3EB489" if selected else "1px solid #999999"
        shadow = "0 0 20px #3EB489" if selected else "none"
        bg = "#0c1b2a" if selected else "#1a1f2b"
    
        with st.container():
            st.markdown(f"""
            <style>
            div#{key}_card {{
                background-color: {bg};
                color: white;
                border-radius: 16px;
                border: {border};
                box-shadow: {shadow};
                padding: 1.5rem;
                height: 320px;
                text-align: center;
                transition: all 0.2s ease;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}
            div#{key}_card:hover {{
                transform: scale(1.02);
                box-shadow: 0 0 25px #3EB489;
            }}
            div[data-testid="stButton"] > button#{key}_btn {{
                background-color: #3EB489;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-size: 1rem;
                height: 40px;
                padding: 0 1.2rem;
            }}
            </style>
            """, unsafe_allow_html=True)
    
            # ✅ 把所有內容寫在這一個 HTML block 裡
            st.markdown(f"""
            <div id="{key}_card">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="font-size: 1.2rem; font-weight: bold;">{title}</div>
                <div style="font-size: 0.9rem; color: #ccc;">{desc}</div>
                <div style="margin-top: 10px;">
            """, unsafe_allow_html=True)
    
            # ✅ Streamlit 的按鈕也放在 div 裡面
            if st.button("選擇", key=f"{key}_btn"):
                st.session_state.selected_mode = title
                st.rerun()
    
            st.markdown("</div></div>", unsafe_allow_html=True)  # 關閉兩層 div

    # 模式選擇
    st.markdown("""
<style>
.banner-text {
    background-color: #0052cc;  /* 深藍色 */
    color: white;               /* 白字 */
    font-size: 16px;
    font-weight: bold;
    text-align: center;
    padding: 10px;
    border-radius: 6px;
    margin: 10px 0px;
}
</style>

<div class="banner-text">
請選擇分析模式
</div>
""", unsafe_allow_html=True)

    if "selected_mode" not in st.session_state:
        st.session_state.selected_mode = None

    # 集中處理按鈕事件
    col1, col2, col3 = st.columns(3)
    with col1:
        render_card("🔍", "單一網址分析", "分析單個網站的文字與圖片", key="single")
    with col2:
        render_card("📂", "批量網址分析", "上傳文字檔，分析多個網站", key="batch")
    with col3:
        render_card("🌐", "關鍵字搜尋分析", "根據關鍵字自動搜尋網站", key="search")
    
    mode = st.session_state.get("selected_mode")
    
    if mode:    
        if "單一網址分析" in mode:
            # 建立左右排列欄位
            # 自訂按鈕樣式讓它貼齊 text_input 高度
            
            # CSS：美化按鈕與輸入框容器
            # --- 自訂樣式 ---
            st.markdown("""
            <style>
            /* ✅ 只針對含有按鈕的欄位內部，垂直置中 */
            div[data-testid="column"] div:has(button) {
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            /* ✅ 自訂按鈕樣式 */
            div[data-testid="column"] button {
                height: 40px;
                width: 60px;
                font-size: 20px;
                background-color: #3EB489;
                color: white;
                border-radius: 10px;
                border: 2px solid #ff5f5f;
                padding: 0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # --- 表單輸入區塊 ---
            with st.form("url_input_form"):
                col1, col2 = st.columns([6, 1])
                
                with col1:
                    url = st.text_input("", placeholder="請輸入網址：", label_visibility="collapsed")
                
                with col2:
                    submitted = st.form_submit_button("確定")
            
                if submitted and url.strip():
                    st.success(f"✅ 你輸入的網址是：{url}")
                elif submitted:
                    st.warning("⚠️ 請輸入有效網址")
            

            # 分析邏輯
            if go:
                if not url.strip():
                    st.warning("⚠️ 請輸入有效網址")
                    return
    
                st.markdown(f"<h3 style='color:white;'>🔍 正在分析：<a href='{url}'>{url}</a></h3>", unsafe_allow_html=True)

                st.markdown("<p style='color:white;'>⏳ 正在讀取網站內容與圖片...</p>", unsafe_allow_html=True)

                with st.spinner(" "): 
                    text_content = crawl_all_text(url)
                    text_result = chain.invoke(text_content)
    
                    image_urls = crawl_images(url)
                    flagged_images = 0
    
                    # 分成兩欄顯示分析結果
                    col1,  col2 = st.columns([5,  5])
    
                    with col1:
                        st.markdown(f"""
    <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #1f77b4;margin-bottom:1rem;">
        <h4 style="margin-bottom:0.8rem;">📄 文字分類結果</h4>
        <pre style="white-space:pre-wrap;font-size:0.92rem;font-family:inherit;">
    {text_result} 
        </pre>
    </div>
    """, unsafe_allow_html=True)
                    with col2:
                        if not image_urls:
                            st.markdown(f"""
    <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
        <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
        <div style="font-size:0.9rem;"><b>(未找到圖片)</b></div>
    </div>
    """, unsafe_allow_html=True)
                        else:
                            sample_size = min(2, len(image_urls))
                            for img in random.sample(image_urls, sample_size):
                                img_result = classify_image(img, llm_image)
                                st.markdown(f"""
    <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
        <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
        <img src="{img}" style="max-width:100%;border-radius:8px;margin-bottom:0.5rem;">
        <div style="font-size:0.9rem;"><b>分類結果：</b>{img_result}</div>
    </div>""", unsafe_allow_html=True)
                                if "Warning" in img_result:
                                    flagged_images += 1
    
    
    
                st.markdown("---")
                st.markdown("<h3 style='color:white;'>📋 綜合結論</h3>", unsafe_allow_html=True)
                if "(1)" in text_result and flagged_images > 0:
                    st.markdown("""
<div style="
    background-color: #fff3cd;
    color: #856404;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #ffeeba;
    font-size: 16px;
">
⚠️ <strong>高風險網站</strong>：網站可能涉及電子煙販售
</div>
""", unsafe_allow_html=True)
                if "(1)" in text_result:
                    st.markdown("""
<div style="
    background-color: #fff3cd;
    color: #856404;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #ffeeba;
    font-size: 16px;
">
⚠️ <strong>高風險網站</strong>：網站可能涉及電子煙販售
</div>
""", unsafe_allow_html=True)
                else:
                    st.markdown("""
<div style="
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #c3e6cb;
    font-size: 16px;
">
✅ <strong>安全網站</strong>：未偵測出高風險內容
</div>
""", unsafe_allow_html=True)
    
        elif "批量網址分析" in mode:
            st.markdown("""
<style>
/* 將 file_uploader 的標籤與上傳檔名都改為白色 */
label, .stFileUploader label {
    color: white !important;
}

/* 檔名顯示區塊文字（含大小） */
section[data-testid="stFileUploader"] div[aria-label] p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# 檔案上傳元件

            uploaded_file = st.file_uploader("請上傳 .txt 檔案（每行一個網址）", type=["txt"])
    
            if st.button("🚀 開始批次分析"):
                if uploaded_file is None:
                    st.warning("⚠️ 請先上傳 .txt 檔案")
                    return
    
                urls = [line.strip().decode("utf-8") for line in uploaded_file.readlines() if line]
                st.markdown(f"<h3 style='color:white;'>📄 共有 {len(urls)} 個網址將進行分析", unsafe_allow_html=True)

                high_risk_urls = []
    
                for idx, url in enumerate(urls, start=1):
                    st.markdown(f"<h3 style='color:white;'>\n 🔗 [{idx}/{len(urls)}] 分析網址：{url}", unsafe_allow_html=True)

                    st.markdown("""
<style>
/* Modify spinner text color to match theme's primaryColor */
div[role="status"] > div > span {
    color: var(--primary-color) !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


                    with st.spinner("⏳ 正在分析..."):
                        text_content = crawl_all_text(url)
                        text_result = chain.invoke(text_content)
                        image_urls = crawl_images(url)
                        flagged_images = 0
    
                        # 左右分區：文字 / 圖像
                        col1,  col2 = st.columns([5, 5])
    
                    with col1:
                        st.markdown(f"""
    <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #1f77b4;margin-bottom:1rem;">
        <h4 style="margin-bottom:0.8rem;">📄 文字分類結果</h4>
        <pre style="white-space:pre-wrap;font-size:0.92rem;font-family:inherit;">
    {text_result}
        </pre>
    </div>
    """, unsafe_allow_html=True)
                    with col2:
                        if not image_urls:
                            st.markdown(f"""
    <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
        <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
        <div style="font-size:0.9rem;"><b>(未找到圖片)</b></div>
    </div>
    """, unsafe_allow_html=True)
                        else:
                            sample_size = min(2, len(image_urls))
                            for img in random.sample(image_urls, sample_size):
                                img_result = classify_image(img, llm_image)
                                st.markdown(f"""
    <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
        <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
        <img src="{img}" style="max-width:100%;border-radius:8px;margin-bottom:0.5rem;">
        <div style="font-size:0.9rem;"><b>分類結果：</b>{img_result}</div>
    </div>
    """, unsafe_allow_html=True)
                                if "Warning" in img_result:
                                    flagged_images += 1
    
    
                    st.markdown("---")
                    # 綜合判斷
                    if "(1)" in text_result and flagged_images > 0:
                        st.markdown("""
<div style="
    background-color: #fff3cd;
    color: #856404;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #ffeeba;
    font-size: 16px;
">
⚠️ <strong>高風險網站</strong>：網站可能涉及電子煙販售
</div>
""", unsafe_allow_html=True)
                        high_risk_urls.append(url)
                    if "(1)" in text_result:
                        st.markdown("""
<div style="
    background-color: #fff3cd;
    color: #856404;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #ffeeba;
    font-size: 16px;
">
⚠️ <strong>高風險網站</strong>：網站可能涉及電子煙販售
</div>
""", unsafe_allow_html=True)
                        high_risk_urls.append(url)

                    else:
                        st.markdown("""
<div style="
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #c3e6cb;
    font-size: 16px;
">
✅ <strong>安全網站</strong>：未偵測出高風險內容
</div>
""", unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("<h3 style='color:white;'>📋 批次分析總結</h3>", unsafe_allow_html=True)
                high_risk_urls = sorted(set(high_risk_urls))

                if high_risk_urls:
                    st.markdown(f"<h3 style='color:white;'>⚠️ 共偵測到高風險網址 {len(high_risk_urls)} 筆", unsafe_allow_html=True)
    
                    st.download_button(
                        label="📥 下載高風險網址清單",
                        data="\n".join(high_risk_urls),
                        file_name="high_risk_urls.txt",
                        mime="text/plain"
                    )
                else:
                    st.markdown("""
<div style="
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #c3e6cb;
    font-size: 16px;
">
✅ 所有網址皆未偵測到高風險內容
</div>
""", unsafe_allow_html=True)
    
        else:
            # 輸入關鍵字
            # 自訂文字顏色為白色
            st.markdown("""
            <style>
            /* 調整 text_area 與 number_input 的標籤文字為白色 */
            label, .stTextArea label, .stNumberInput label {
                color: white !important;
            }
            
            /* 調整輸入框中文字為白色，背景為深色（可視需求調整） */
            textarea, input[type="number"] {
                color: white !important;
                background-color: #1a1f2b !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # UI 元件
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
                st.markdown(f"""
<div style='
    background-color: #1e3a5f;
    color: white;
    padding: 1rem;
    border-left: 5px solid #3EB489;
    border-radius: 5px;
    font-size: 1rem;
'>
🔍 將針對 <strong>{len(keywords_list)}</strong> 個關鍵字，各擷取 <strong>{limit}</strong> 組搜尋結果
</div>
""", unsafe_allow_html=True)
    
                all_urls = []
                for kw in keywords_list:
                    st.markdown(f"""
<h4 style='color:white;'>🔎 搜尋關鍵字：<strong>{kw}</strong></h4>
""", unsafe_allow_html=True)
                    found = google_search(kw, count=limit)
                    all_urls.extend([url for url in found if url not in all_urls])
    
                st.markdown(f"""
<p style="color:white; font-size:1rem;">
📥 總共取得 <strong>{len(all_urls)}</strong> 個原始網址
</p>
""", unsafe_allow_html=True)
    
                # 過濾黑名單
                filtered_urls = [url for url in all_urls if not is_blacklisted_url(url)]
                st.markdown(f"""
<div style='
    background-color: #2e7d32;
    color: white;
    padding: 1rem;
    border-left: 5px solid #00c853;
    border-radius: 5px;
    font-size: 1rem;
'>
✅ 經過過濾後剩下 <strong>{len(filtered_urls)}</strong> 個可疑網址
</div>
""", unsafe_allow_html=True)

    
                high_risk_urls = []
    
                for idx, url in enumerate(filtered_urls, start=1):
                    st.markdown(f"""
<hr style="border-top: 1px solid white;"/>
<h3 style="color:white;">
🔗 [{idx}/{len(filtered_urls)}] 分析網址：<a href="{url}" target="_blank" style="color:white; text-decoration:underline;">{url}</a>
</h3>
""", unsafe_allow_html=True)
    
                    with st.spinner("⏳ 正在分析..."):
                        text_content = crawl_all_text(url)
                        text_result = chain.invoke(text_content)
    
                        image_urls = crawl_images(url)
                        flagged_images = 0
    
                        # 分兩欄顯示文字與圖像
                        col1,  col2 = st.columns([5,  5])
    
                    with col1:
                        st.markdown(f"""
    <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #1f77b4;margin-bottom:1rem;">
        <h4 style="margin-bottom:0.8rem;">📄 文字分類結果</h4>
        <pre style="white-space:pre-wrap;font-size:0.92rem;font-family:inherit;">
    {text_result}
        </pre>
    </div>
    """, unsafe_allow_html=True)
                    with col2:
                        if not image_urls:
                            st.markdown(f"""
    <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
        <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
        <div style="font-size:0.9rem;"><b>(未找到圖片)</b></div>
    </div>
    """, unsafe_allow_html=True)
                        else:
                            sample_size = min(2, len(image_urls))
                            for img in random.sample(image_urls, sample_size):
                                img_result = classify_image(img, llm_image)
                                st.markdown(f"""
    <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
        <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
        <img src="{img}" style="max-width:100%;border-radius:8px;margin-bottom:0.5rem;">
        <div style="font-size:0.9rem;"><b>分類結果：</b>{img_result}</div>
    </div>
    """, unsafe_allow_html=True)
                                if "Warning" in img_result:
                                    flagged_images += 1
    
    
    
                    
                    st.markdown("---")
                    # 綜合判斷
                    if "(1)" in text_result and flagged_images > 0:
                        st.markdown("""
    <div style="
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ffeeba;
        font-size: 16px;
    ">
    ⚠️ <strong>高風險網站</strong>：網站可能涉及電子煙販售
    </div>
    """, unsafe_allow_html=True)
                        high_risk_urls.append(url)

                    if "(1)" in text_result:
                        st.markdown("""
    <div style="
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ffeeba;
        font-size: 16px;
    ">
    ⚠️ <strong>高風險網站</strong>：網站可能涉及電子煙販售
    </div>
    """, unsafe_allow_html=True)
                        high_risk_urls.append(url)

                    else:
                        st.markdown("""
    <div style="
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        font-size: 16px;
    ">
    ✅ <strong>安全網站</strong>：未偵測出高風險內容
    </div>
    """, unsafe_allow_html=True)
    
                # 總結與下載
                st.markdown("---")
                st.markdown("<h2 style='color:white;'>📋 分析總結</h2>", unsafe_allow_html=True)
                high_risk_urls = sorted(set(high_risk_urls))

                if high_risk_urls:
                    st.warning(f"⚠️ 偵測到高風險網址：{len(high_risk_urls)} 筆")
                    st.download_button(
                        label="📥 下載高風險網址清單",
                        data="\n".join(high_risk_urls),
                        file_name="google_high_risk_urls.txt",
                        mime="text/plain"
                    )
                else:
                    st.markdown("""
    <div style="
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        font-size: 16px;
    ">
    ✅ 所有搜尋結果均未偵測到高風險內容
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


