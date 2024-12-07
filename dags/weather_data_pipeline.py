import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

API_KEY = os.getenv('WEATHER_API_KEY', 'default_key')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_weather_data():
    api_key = API_KEY
    city = "Новосибирск"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    with open('/opt/airflow/temperatures/weather_data.json', 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Weather data for {city} saved successfully!")

with DAG(
    'weather_data_pipeline',
    default_args=default_args,
    description='Pipeline для сбора данных о погоде',
    schedule=timedelta(days=1),
    start_date=datetime(2024, 12, 7),
    catchup=False,
) as dag:

    fetch_weather_task = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=fetch_weather_data,
    )

    fetch_weather_task