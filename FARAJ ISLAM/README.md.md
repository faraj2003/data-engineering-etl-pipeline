# **Data Engineer Intern – Website Content Pipeline**



### **Project Overview**



This project implements an end-to-end data pipeline to crawl websites, extract and structure content, standardize it, and compute aggregated metrics. The pipeline is designed to be reliable, repeatable, and scalable, orchestrated using Apache Airflow.



##### **The pipeline covers:**



* Website Crawling \& Raw Data Capture



* Content Extraction \& Tagging



* Standardized Data Model Transformation



* Aggregation \& Metrics Computation



* Orchestration via Airflow DAG



#### **Folder Structure:**



data-engineer-intern-task/

│

├── dags/

│   └── website\_content\_pipeline.py    # Airflow DAG

│

├── src/

│   ├── crawler/

│   │   └── crawler.py

│   ├── extractor/

│   │   └── content\_extractor.py

│   ├── transformer/

│   │   └── standardize.py

│   ├── aggregator/

│   │   └── metrics.py

│   └── utils/

│       └── logger.py

│

├── data/

│   ├── raw/                           # Raw HTML + metadata

│   ├── processed/                     # Extracted and tagged content

│   ├── standardized/                  # JSON per website

│   └── aggregates/                    # metrics.json

│

├── README.md

└── requirements.txt



#### **Pipeline Steps**



###### **Step 1 – Crawl Websites**



* Crawls multiple company websites (5–10)



* Captures homepage, navbar, footer, case studies, and internal pages



* Stores raw HTML + metadata in data/raw/<website>/



* Logs HTTP status, URL, and crawl timestamp



###### **Step 2 – Extract \& Tag Content**



* Extracts readable text from HTML using BeautifulSoup



* Categorizes into homepage, navbar, footer, case\_study



* Cleans content by removing scripts and styles



* Stores JSON files per section in data/processed/<website>/



###### **Step 3 – Standardize Data**



* Combines all sections into a standardized JSON record per website



Example schema:



{

&nbsp; "website": "https://example.com",

&nbsp; "section": "case\_study",

&nbsp; "content": "Extracted text...",

&nbsp; "crawl\_timestamp": "2026-01-10T10:30:00Z",

&nbsp; "isActive": true

}





* Stored in data/standardized/<website>.json



###### **Step 4 – Aggregation \& Metrics**



Computes:



* Number of websites with case studies



* Active vs inactive websites



* Content length statistics per section



* Aggregated output stored in data/aggregates/metrics.json



###### **Step 5 – Airflow DAG**



DAG: website\_content\_pipeline.py orchestrates all steps:



crawl\_websites → extract\_content → standardize\_data → compute\_metrics





**DAG features:**



* Clear task separation



* Idempotent and retryable tasks



* Easy to extend to more websites or sections







### **Logging \& Error Handling**



* Each module uses a logger for info, warnings, and errors



* Missing HTML files or empty sections are handled gracefully



* Tasks are idempotent — reruns overwrite previous outputs safely





### **Scaling Considerations**



* Adding more websites only requires updating the websites list in crawler.py



* Modular design allows adding new extraction rules, sections, or analytics easily



* Can be extended to cloud storage (S3) for raw/processed/standardized data





### **How to Run**



* Install dependencies:



pip install -r requirements.txt





* Run modules manually (optional):



python src/crawler/crawler.py

python src/extractor/content\_extractor.py

python src/transformer/standardize.py

python src/aggregator/metrics.py





#### **Airflow DAG :**



* DAG is included in dags/website\_content\_pipeline.py



* Can be run in Airflow by placing in the DAG folder and triggering manually





### **Deliverables**



* dags/website\_content\_pipeline.py → Airflow DAG



* src/ → Python modules for crawling, extraction, transformation, and metrics



* data/ → Sample raw, processed, standardized, and aggregated outputs



* README.md → This file explaining design decisions and pipeline workflow
