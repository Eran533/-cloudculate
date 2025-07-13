from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_aws_architectures():
    options = Options()
    options.add_argument("--headless")  # Run without UI
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    url = "https://www.netcomlearning.com/blog/aws-service-list"
    driver.get(url)

    time.sleep(5)  # Wait for JS to load content

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Clean HTML
    for tag in soup(['script', 'style']):
        tag.decompose()

    driver.quit()

    results = []

    # Find header by text and get next section or container with list
    header = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3'] and 'List of All AWS Services' in tag.text)
    if header:
        container = header.find_next_sibling()
    else:
        container = soup  # fallback to whole page

    # Find all <p> tags with <strong> inside in container
    category_headers = container.find_all('p')

    for p in category_headers:
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
