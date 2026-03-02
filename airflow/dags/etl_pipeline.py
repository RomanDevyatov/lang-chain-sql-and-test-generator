from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from genaidrivenetl.pipeline import run_main_pipeline  # твой LangChain ETL

def run_etl_task():
    run_main_pipeline()

with DAG(
    dag_id="genai_etl",
    start_date=datetime(2026, 2, 27),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    etl = PythonOperator(
        task_id="run_etl",
        python_callable=run_etl_task,
    )
