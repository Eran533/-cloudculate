from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time

def scrape_aws_architectures():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Use env variables you set in the Dockerfile
    options.binary_location = os.getenv("CHROME_BIN", "/usr/bin/google-chrome")
    service = Service(os.getenv("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver"))

    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.netcomlearning.com/blog/aws-service-list"
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for tag in soup(['script', 'style']):
        tag.decompose()

    driver.quit()

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
