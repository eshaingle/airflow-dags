import os
from os import environ
import json
from airflow import DAG
from airflow.models import Variable
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.hooks.base_hook import BaseHook

os.environ['AIRFLOW__SECRETS__BACKEND'] = "airflow.contrib.secrets.hashicorp_vault.VaultBackend"
os.environ['AIRFLOW__SECRETS__BACKEND_KWARGS'] = '{"connections_path": "myapp", "mount_point": "secret", "auth_type": "kubernetes", "kubernetes_role": "example", "kubernetes_jwt_path":"/var/run/secrets/kubernetes.io/serviceaccount/token", "url": "http://192.168.49.1:8200"}'

def get_secrets(**kwargs):
    conn = BaseHook.get_connection(kwargs['my_conn_id'])
    print("Password:", {conn.password} )
    print(" Login:", {conn.username} )
    print("Url:", {environ.get("CLIENT_TOKEN")})


dag = DAG(
    'vaulttoken_k8s', start_date=datetime(2020, 1, 1), schedule_interval=None)

test_task = PythonOperator(
    task_id='test-vault',
    python_callable=get_secrets,
    op_kwargs={'my_conn_id': 'config'},
    dag=dag)

passing = KubernetesPodOperator(namespace='default',
				service_account_name="vault-auth",
                                image="alpine:3.7",
                                cmds=["sh", "-cx"],
                                arguments=["apk add curl jq && curl --request POST \
        	--data '{"'"jwt"'": "'$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)'", "'"role"'": "'"example"'"}' \
        	http://192.168.49.1:8200/v1/auth/kubernetes/login "],
                                labels={"test-airflow": "firstversion"},
                                name="passing-test",
                                task_id="passing-task",
				get_logs=True,
                                dag=dag
                                )
