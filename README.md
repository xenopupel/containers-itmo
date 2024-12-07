# Good
## Сборка

docker build -t airflow_good -f .\good.Dockerfile .

## Запуск

docker run -d \
     -v "D:/Vscode_projects/Containers/containers-itmo/dags:/opt/airflow/dags" \ 
     -v "D:/Vscode_projects/Containers/airflow-logs:/opt/airflow/logs" \ 
     -v "D:/Vscode_projects/Containers/temperatures:/opt/airflow/temperatures" \ 
     -e WEATHER_API_KEY="58ef808c914a66e0e00be58843f0d251" \ 
     -p 5000:8080 \ 
     airflow_good
