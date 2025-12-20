from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from scripts.validate_features import validate_features
from scripts.train_baseline import train_baseline
from scripts.evaluate_model import evaluate_model
from scripts.register_model import register_model

with DAG(
    dag_id="walmart_training_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    validate = PythonOperator(
        task_id="validate_features",
        python_callable=validate_features,
    )

    train = PythonOperator(
        task_id="train_baseline_model",
        python_callable=train_baseline,
    )

    evaluate = PythonOperator(
        task_id="evaluate_on_test",
        python_callable=evaluate_model,
    )

    register = PythonOperator(
        task_id="register_model",
        python_callable=register_model,
    )

    validate >> train >> evaluate >> register
