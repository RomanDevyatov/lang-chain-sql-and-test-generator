from datetime import datetime

from airflow.operators.python import PythonOperator

from airflow import DAG
from app.genaidrivenetl.main import run_pipeline

def run_etl_task():
    run_pipeline()

with DAG(
    dag_id="genai_etl",
    start_date=datetime(2026, 2, 27),
    schedule="@daily",
    catchup=False
) as dag:

    etl = PythonOperator(
        task_id="run_etl",
        python_callable=run_etl_task
    )

