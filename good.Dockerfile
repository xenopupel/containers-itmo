FROM apache/airflow:slim-2.10.3-python3.11

USER root

RUN apt-get update && apt-get install -y --no-install-recommends curl && apt-get clean

USER airflow

COPY requirements.txt /opt/airflow/requirements.txt

COPY entrypoint.sh /entrypoint.sh

RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

VOLUME ["/opt/airflow/dags", "/opt/airflow/logs", "/opt/airflow/temperatures"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
CMD curl --fail http://localhost:8080/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
