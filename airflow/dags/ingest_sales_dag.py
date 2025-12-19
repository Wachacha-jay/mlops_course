from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.download_data import download_data
from scripts.validate_data import validate_data
from scripts.persist_data import persist_validated_data

default_args = {
    "owner": "mlops",
    "retries": 1,
}

with DAG(
    dag_id="walmart_sales_ingestion",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
) as dag:

    ingest = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=download_data,
    )

    validate = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data,
    )

    persist = PythonOperator(
        task_id="persist_validated_data",
        python_callable=persist_validated_data,
    )

    ingest >> validate >> persist
