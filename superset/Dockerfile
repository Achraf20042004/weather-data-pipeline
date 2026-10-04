FROM apache/superset:4.1.1

# driver PostgreSQL (base meteo + metadonnees Superset)
USER root
RUN pip install --no-cache-dir psycopg2-binary
USER superset
