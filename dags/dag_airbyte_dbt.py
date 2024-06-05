from airflow.decorators import dag, task
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook, DbtCloudJobRunStatus
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from datetime import datetime
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.models import Variable
import json
from time import sleep


DBT_CLOUD_CONN_ID = 'dbt-connection'
DBT_JOB_ID = '70403103937984'
AIRBYTE_CONNECTION_ID = Variable.get('AIRBYTE_GOOGLE_POSTGRES_CONNECTION_ID')
AIRBYTE_API_KEY = f'Bearer {Variable.get("AIRBYTE_API_TOKEN")}'


@dag(
    start_date=datetime(2024,6,4),
    schedule='@daily',
    catchup=False
)

def running_airbyte_dbt():

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

    @task
    def operador_http_sensor():
        sleep(120)

    start_dbt = DbtCloudRunJobOperator(
        task_id = 'rodardbt',
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        job_id = DBT_JOB_ID,
        check_interval=60,
        timeout=360
    )
    
    http_sensor = operador_http_sensor()
    start_airbyte_sync >> http_sensor >> start_dbt

running_airbyte_dbt()