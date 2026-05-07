import os
import sys
import time
import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_output_directory(directory="output"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def init_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    return driver

def fetch_page(driver, url, wait_time=5):
    driver.get(url)
    time.sleep(wait_time)
    html = driver.page_source
    return html

def extract_scripts(soup, base_url):
    scripts = soup.find_all("script")
    inline_scripts = []
    external_script_urls = []
    
    for script in scripts:
        if script.has_attr("src"):
            src = urljoin(base_url, script["src"])
            external_script_urls.append(src)
        else:
            inline_scripts.append(script.string or "")
    return scripts, inline_scripts, external_script_urls

def fetch_external_scripts(script_urls):
    """Fetch external JavaScript code given a list of URLs."""
    external_scripts = {}
    for src_url in script_urls:
        try:
            r = requests.get(src_url, timeout=10)
            if r.status_code == 200:
                external_scripts[src_url] = r.text
            else:
                external_scripts[src_url] = f"Failed to load script, status code: {r.status_code}"
        except Exception as e:
            external_scripts[src_url] = f"Error fetching script: {e}"
    return external_scripts

def save_full_data(html, inline_scripts, external_scripts, url, output_dir):
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    filename = f"{domain}_fulldata.txt"
    output_path = os.path.join(output_dir, filename)

    data_parts = []
    data_parts.append("=== HTML CODE ===")
    data_parts.append(html)
    
    data_parts.append("\n\n=== Inline JS CODE ===")
    for idx, js in enumerate(inline_scripts, start=1):
        data_parts.append(f"\n--- Inline Script {idx} ---\n")
        data_parts.append(js)
        
    data_parts.append("\n\n=== External JS CODE ===")
    for src_url, js_code in external_scripts.items():
        data_parts.append(f"\n--- External Script from {src_url} ---\n")
        data_parts.append(js_code)
        
    full_data = "\n".join(data_parts)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_data)
    
    return output_path

def scan_for_api_endpoints(content):
    api_pattern = re.compile(r"(https?://[^\s'\"<>]+api[^\s'\"<>]*)", re.IGNORECASE)
    return set(api_pattern.findall(content))

def print_dom_tree(element, indent=0):
    if isinstance(element, Tag):
        print("  " * indent + f"<{element.name}>")
        for child in element.children:
            if isinstance(child, Tag):
                print_dom_tree(child, indent + 1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python collect.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    
    output_dir = setup_output_directory("output")

    print("[*] Initializing headless browser...")
    driver = init_webdriver()

    try:
        print(f"[*] Fetching page: {url}")
        html = fetch_page(driver, url)
    except Exception as e:
        print(f"[!] Error fetching the page: {e}")
        driver.quit()
        sys.exit(1)
    finally:
        driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    page_title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

    scripts, inline_scripts, external_script_urls = extract_scripts(soup, url)
    print(f"[*] Total <script> tags found: {len(scripts)}")
    print(f"[*] Inline scripts: {len(inline_scripts)}")
    print(f"[*] External script URLs: {len(external_script_urls)}")
    
    print("[*] Fetching external JavaScript files...")
    external_scripts = fetch_external_scripts(external_script_urls)

    output_path = save_full_data(html, inline_scripts, external_scripts, url, output_dir)
    print(f"[*] All HTML and JavaScript data saved to: {output_path}")

    print("\n=== Site Information ===")
    print(f"URL: {url}")
    print(f"Title: {page_title}")
    print(f"Total scripts: {len(scripts)}")
    print(f"  Inline: {len(inline_scripts)}")
    print(f"  External: {len(external_script_urls)}")

    print("\n=== HTML DOM Tree Structure ===")
    if soup.html:
        print_dom_tree(soup.html)
    else:
        print_dom_tree(soup)
    combined_content = "\n".join([html] + inline_scripts + list(external_scripts.values()))
    api_endpoints = scan_for_api_endpoints(combined_content)
    
    print("\n=== Potential API Endpoints Found ===")
    if api_endpoints:
        for endpoint in api_endpoints:
            print(endpoint)
    else:
        print("No potential API endpoints detected (based on a simple pattern match).")

if __name__ == "__main__":
    main()
