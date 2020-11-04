from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.hooks.base_hook import BaseHook


def get_secrets(**kwargs):
    conn = BaseHook.get_connection(kwargs['my_conn_id'])
    print("Password:", {conn.password} )
    print(" Login:", {conn.login} )
    print(" URI:", {conn.get_uri()} )
    print("Host:", {conn.host})

with DAG('vault_example', start_date=datetime(2020, 1, 1), schedule_interval=None) as dag:


    test_task = PythonOperator(
        task_id='test-task',
        python_callable=get_secrets,
        op_kwargs={'my_conn_id': 'smtp_default'},
    )
