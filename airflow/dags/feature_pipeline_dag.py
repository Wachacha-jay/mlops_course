from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.feature_engineering import generate_features
from scripts.split_data import split_data
from scripts.log_dataset_metadata import log_dataset_metadata

with DAG(
    dag_id="walmart_feature_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    features = PythonOperator(
        task_id="feature_engineering",
        python_callable=generate_features,
    )

    split = PythonOperator(
        task_id="time_based_split",
        python_callable=split_data,
    )

    log_meta = PythonOperator(
        task_id="log_dataset_metadata",
        python_callable=log_dataset_metadata,
    )

    features >> split >> log_meta
