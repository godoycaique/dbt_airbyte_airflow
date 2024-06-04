from airflow.decorators import dag, task
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook, DbtCloudJobRunStatus
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from datetime import datetime


DBT_CLOUD_CONN_ID = 'dbt-connection'
JOB_ID = '650808'

@dag(
    start_date=datetime(2024,6,4),
    schedule='@daily',
    catchup=False
)

def running_dbt_cloud():

    rodar_dbt = DbtCloudRunJobOperator(
        task_id = 'rodardbt',
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        job_id = JOB_ID,
        check_interval=60,
        timeout=360
    )
    
running_dbt_cloud()