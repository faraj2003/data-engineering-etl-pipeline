import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.logger import setup_logger

logger = setup_logger("metrics_logger")

STANDARDIZED_FOLDER = Path("data/standardized")
AGGREGATES_FOLDER = Path("data/aggregates")
AGGREGATES_FOLDER.mkdir(parents=True, exist_ok=True)

def compute_metrics():
    metrics = {
        "total_websites": 0,
        "websites_with_case_study": 0,
        "active_websites": 0,
        "inactive_websites": 0,
        "content_length_stats": {
            "homepage": {"min": None, "max": None, "avg": None},
            "navbar": {"min": None, "max": None, "avg": None},
            "footer": {"min": None, "max": None, "avg": None},
            "case_study": {"min": None, "max": None, "avg": None}
        }
    }

    content_lengths = {"homepage": [], "navbar": [], "footer": [], "case_study": []}

    for file in STANDARDIZED_FOLDER.iterdir():
        if file.suffix != ".json":
            continue
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            metrics["total_websites"] += 1

            website_active = False
            case_study_present = False

            for section in data:
                name = section["section"]
                content_len = len(section["content"])
                content_lengths[name].append(content_len)
                if section["isActive"]:
                    website_active = True
                if name == "case_study" and section["isActive"]:
                    case_study_present = True
            
            if website_active:
                metrics["active_websites"] += 1
            else:
                metrics["inactive_websites"] += 1
            if case_study_present:
                metrics["websites_with_case_study"] += 1

    for section, lengths in content_lengths.items():
        if lengths:
            metrics["content_length_stats"][section]["min"] = min(lengths)
            metrics["content_length_stats"][section]["max"] = max(lengths)
            metrics["content_length_stats"][section]["avg"] = sum(lengths) / len(lengths)
        else:
            metrics["content_length_stats"][section]["min"] = 0
            metrics["content_length_stats"][section]["max"] = 0
            metrics["content_length_stats"][section]["avg"] = 0

    metrics_file = AGGREGATES_FOLDER / "metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
    
    logger.info(f"Metrics computed and saved to {metrics_file}")

if __name__ == "__main__":
    compute_metrics()
