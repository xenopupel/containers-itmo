# Плохая практика: полный жирный образ
FROM python:3.11

# Плохая практика: Все команды выполняются от имени пользователя root
USER root

# Плохая практика: отсутствие минимизации слоев и кеширования, что увеличивает объем образа
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim nano wget

COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Плохая практика: отсутствие установки HEALTHCHECK
# Это может помешать мониторингу состояния контейнера

COPY entrypoint.sh /entrypoint.sh

VOLUME ["/opt/airflow/dags", "/opt/airflow/logs", "/opt/airflow/temperatures"]

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
