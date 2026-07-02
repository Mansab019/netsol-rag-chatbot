import requests
from bs4 import BeautifulSoup


pages = {
    "homepage": "https://netsoltech.com/en-us",
    "cloud_services": "https://netsoltech.com/services/cloud-services",
    "emerging_tech": "https://netsoltech.com/services/emerging-technologies",
    "information_security": "https://netsoltech.com/services/information-security",
    "company_info": "https://ir.netsoltech.com/company-information",
}

def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        print(f"Failed to fetch {url} - status {response.status_code}")
        return None
    
    return response.text

def extract_text(html):
    soap = BeautifulSoup(html, 'html.parser')
    # Remove script and style elements
    for script_or_style in soap(['script', 'style']):
        script_or_style.decompose()
    # Get text
    text = soap.get_text(separator=' ')
    # Collapse whitespace
    text = ' '.join(text.split())
    return text     
                
                
def scrape_and_save(pages):
    for name, url in pages.items():
        html = fetch_page(url)
        if html:
            text = extract_text(html)
            with open(f"data/raw/{name}.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved: {name}")
        else:
            print(f"Skipped (failed fetch): {name}")
            
            
