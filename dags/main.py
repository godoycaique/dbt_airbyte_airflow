from time import sleep

from airflow.decorators import dag, task
from datetime import datetime



@dag(
        dag_id='dag_teste',
        description='meu teste',
        schedule='* * * 1 *',
        start_date=datetime(2024,6,4),
        catchup=False
)
def pipeline():
    @task
    def primeira():
        print('primeira')
        sleep(2)

    @task
    def segunda():
        print('segunda')
        sleep(2)

    @task
    def terceira():
        print('terceira')
        sleep(2)

    t1 = primeira()
    t2 = segunda()
    t3 = terceira()

    t1 >> t2 >> t3

pipeline()