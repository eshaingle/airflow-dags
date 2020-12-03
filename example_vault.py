import os
from os import environ
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.hooks.base_hook import BaseHook

os.environ['AIRFLOW__SECRETS__BACKEND'] = "airflow.providers.hashicorp.secrets.vault.VaultBackend"
os.environ['AIRFLOW__SECRETS__BACKEND_KWARGS'] = '{"connections_path": "myapp", "mount_point": "secret", "auth_type": "token", "token": "s.syjqsHYKDG0zmCE6YkUyGCIy", "url": "http://vault:8200"}'

def get_secrets(**kwargs):
    conn = BaseHook.get_connection(kwargs['my_conn_id'])
    print("Password:", {conn.password} )
    print("password:", {conn.username} )

with DAG('vault_example', start_date=datetime(2020, 1, 1), schedule_interval=None) as dag:

    test_task = PythonOperator(
        task_id='test-task',
        python_callable=get_secrets,
        op_kwargs={'my_conn_id': 'test_data'},
    )
