import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.logger import setup_logger

logger = setup_logger("standardizer_logger")

PROCESSED_FOLDER = Path("data/processed")
STANDARDIZED_FOLDER = Path("data/standardized")
STANDARDIZED_FOLDER.mkdir(parents=True, exist_ok=True)

def standardize_website(website_folder):
    website_name = website_folder.name
    sections = ["homepage", "navbar", "footer", "case_study"]
    standardized_records = []

    for section in sections:
        section_file = website_folder / f"{section}.json"
        if section_file.exists():
            with open(section_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            logger.warning(f"{section}.json not found for {website_name}")
            data = {
                "website": f"https://{website_name}",
                "section": section,
                "content": "",
                "crawl_timestamp": "",
                "isActive": False
            }
        standardized_records.append(data)
    
    output_file = STANDARDIZED_FOLDER / f"{website_name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(standardized_records, f, indent=4)
    logger.info(f"Standardized data saved for {website_name}")

def standardize_all_websites():
    if not PROCESSED_FOLDER.exists():
        logger.error(f"Processed folder {PROCESSED_FOLDER} does not exist!")
        return
    for website_folder in PROCESSED_FOLDER.iterdir():
        if website_folder.is_dir():
            standardize_website(website_folder)

if __name__ == "__main__":
    standardize_all_websites()
