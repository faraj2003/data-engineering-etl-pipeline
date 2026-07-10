# Data Engineering ETL Pipeline

## Overview

This repository contains a modular Extract, Transform, Load (ETL) pipeline designed to collect, process, standardize, and analyze website content from multiple e-commerce platforms. The pipeline is orchestrated using Apache Airflow, enabling automated execution of each stage while maintaining clear task dependencies.

The project demonstrates core data engineering principles including modular pipeline design, workflow orchestration, structured data processing, centralized logging, and analytics generation.

## Features

* Modular ETL pipeline architecture
* Apache Airflow workflow orchestration
* Automated web crawling with retry mechanism
* HTML content extraction using BeautifulSoup
* Data standardization into a unified JSON schema
* Aggregated metrics generation
* Centralized logging across pipeline stages

## Architecture

The pipeline follows a staged ETL architecture where each module performs a single responsibility.

```text
            Apache Airflow
                   │
                   ▼
            Website Crawler
                   │
                   ▼
          Content Extractor
                   │
                   ▼
      Data Standardization
                   │
                   ▼
        Metrics Aggregator

```

Each stage produces intermediate outputs which become the input for the next stage, making the pipeline easy to debug, maintain, and extend.

## Pipeline Stages

### 1. Crawl

**Location**

`src/crawler/crawler.py`

The crawler is responsible for collecting raw HTML content from the configured target websites.
Its responsibilities include:

* Sending HTTP requests
* Managing retry attempts for failed requests
* Downloading webpage content
* Capturing crawl timestamps
* Saving raw HTML for downstream processing

The crawler acts as the ingestion layer of the ETL pipeline.

### 2. Extract

**Location**

`src/extractor/content_extractor.py`

The extractor parses the downloaded HTML using BeautifulSoup and extracts relevant website components.
Examples include:

* Navigation content
* Homepage content
* Footer content
* Additional structured webpage sections

The extracted content is converted into structured JSON along with metadata such as:

* Website name
* Section name
* Crawl timestamp
* Activity status

This stage converts unstructured HTML into structured data suitable for transformation.

### 3. Transform

**Location**

`src/transformer/standardize.py`

The transformation stage standardizes the extracted data into a consistent schema.
Key responsibilities include:

* Combining extracted sections
* Enforcing a common JSON structure
* Inserting default values for unavailable sections
* Preparing clean datasets for downstream analytics

This stage ensures every processed website follows the same data format regardless of differences in the source HTML.

### 4. Aggregate

**Location**

`src/aggregator/metrics.py`

The aggregation stage generates summary statistics from the standardized datasets.
Example metrics include:

* Total websites processed
* Active websites
* Websites containing case-study information
* Content length statistics
* Pipeline summary metrics

The generated metrics can be consumed by reporting or downstream analytical workflows.

## Workflow Orchestration

The entire ETL pipeline is orchestrated using Apache Airflow.

**DAG Location**

`dags/website_content_pipeline.py`

The DAG defines the execution order of the pipeline:

```text
Crawler
      │
      ▼
Extractor
      │
      ▼
Transformer
      │
      ▼
Aggregator

```

Airflow manages:

* Task scheduling
* Task dependencies
* Retry policies
* Execution monitoring
* Centralized logging

This separation between orchestration and business logic improves maintainability and scalability.

## Project Structure

```text
data-engineering-etl-pipeline/
│
├── dags/
│   └── website_content_pipeline.py
│
├── src/
│   ├── crawler/
│   │   └── crawler.py
│   │
│   ├── extractor/
│   │   └── content_extractor.py
│   │
│   ├── transformer/
│   │   └── standardize.py
│   │
│   ├── aggregator/
│   │   └── metrics.py
│   │
│   └── utils/
│       └── logger.py
│
├── requirements.txt
├── dag_diagram.txt
└── README.md

```

## Logging

The project includes a centralized logging utility located in:

`src/utils/logger.py`

Logging is used throughout the pipeline to record:

* Pipeline execution progress
* Successful task completion
* Retry attempts
* Runtime errors
* Debug information

Centralized logging simplifies troubleshooting and monitoring during pipeline execution.

## Technologies Used

* Python
* Apache Airflow
* BeautifulSoup4
* Requests
* JSON
* Logging

## Installation

**Clone the repository**

```bash
git clone https://github.com/faraj2003/data-engineering-etl-pipeline.git
cd data-engineering-etl-pipeline

```

**Create a virtual environment**

```bash
python -m venv venv

```

**Windows**

```cmd
venv\Scripts\activate

```

**Linux/macOS**

```bash
source venv/bin/activate

```

**Install dependencies**

```bash
pip install -r requirements.txt

```

**Configure Apache Airflow**

Place the DAG inside your Airflow DAG directory or create a symbolic link.
Example:

```bash
ln -s /path/to/project/dags/website_content_pipeline.py ~/airflow/dags/

```

Start Airflow services:

```bash
airflow scheduler
airflow webserver -p 8080

```

Open:

`http://localhost:8080`

Locate `website_content_pipeline`, enable the DAG, and trigger a run.

## Pipeline Output

During execution, the pipeline produces multiple intermediate outputs that correspond to each ETL stage.

```text
Target Websites
        │
        ▼
    Raw HTML
        │
        ▼
Structured JSON
        │
        ▼
Standardized Dataset
        │
        ▼
Business Metrics

```

This layered processing approach makes debugging easier while maintaining a clear separation of responsibilities between pipeline stages.

### Example Standardized Output

```json
{
  "website": "amazon.in",
  "section": "homepage",
  "content": "...",
  "crawl_timestamp": "2026-07-10T10:25:00",
  "isActive": true
}

```

## Future Improvements

Potential enhancements include:

* Load standardized data into a relational database (PostgreSQL/MySQL)
* Integrating cloud object storage such as Amazon S3
* Adding automated data quality validation checks
* Containerizing the pipeline using Docker
* Implementing CI/CD for automated testing and deployment
* Extending Airflow scheduling for production workloads

## Author

Faraj Islam
