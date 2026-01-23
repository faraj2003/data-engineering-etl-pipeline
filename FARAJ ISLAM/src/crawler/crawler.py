import requests
from pathlib import Path
import json
from datetime import datetime
import time


WEBSITES = [
    "https://amazon.in",
    "https://www.flipkart.com"
]

SECTIONS = ["homepage", "navbar", "footer", "case_study"]

RAW_FOLDER = Path("data/raw")

# -----------------------------
# FUNCTIONS
# -----------------------------
def fetch_url(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.text, resp.status_code
        except:
            time.sleep(delay)
    return None, None

def save_html(website, section, html):
    folder = RAW_FOLDER / website.replace("https://", "").replace("http://", "")
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / f"{section}.html"
    if html:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

def crawl_website(website):
    metadata = []
    for section in SECTIONS:
        if section == "homepage":
            url = website
        elif section == "case_study":
            url = website + "/case-studies"
        else:  # navbar/footer
            url = website
        html, status = fetch_url(url)
        save_html(website, section, html)
        metadata.append({
            "section": section,
            "url": url,
            "status": status if status else "Failed",
            "crawl_timestamp": datetime.utcnow().isoformat() + "Z"
        })
    # Save metadata
    folder = RAW_FOLDER / website.replace("https://", "").replace("http://", "")
    with open(folder / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"Crawled {website}")

def crawl_all_websites():
    for website in WEBSITES:
        crawl_website(website)

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    crawl_all_websites()
