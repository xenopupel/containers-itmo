FROM apache/airflow:slim-2.10.3-python3.11

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl dos2unix && apt-get clean

COPY requirements.txt /opt/airflow/requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh && dos2unix /entrypoint.sh

USER airflow

RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

VOLUME ["/opt/airflow/dags", "/opt/airflow/logs", "/opt/airflow/temperatures"]

EXPOSE 8080
