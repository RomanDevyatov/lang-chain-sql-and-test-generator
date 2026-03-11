from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from genaidrivenetl.main import run_pipeline
from airflow.sdk.definitions.template import literal

with DAG(
    dag_id="generate_sql_and_test",
    start_date=datetime(2026, 2, 27),
    schedule="@daily",
    catchup=False
) as dag:

    # -----------------------------
    # Python ETL pipeline
    # -----------------------------

    gen_sql_and_test = PythonOperator(
        task_id="run_etl",
        python_callable=run_pipeline
    )

    # -----------------------------
    # Bash scripts
    # -----------------------------
    
    init_db = BashOperator(
        task_id="init_db",
        bash_command=literal("/opt/airflow/scripts/init_db.sh")
    )

    # run_generated_tests = BashOperator(
    #     task_id="run_generated_tests",
    #     bash_command=literal("/opt/airflow/scripts/run_generated_tests.sh")
    # )

    stage_to_prod = BashOperator(
        task_id="stage_to_prod",
        bash_command=literal("/opt/airflow/scripts/run_commit_views.sh")
    )

    run_lint = BashOperator(
        task_id="run_lint",
        bash_command=literal("/opt/airflow/scripts/run_lint.sh")
    )

    init_db >> gen_sql_and_test >> stage_to_prod >> run_lint
