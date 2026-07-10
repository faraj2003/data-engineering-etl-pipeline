
# Data Engineering ETL Pipeline: E-Commerce Scraper & Aggregator

## 📌 Overview

This project is an automated **Extract, Transform, Load (ETL) pipeline** designed to scrape, process, and analyze web data from major e-commerce platforms (specifically **Amazon.in** and **Flipkart.com**).

Orchestrated using **Apache Airflow**, the pipeline crawls raw HTML content from target websites, extracts specific page components (like navbars, footers, and homepages), standardizes the data into a structured JSON format, and computes analytical metrics.

## 🏗️ Architecture & Pipeline Stages

The ETL process is broken down into four primary modular stages:

1. **Crawler (`src/crawler/crawler.py`):** Fetches raw HTML content and metadata from target e-commerce websites and stores them in the `data/raw/` directory.
2. **Extractor (`src/extractor/content_extractor.py`):** Parses the raw HTML to extract specific page elements (navbar, footer, homepage features, and case studies), saving the intermediate results as JSON in `data/processed/`.
3. **Transformer (`src/transformer/standardize.py`):** Cleans and standardizes the extracted JSON data into a unified schema, storing the final output in `data/standardized/`.
4. **Aggregator (`src/aggregator/metrics.py`):** Analyzes the standardized data to generate business or pipeline metrics, outputting to `data/aggregates/metrics.json`.

## 📂 Directory Structure

```text
data-engineering-etl-pipeline/
│
├── dags/                                 # Apache Airflow DAGs
│   └── website_content_pipeline.py       # Main pipeline orchestration script
│
├── data/                                 # Local Data Lake 
│   ├── raw/                              # Stage 1: Raw HTML and metadata
│   │   ├── amazon.in/
│   │   └── www.flipkart.com/
│   ├── processed/                        # Stage 2: Extracted component JSONs
│   │   ├── amazon.in/
│   │   └── www.flipkart.com/
│   ├── standardized/                     # Stage 3: Unified/Cleaned JSON data
│   │   ├── amazon.in.json
│   │   └── www.flipkart.com.json
│   └── aggregates/                       # Stage 4: Computed metrics
│       └── metrics.json
│
├── src/                                  # Source Code Modules
│   ├── crawler/
│   │   └── crawler.py                    # Web scraping logic
│   ├── extractor/
│   │   └── content_extractor.py          # HTML parsing and extraction logic
│   ├── transformer/
│   │   └── standardize.py                # Data transformation and schema enforcement
│   ├── aggregator/
│   │   └── metrics.py                    # Metric calculation logic
│   └── utils/
│       └── logger.py                     # Custom logging configuration
│
├── requirements.txt                      # Python dependencies
├── dag_diagram.txt                       # Visual representation of the Airflow DAG
└── README.md                             # Project documentation

```

## 🚀 Getting Started

### Prerequisites

* **Python 3.8+**
* **Apache Airflow** installed and initialized
* Virtual Environment (recommended)

### Installation & Setup

1. **Clone the repository (or navigate to the project directory):**
```bash
cd data-engineering-etl-pipeline

```


2. **Set up a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure Airflow:**
* Point your `AIRFLOW_HOME` to a desired directory.
* Symlink or copy the `dags/` folder into your Airflow DAGs directory.
* Ensure Airflow has read/write permissions to the `data/` directory.



### Running the Pipeline

1. Start the Airflow webserver and scheduler:
```bash
airflow scheduler &
airflow webserver -p 8080

```


2. Open the Airflow UI (`http://localhost:8080`).
3. Locate the `website_content_pipeline` DAG.
4. Unpause the DAG and trigger it manually to begin the ETL extraction process.

## 📊 Data Flow & Outputs

* **Raw Data:** HTML files (e.g., `footer.html`, `homepage.html`) are saved in `data/raw/<domain>/`.
* **Processed Data:** Parsed JSON files (e.g., `navbar.json`, `footer.json`) are generated in `data/processed/<domain>/`.
* **Standardized Data:** Consolidated JSON payloads are created in `data/standardized/`.
* **Aggregates:** A final `metrics.json` file is produced in `data/aggregates/` containing insights based on the pipeline run.

## 🛠️ Built With

* **Python** - Core programming language
* **Apache Airflow** - Workflow orchestration
* **BeautifulSoup / LXML** (Inferred) - For HTML content extraction
* **JSON** - Standardized data format

## 👤 Author

**Faraj Islam**
