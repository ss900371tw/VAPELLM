import streamlit as st
import requests
import tempfile
import os
import shutil
import json

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
from langchain_core.prompts import PromptTemplate
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
from serpapi import GoogleSearch

from langchain_google_genai import ChatGoogleGenerativeAI
gemini_api_key = os.getenv("GOOGLE_API_KEY", "")
googlesearch_api_key = os.getenv("GOOGLE_SEARCH_API_KEY", "") 
# -------------------- 2. Prompt --------------------
text_template = """
作為一位專業的電子菸交易網站分類器，
你具備辨識下列 HTML 內容並將其分類的能力：

請依據以下兩類進行分類：

(1) 電子菸銷售網站

(2) 非此類網站

由於產品名稱、品牌或提及方式無窮無盡，請勿僅依賴特定關鍵字，
而應根據通用指標判斷，特別注意以下幾點：

1）使用情境或宣稱內容
請留意是否有明示或暗示改變情緒、緩解壓力、提升專注、助眠、放鬆身心等效果的描述。
若產品宣稱具備非一般性娛樂或健康功效（例如：「強力放鬆」、「超快感」、「助眠神器」、「工作提神」等），可能暗示該電子菸或煙油產品含有特殊添加物，須進一步關注其合法性與成分來源。
電子菸裝置與煙油（e-liquid）若搭配此類宣稱，也應視為電子菸銷售網站的一部分。


2）交易性線索
提及價格、像是「私訊我」、「祕密配方」、「加 LINE 詳談」、「隱密出貨」、「DM 我」、「PM 我」等措辭，
可能與非法或受限產品有關。
若網站提供：
加入購物車
快速下單
產品型錄瀏覽
→ 即便表面合法，也應提高警覺，可能屬於非法販售網站。
→ 對於模糊不清或自相矛盾的聲明也要保持警惕。
⚠️ 注意：專業外觀與科學用語無法掩蓋其銷售管制物質的事實。


3）資訊性或教育性網站
若網站的內容僅限於健康知識、醫療參考、公共衛生宣導，
而未提供任何產品購買、價格、聯絡方式或下單功能，應分類為(2) 非此類網站。

這類網站可能包含：
健康百科全書（如：WebMD、NIH、Mayo Clinic）
醫療或藥品資料庫（如：drugs.com）
政府機構網站或非營利健康平台
探討電子菸對健康影響、成分分析、戒菸建議的科普文章
即使網站中提及電子菸品牌、成分或裝置介紹，只要未涉及販售行為、購物功能、價格資訊或聯絡下單引導，即應歸為資訊性用途。
🧠 特別注意：請勿錯判教育性網站為販售網站。

🔎【待分類 HTML 內容】：

{html}

📋 綜合報告：
最終分類：(1) 電子菸銷售網站  或 (2) 非此類網站

導致此分類的通用判斷依據（根據上面 1～3 條）

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
        return soup.get_text(separator="\n", strip=True)[:100]

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

                    return body_text[:100]

            except Exception as e:
                return f"{url}"



# ---------------------------------------------------------------------------
# 4. 爬取網頁的圖片 URL
# ---------------------------------------------------------------------------





def upload_image_to_imgbb(image_path):
    with open(image_path, "rb") as f:
        IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_API_KEY},
            files={"image": f}
        )
    res.raise_for_status()
    return res.json()["data"]["url"]




import streamlit as st
from playwright.sync_api import sync_playwright
import urllib.parse

from playwright.sync_api import sync_playwright


def search_similar_images_via_serpapi(image_url):
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    params = {
        "engine": "google_reverse_image",
        "api_key": SERPAPI_API_KEY,
        "image_url": image_url,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    st.markdown("""
<style>
/* Expander 標題（用 summary 明確指定並強制覆蓋） */
details > summary {
    background-color: #3b4a6b !important;   /* 比原本亮，偏藍灰 */
    color: white !important;
    font-weight: bold !important;
    border: 1px solid #4da6ff !important;  /* 淺藍邊框 */
    border-radius: 8px !important;
    padding: 10px !important;
    transition: background-color 0.2s ease;
}

/* Hover 更亮一點 */
details > summary:hover {
    background-color: #4b5d88 !important;
    cursor: pointer;
}

/* 展開內容顏色 */
div[data-testid="stExpander"] .streamlit-expanderContent {
    color: #f0f0f0 !important;
}
</style>
""", unsafe_allow_html=True)


    # ✅ 使用收合元件顯示回傳內容
    with st.expander("📦 Click to view SerpAPI response content"):
        st.json(results)

    image_results = results.get("image_results", [])
    urls = [item.get("link") for item in image_results if "link" in item]
    return urls


    
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

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO
from PIL import Image


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, unquote
from io import BytesIO
from PIL import Image
import os
import shutil
import requests
from urllib.parse import urlparse, parse_qs, unquote, urljoin
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

from IPython.display import display, Image as IPyImage  # 用於 Jupyter 顯示圖片

# --- 從 Next.js 優化網址取出原圖 ---
def extract_real_image_url(next_image_url: str) -> str:
    try:
        query = urlparse(next_image_url).query
        params = parse_qs(query)
        real_url = params.get("url", [""])[0]
        return unquote(real_url)
    except:
        return next_image_url

# --- 規範化 src ---
def normalize_src(src: str, base_url: str) -> str:
    if not src:
        return ""
    if src.startswith("//"):
        return "https:" + src
    return urljoin(base_url, src)

# --- 爬圖片 ---
def crawl_images(url: str, max_images=2):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Referer": url
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all("img")

        results = []
        seen = set()

        for img in img_tags:
            src_candidates = [
                img.get("src"),
                img.get("data-src"),
                img.get("data-original"),
                img.get("data-image"),
                img.get("data-lazy"),
            ]

            for raw_src in src_candidates:
                img_url = normalize_src(raw_src, url)
                if not img_url or "base64" in img_url or img_url in seen:
                    continue
                seen.add(img_url)

                if "_next/image" in img_url and "url=" in img_url:
                    img_url = extract_real_image_url(img_url)

                try:
                    img_resp = requests.get(img_url, headers=headers, timeout=5)
                    img_resp.raise_for_status()
                    img = Image.open(BytesIO(img_resp.content)).convert("RGB")

                    img_io = BytesIO()
                    img.save(img_io, format="PNG")
                    img_io.seek(0)

                    results.append((img_io, img_url))
                    break

                except Exception as e:
                    continue

            if len(results) >= max_images:
                break

        return results

    except Exception as e:
        print(f"❌ crawl_images 發生錯誤: {e}")
        return []




# -------------------- 6. 分析圖片 --------------------
def get_image_prompt(img_url: str) -> str:
    return f"""
請協助我分析這張圖片：{img_url}

✅ 請完成以下任務：

1. **描述圖片的整體內容與構圖**（包含出現的物品、人物、背景、動作、文字等）。
2. 根據下列分類，逐一檢查圖片中是否出現相關項目，並說明原因與判斷依據。
3. 若圖片中某項目「可能出現但不確定」，請說明為何不確定。
4. 最後請總結判定結果，並明確說明是否屬於高風險圖片（包含受限項目）。

📋 受限項目分類如下：

**a. 電子菸裝置或零件**  
如主機、本體、電池卡匣、霧化器、吸嘴、充電器等。

**b. 電子菸品牌與標誌**  
如 JUUL、RELX、MYLE 等商標、文字標誌或 LOGO。

**c. 吸煙或霧氣效果**  
圖中是否有明顯煙霧、蒸氣或霧氣擴散效果。

**d. 電子菸文化相關元素**  
如 vape 聚會、煙圈表演（O-rings）、相關塗鴉、穿著印花服飾等。

**e. 推廣行銷內容**  
如促銷標語、價格資訊、購買連結、優惠碼、購物車等導購訊息。

📝 回覆範例格式：
- 圖片描述：XXX
- a. 電子菸裝置：有/無，判斷依據是…
- b. 品牌與標誌：…
- c. 霧氣效果：…
- d. 文化元素：…
- e. 行銷內容：…
- 總結判定：✅ Safe / 🚨 Warning（並說明原因）

📷 請依照以上格式，詳細說明圖片內容與判斷過程。
"""

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from io import BytesIO
import base64

import requests
from io import BytesIO
import base64


from langchain_core.messages import HumanMessage
from io import BytesIO




from langchain_core.messages import HumanMessage
from io import BytesIO
import requests
import os
from io import BytesIO
from langchain_core.messages import HumanMessage

def upload_bytesio_to_imgbb(img_io: BytesIO) -> str:
    """
    將 BytesIO 圖片上傳至 imgbb，回傳圖片網址
    """
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
    if not IMGBB_API_KEY:
        raise ValueError("❌ 請設定環境變數 IMGBB_API_KEY")

    img_io.seek(0)
    res = requests.post(
        "https://api.imgbb.com/1/upload",
        params={"key": IMGBB_API_KEY},
        files={"image": ("image.png", img_io, "image/png")}
    )
    res.raise_for_status()
    return res.json()["data"]["url"]


import base64
import os
import requests
from datetime import datetime
from io import BytesIO




def classify_image(image_input, model):
    """
    回傳：
    - result_text: 分析結果（✅ Safe / 🚨 Warning）
    - image_url: 上傳後的圖片網址（raw.githubusercontent.com 或 imgbb）
    """
    from langchain_core.messages import HumanMessage
    import requests
    from io import BytesIO
    import os

    def upload_bytesio_to_imgbb(img_io: BytesIO) -> str:
        IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
        if not IMGBB_API_KEY:
            raise ValueError("❌ 請設定 IMGBB_API_KEY 環境變數")
        img_io.seek(0)
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_API_KEY},
            files={"image": ("image.png", img_io, "image/png")}
        )
        res.raise_for_status()
        return res.json()["data"]["url"]

    try:
        if isinstance(image_input, str) and image_input.startswith("http"):
            image_url = image_input
        elif isinstance(image_input, BytesIO):
            image_url = upload_bytesio_to_imgbb(image_input)
        else:
            return "❌ 不支援的圖片輸入類型", None

        message = HumanMessage(
            content=[
                {"type": "text", "text": "請判斷這張圖片是否包含電子菸、毒品或相關符號，回傳：🚨 Warning 或 ✅ Safe"},
                {"type": "image_url", "image_url": {"url": image_url}},
            ]
        )
        result = model.invoke([message])
        return result.content, image_url  # ⬅️ 回傳兩個值

    except Exception as e:
        return f"⚠️ 圖片分析失敗：{e}", None



# -------------------- 7. Google Search --------------------
from duckduckgo_search import DDGS

def google_search(query, count=10):
    """
    使用 DuckDuckGo 替代 Google 搜尋，免 API Key、免設定環境
    """
    print(f"🔍 正在搜尋：{query}...")
    results = []
    try:
        # 使用 context manager 呼叫 DuckDuckGo 搜尋
        with DDGS() as ddgs:
            # text() 會回傳搜尋結果，max_results 控制數量
            ddgs_gen = ddgs.text(query, max_results=count)
            if ddgs_gen:
                for r in ddgs_gen:
                    results.append(r['href']) # 'href' 就是網頁連結
        return results
    except Exception as e:
        print(f"❌ 搜尋發生錯誤：{e}")
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
    llm_text = ChatGoogleGenerativeAI(
    google_api_key=gemini_api_key, 
    model="gemini-2.5-pro",  # 或使用 "gemini-pro"
    temperature=0
    )

    llm_image = ChatGoogleGenerativeAI(
    google_api_key=gemini_api_key, 
    model="gemini-2.5-pro",  # 具備強大圖片分析能力的多模態模型
    temperature=0
    )
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
                <div style="font-size: 1.8rem;">{icon}</div>
                <div style="font-size: 1.6rem; font-weight: bold;">{title}</div>
                <div style="font-size: 1.4rem; color: #ccc;">{desc}</div>
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
    col1, col2, col3 , col4= st.columns(4)
    with col1:
        render_card("🔍", "單網分析", "分析個別網站的圖文", key="single")
    with col2:
        render_card("📂", "批量分析", "上傳多網站txt檔分析", key="batch")
    with col3:
        render_card("🌐", "字詞分析", "根據關鍵字爬蟲分析", key="search")
    with col4:
        render_card("📸", "以圖分析", "以圖搜圖並爬蟲分析", key="picture")
    
    mode = st.session_state.get("selected_mode")
    
    if mode:    
        if "單網分析" in mode:
            # 建立左右排列欄位
            # 自訂按鈕樣式讓它貼齊 text_input 高度
            
            # CSS：美化按鈕與輸入框容器
            # --- 自訂樣式 ---

            # --- 自訂樣式 ---
            st.markdown("""
            <style>
            div[data-testid="column"] div:has(button) {
                display: flex;
                align-items: center;
                justify-content: center;
            }
            div[data-testid="column"] div:has(input) {
                display: flex;
                align-items: center;
            }
            input[type="text"] {
                height: 40px;
                font-size: 16px;
                padding: 6px 10px;
                border-radius: 8px;
                border: 1.5px solid #ccc;
            }
            div[data-testid="column"] button {
                height: 40px;
                width: 60px;
                font-size: 18px;
                background-color: #3EB489;
                color: white;
                border-radius: 10px;
                border: 2px solid #ff5f5f;
                padding: 0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # --- 輸入表單區塊 ---
            with st.form("url_input_form"):
                col1, col2 = st.columns([5, 1])
            
                with col1:
                    url = st.text_input("", placeholder="請輸入網址：", label_visibility="collapsed")
            
                with col2:
                    submitted = st.form_submit_button("確定")
            
            # --- 分析邏輯在表單外判斷，才能正確中止流程 ---
            if submitted:
                if not url.strip():
                    st.markdown("""
                    <div style="
                        background-color: #fff3cd;
                        color: #856404;
                        padding: 1rem;
                        border-radius: 10px;
                        border: 1px solid #ffeeba;
                        font-size: 16px;
                    ">
                    ⚠️ 請輸入有效網址
                    </div>
                    """, unsafe_allow_html=True)
                    return
                else:
                    st.markdown(f"""
<h3 style='color:white;'>
🔍 正在分析：<a href='{url}' 
 target='_blank' style='color:#00ffff; text-decoration: underline;'>{url}</a>
</h3>
""", unsafe_allow_html=True)
                    # 這裡可以繼續放分析程式邏輯
                st.markdown("""
    <style>
    .stSpinner > div > div {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)
                with st.spinner("⏳ 正在讀取網站內容與圖片"): 
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
                            for img_io, img_url in random.sample(image_urls, sample_size):
                                img_result = classify_image(img_io, llm_image)
                                verdict, uploaded_img_url = img_result
                                st.markdown(f"""
<div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
    <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
    <img src="{uploaded_img_url}" style="max-width:100%;border-radius:8px;margin-bottom:0.5rem;">
    <div style="font-size:0.9rem;">
        <b>分類結果：</b>{verdict}<br>
        <b>圖片連結：</b><a href="{uploaded_img_url}" target="_blank">{uploaded_img_url}</a>
    </div>
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
    
        elif "批量分析" in mode:
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
                    st.markdown("""
<div style="
    background-color: #fff3cd;
    color: #856404;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #ffeeba;
    font-size: 16px;
">
⚠️ 請先上傳 .txt 檔案
</div>
""", unsafe_allow_html=True)
                    return
    
                urls = [line.strip().decode("utf-8") for line in uploaded_file.readlines() if line]
                st.markdown(f"<h3 style='color:white;'>📄 共有 {len(urls)} 個網址將進行分析", unsafe_allow_html=True)

                high_risk_urls = []
    
                for idx, url in enumerate(urls, start=1):
                    st.markdown(f"""
<h3 style='color:white;'>
🔗 [{idx}/{len(urls)}] 分析網址：
<a href='{url}' target='_blank' style='color:#00ffff; text-decoration: underline;'>{url}</a>
</h3>
""", unsafe_allow_html=True)
                    st.markdown("""
    <style>
    .stSpinner > div > div {
        color: white !important;
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
                            for img_io, img_url in random.sample(image_urls, sample_size):
                                img_result = classify_image(img_io, llm_image)
                                verdict, uploaded_img_url = img_result
                                st.markdown(f"""
<div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
    <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
    <img src="{uploaded_img_url}" style="max-width:100%;border-radius:8px;margin-bottom:0.5rem;">
    <div style="font-size:0.9rem;">
        <b>分類結果：</b>{verdict}<br>
        <b>圖片連結：</b><a href="{uploaded_img_url}" target="_blank">{uploaded_img_url}</a>
    </div>
</div>""", unsafe_allow_html=True)
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
    
        elif "字詞分析" in mode:
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
<h3 style='color:white;'>
🔗 [{idx}/{len(filtered_urls)}] 分析網址：
<a href='{url}' target='_blank' style='color:#00ffff; text-decoration: underline;'>{url}</a>
</h3>
""", unsafe_allow_html=True)
                    

                    st.markdown("""
    <style>
    .stSpinner > div > div {
        color: white !important;
    }
    </style>
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
                            for img_io, img_url in random.sample(image_urls, sample_size):
                                img_result = classify_image(img_io, llm_image)
                                verdict, uploaded_img_url = img_result
                                st.markdown(f"""
<div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
    <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
    <img src="{uploaded_img_url}" style="max-width:100%;border-radius:8px;margin-bottom:0.5rem;">
    <div style="font-size:0.9rem;">
        <b>分類結果：</b>{verdict}<br>
        <b>圖片連結：</b><a href="{uploaded_img_url}" target="_blank">{uploaded_img_url}</a>
    </div>
</div>""", unsafe_allow_html=True)
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
        elif "以圖分析" in mode:
        
            # 初始化狀態旗標
            if "download_finished" not in st.session_state:
                st.session_state.download_finished = False
            if "start_analysis" not in st.session_state:
                st.session_state.start_analysis = False
        
            # 標題 + 上傳區
            st.markdown("<h3 style='color:white;'>📸 上傳圖片以搜尋相似網站</h3>", unsafe_allow_html=True)
            st.markdown('<label style="color:white;font-size:1rem;">📤 請上傳圖片 (jpg, jpeg, png)</label>', unsafe_allow_html=True)
            st.markdown("""
<style>
/* 檔名橘色：適用於已上傳後顯示的檔名區域 */
span[data-testid="uploaded-file-name"] {
    color: #FF7518 !important;  /* 或 #FFA500 更亮的橘色 */
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
            uploaded_files = st.file_uploader(
                "上傳圖片", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed"
            )
        
            # 如果有上傳新圖片 → 重置狀態
            if uploaded_files:
                st.session_state.download_finished = False
                st.session_state.start_analysis = False
        
            # 顯示「開始分析」按鈕
            if st.button("🚀 開始分析"):
                if not uploaded_files:
                    st.markdown("""
                    <div style="
                        background-color: #fff3cd;
                        color: #856404;
                        padding: 1rem;
                        border-radius: 10px;
                        border: 1px solid #ffeeba;
                        font-size: 16px;
                    ">
                    ⚠️ 請先上傳圖片檔案 (.jpg, .jpeg, .png)
                    </div>
                    """, unsafe_allow_html=True) 
                    st.stop()
                else:
                    st.session_state.start_analysis = True
            else:
                st.stop()
        
            # 🔍 分析流程只在「未點擊下載」+「已按下分析」時執行
            if uploaded_files and not st.session_state.download_finished and st.session_state.start_analysis:
                all_high_risk_urls = []
        
                for img_idx, uploaded_file in enumerate(uploaded_files, 1):
                    st.markdown(f"<h3 style='color:white;'>📷 圖片 {img_idx}：{uploaded_file.name}</h3>", unsafe_allow_html=True)
                    st.image(uploaded_file, use_container_width=True)
        
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
        
                    try:
                        image_url = upload_image_to_imgbb(tmp_path)
                        st.markdown(f"""
                            <div style="background-color: #d4edda; color: #155724; padding: 1rem;
                                        border-radius: 10px; border: 1px solid #c3e6cb; font-size: 16px;">
                                ✅ 圖片上傳成功：<a href="{image_url}" target="_blank">{image_url}</a>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("""
    <style>
    .stSpinner > div > div {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)
                        with st.spinner("🔍 使用 Google 搜尋相似圖片中..."):
                            st.markdown("""
    <style>
    .stSpinner > div > div {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)
                            
                            urls = search_similar_images_via_serpapi(image_url)
        
                        st.markdown(f"<p style='color:white;'>🔗 共取得 {len(urls)} 個相似網站網址</p>", unsafe_allow_html=True)
        
                        for url_idx, url in enumerate(urls, 1):
                            st.markdown(f"""
<h3 style='color:white;'>
🔗 [{url_idx}/{len(urls)}] 分析網址：
<a href='{url}' target='_blank' style='color:#00ffff; text-decoration: underline;'>{url}</a>
</h3>
""", unsafe_allow_html=True)
                    

                            st.markdown("""
    <style>
    .stSpinner > div > div {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)
                            with st.spinner("⏳ 正在分析網站內容與圖片..."):
                                text_content = crawl_all_text(url)
                                text_result = chain.invoke(text_content)
                                image_urls = crawl_images(url)
                                flagged_images = 0
        
                                col1, col2 = st.columns([5, 5])
                                with col1:
                                    st.markdown(f"""
                                        <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;
                                                    border-radius:12px;border-left:6px solid #1f77b4;margin-bottom:1rem;">
                                            <h4 style="margin-bottom:0.8rem;">📄 文字分類結果</h4>
                                            <pre style="white-space:pre-wrap;font-size:0.92rem;font-family:inherit;">{text_result}</pre>
                                        </div>
                                    """, unsafe_allow_html=True)
        
                                with col2:
                                    if not image_urls:
                                        st.markdown("""
                                            <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;
                                                        border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
                                                <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
                                                <div style="font-size:0.9rem;"><b>(未找到圖片)</b></div>
                                            </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        sample_size = min(2, len(image_urls))
                                        for img_io, img_url in random.sample(image_urls, sample_size):
                                            img_result = classify_image(img_io, llm_image)
                                            verdict, uploaded_img_url = img_result
                                            st.markdown(f"""
            <div style="background-color:#f7f9fc;padding:1.2rem 1.5rem;border-radius:12px;border-left:6px solid #ff7f0e;margin-bottom:1rem;">
                <h4 style="margin-bottom:0.8rem;">📷 圖像分析結果</h4>
                <img src="{uploaded_img_url}" style="max-width:100%;border-radius:8px;margin-bottom:0.5rem;">
                <div style="font-size:0.9rem;">
                    <b>分類結果：</b>{verdict}<br>
                    <b>圖片連結：</b><a href="{uploaded_img_url}" target="_blank">{uploaded_img_url}</a>
                </div>
            </div>""", unsafe_allow_html=True)
                                            if "Warning" in img_result:
                                                flagged_images += 1
        
                            if "(1)" in text_result or flagged_images > 0:
                                st.markdown("""
                                    <div style="background-color: #fff3cd; color: #856404; padding: 1rem;
                                                border-radius: 10px; border: 1px solid #ffeeba; font-size: 16px;">
                                        ⚠️ <strong>高風險網站</strong>：網站可能涉及電子煙販售
                                    </div>
                                """, unsafe_allow_html=True)
                                all_high_risk_urls.append(url)
                            else:
                                st.markdown("""
                                    <div style="background-color: #d4edda; color: #155724; padding: 1rem;
                                                border-radius: 10px; border: 1px solid #c3e6cb; font-size: 16px;">
                                        ✅ <strong>安全網站</strong>
                                    </div>
                                """, unsafe_allow_html=True)
        
                            st.markdown("---")
        
                    except Exception as e:
                        st.error(f"❌ 發生錯誤：{e}")
        
                # 📋 分析總結
                st.markdown("<h3 style='color:white;'>📋 所有圖片分析總結</h3>", unsafe_allow_html=True)
                unique_urls = sorted(set(all_high_risk_urls))
        
                if unique_urls:
                    st.markdown(f"""
                        <div style="background-color: #fff3cd; color: #856404; padding: 1rem;
                                    border-radius: 10px; border: 1px solid #ffeeba; font-size: 16px;">
                            ⚠️ 共偵測到高風險網址 {len(unique_urls)} 筆
                        </div>
                    """, unsafe_allow_html=True)
        
                    if st.download_button(
                        label="📥 下載高風險網址清單",
                        data="\n".join(unique_urls),
                        file_name="imgsearch_high_risk_urls.txt",
                        mime="text/plain"
                    ):
                        st.session_state.download_finished = True
                        st.session_state.start_analysis = False  # 重置分析狀態
                        st.success("✅ 檔案已下載，請重新上傳圖片進行下一輪分析")
                else:
                    st.markdown("""
                        <div style="background-color: #d4edda; color: #155724; padding: 1rem;
                                    border-radius: 10px; border: 1px solid #c3e6cb; font-size: 16px;">
                            ✅ 所有搜尋結果皆未偵測出高風險內容
                        </div>
                    """, unsafe_allow_html=True)
        


if __name__ == "__main__":
    main()
