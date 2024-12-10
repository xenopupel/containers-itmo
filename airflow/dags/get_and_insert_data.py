from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2
import os

POSTGRES_CONN = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
}
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_ingestion',
    default_args=default_args,
    description='Получить данные из FastAPI и положить в Postgres',
    schedule_interval=timedelta(seconds=10),
    start_date=datetime(2024, 12, 1),
    catchup=False,
)

def fetch_data():
    response = requests.get("http://data-service:8000/data")
    response.raise_for_status()
    data = response.json()
    return data

def store_data(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='fetch_data')

    connection = psycopg2.connect(**POSTGRES_CONN)
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO data_table (id, name, value, timestamp) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (data['id'], data['name'], data['value'], data['timestamp']))
    connection.commit()
    cursor.close()
    connection.close()

fetch_data_task = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    dag=dag,
)

store_data_task = PythonOperator(
    task_id='store_data',
    python_callable=store_data,
    provide_context=True,
    dag=dag,
)

fetch_data_task >> store_data_task
