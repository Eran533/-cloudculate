from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time
import traceback

def scrape_aws_architectures():
    try:
        print("🔍 Starting scrape_aws_architectures")

        chrome_bin = os.getenv("CHROME_BIN", "/usr/bin/google-chrome")
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver")

        print(f"🛠 Using Chrome binary: {chrome_bin}")
        print(f"🛠 Using ChromeDriver path: {chromedriver_path}")

        if not os.path.isfile(chrome_bin):
            print(f"⚠️ Chrome binary not found at: {chrome_bin}")
        else:
            print("✅ Chrome binary found")

        if not os.path.isfile(chromedriver_path):
            print(f"⚠️ Chromedriver not found at: {chromedriver_path}")
        else:
            print("✅ Chromedriver found")

        options = Options()
        options.add_argument("--headless=new")  # or comment out for GUI mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/114.0.5735.110 Safari/537.36")
        options.binary_location = chrome_bin

        print("⚙️ Chrome options configured")

        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)

        # Remove "navigator.webdriver"
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })

        print("✅ WebDriver initialized successfully")

        url = "https://www.netcomlearning.com/blog/aws-service-list"
        print(f"🌐 Navigating to {url}")
        driver.get(url)

        time.sleep(5)
        print("⏳ Waited 5 seconds for page to load")

        page_source = driver.page_source

        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        driver.save_screenshot("screenshot.png")
        print("📸 Screenshot saved as screenshot.png")

        if "Just a moment..." in page_source or "cf-browser-verification" in page_source:
            print("⚠️ Possible Cloudflare bot protection")
        if "captcha" in page_source.lower():
            print("⚠️ CAPTCHA detected in page content!")

        soup = BeautifulSoup(page_source, 'html.parser')

        for tag in soup(['script', 'style']):
            tag.decompose()

        driver.quit()
        print("✅ WebDriver quit successfully")

        results = []
        header = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3'] and 'List of All AWS Services' in tag.text)
        container = header.find_next_sibling() if header else soup

        for p in container.find_all('p'):
            strong_tag = p.find('strong')
            if strong_tag:
                category_name = strong_tag.get_text(strip=True)
                ol = p.find_next_sibling('ol')
                if ol:
                    for li in ol.find_all('li'):
                        strong = li.find('strong')
                        if strong:
                            name = strong.get_text(strip=True).rstrip(":")
                            description = li.get_text(strip=True).replace(name + ":", "").strip()
                            results.append({
                                "category": category_name,
                                "name": name,
                                "description": description
                            })

        print(f"✅ Scraped {len(results)} AWS services")
        return results

    except Exception as e:
        print("❌ Exception occurred:")
        traceback.print_exc()
        return []
