import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

sys.path.append("/opt/airflow/api-request")

DBT_BIN = "/home/airflow/dbt_venv/bin/dbt"
DBT_DIR = "/opt/airflow/dbt"


def ingest_weather_data():
    from insert_records import main  # import ici pour ne pas ralentir le parsing du DAG
    main()


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_api_dbt_orchestrator",
    description="Weatherstack API -> PostgreSQL (raw) -> dbt (staging + marts)",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=timedelta(hours=1),
    catchup=False,
    tags=["weather", "dbt"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_data_task",
        python_callable=ingest_weather_data,
    )

    transform = BashOperator(
        task_id="transform_data_task",
        bash_command=f"cd {DBT_DIR}/my_project && {DBT_BIN} build --profiles-dir {DBT_DIR}",
    )

    ingest >> transform
