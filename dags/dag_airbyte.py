from airflow.decorators import dag, task
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.models import Variable
import json
from datetime import datetime

AIRBYTE_CONNECTION_ID = Variable.get('AIRBYTE_GOOGLE_POSTGRES_CONNECTION_ID')
AIRBYTE_API_KEY = f'Bearer {Variable.get("AIRBYTE_API_TOKEN")}'

@dag(
    start_date=datetime(2024,6,5), 
    schedule_interval='@daily', 
    catchup=False
)
def running_airbyte():
    start_airbyte_sync = SimpleHttpOperator(
        task_id = 'start_airbyte_sync',
        http_conn_id = 'airbyte',
        endpoint = f'/v1/jobs',
        method = 'POST',
        headers = {
            "Content-Type":"application/json",
            "User-Agent": "fake-useragent",
            "Accept": "application/json",
            "Authorization": AIRBYTE_API_KEY
        },
        data = json.dumps({"connectionId":AIRBYTE_CONNECTION_ID, "jobType":"sync"}),
        response_check =lambda response: response.json()['status'] == 'running'
    )

    start_airbyte_sync

running_airbyte()