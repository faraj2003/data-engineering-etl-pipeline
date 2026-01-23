import sys
from pathlib import Path
import json
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.logger import setup_logger

logger = setup_logger("extractor_logger")

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")

def extract_text_from_html(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)

def get_crawl_timestamp(website_folder, section):
    metadata_file = website_folder / "metadata.json"
    if metadata_file.exists():
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            for item in metadata:
                if item.get("section") == section:
                    return item.get("crawl_timestamp", "")
    return ""

def process_website(website_folder):
    website_name = website_folder.name
    processed_website_folder = PROCESSED_FOLDER / website_name
    processed_website_folder.mkdir(parents=True, exist_ok=True)

    sections = ["homepage", "navbar", "footer", "case_study"]
    for section in sections:
        html_file = website_folder / f"{section}.html"
        content = ""
        if html_file.exists():
            with open(html_file, "r", encoding="utf-8") as f:
                html_content = f.read()
                content = extract_text_from_html(html_content)
        else:
            logger.warning(f"{section}.html not found for {website_name}")
        
        crawl_timestamp = get_crawl_timestamp(website_folder, section)

        output = {
            "website": f"https://{website_name}",
            "section": section,
            "content": content,
            "crawl_timestamp": crawl_timestamp,
            "isActive": bool(content)
        }

        output_file = processed_website_folder / f"{section}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)
        
        logger.info(f"Processed {section} for {website_name}")

def process_all_websites():
    if not RAW_FOLDER.exists():
        logger.error(f"Raw folder {RAW_FOLDER} does not exist!")
        return

    for website_folder in RAW_FOLDER.iterdir():
        if website_folder.is_dir():
            logger.info(f"Processing website: {website_folder.name}")
            process_website(website_folder)

if __name__ == "__main__":
    process_all_websites()
