from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from crawler.crawler import crawl_websites
from extractor.content_extractor import process_all_websites as extract_content
from transformer.standardize import standardize_all_websites
from aggregator.metrics import compute_metrics

default_args = {
    "owner": "faraj",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    "website_content_pipeline",
    default_args=default_args,
    description="End-to-end website content pipeline",
    schedule_interval=None,
    start_date=datetime(2026, 1, 19),
    catchup=False,
    tags=["data-engineer-intern"],
) as dag:

    crawl_task = PythonOperator(
        task_id="crawl_websites",
        python_callable=crawl_websites,
    )

    extract_task = PythonOperator(
        task_id="extract_content",
        python_callable=extract_content,
    )

    standardize_task = PythonOperator(
        task_id="standardize_data",
        python_callable=standardize_all_websites,
    )

    metrics_task = PythonOperator(
        task_id="compute_metrics",
        python_callable=compute_metrics,
    )

    crawl_task >> extract_task >> standardize_task >> metrics_task
