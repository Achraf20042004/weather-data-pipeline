FROM apache/airflow:2.9.3

# dbt dans un virtualenv separe pour eviter les conflits de dependances avec Airflow
RUN python -m venv /home/airflow/dbt_venv \
    && /home/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-postgres==1.9.0
