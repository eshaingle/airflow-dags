import os
from os import environ
import json
from airflow import DAG
from airflow.models import Variable
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.hooks.base_hook import BaseHook
from airflow.providers.hashicorp.secrets.vault import VaultBackend

os.environ['AIRFLOW__SECRETS__BACKEND'] = "airflow.providers.hashicorp.secrets.vault.VaultBackend"
os.environ['AIRFLOW__SECRETS__BACKEND_KWARGS'] = '{"connections_path": "message", "auth_mount_point": "kubernetes", "mount_point": "kv", "auth_type": "kubernetes", "kubernetes_role": "example", "kubernetes_jwt_path":"/var/run/secrets/kubernetes.io/serviceaccount/token", "url": "http://vault.default.svc:8200"}'

def get_secrets(**kwargs):
    conn = BaseHook.get_connection(kwargs['my_conn_id'])
    print("Password:", {conn.password} )
    print(" Login:", {conn.login} )
    print(" URI:", {conn.get_uri()} )
    print("Host:", {conn.host})


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
                                arguments=["apk add curl && curl --request POST \
        	--data '{"'"jwt"'": "'"eyJhbGciOiJSUzI1NiIsImtpZCI6Imh3T0U2QXNSVjVHUzlySG0tVDh5U0k5eVNSeEJWLUN0SzJYcFVrVEtYek0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6InZhdWx0LWF1dGgtdG9rZW4tODJmY2YiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidmF1bHQtYXV0aCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImIxMWU1ZDdjLTMxZjQtNDFlMi1hM2MzLWY1MDI4ZWRhZWE4NCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OnZhdWx0LWF1dGgifQ.TIO1gsY47wdsJVCksdFFlypsJ4SY0vSCmnUWkoqNseI4zlp3tR5y1xnSko_6gM9kF8tenfVvhf-oTkSecaFFzmVTlhA4YJopMAHUH7bdXM_UgrFFyv2hKx6ZwZrW6H5T-GZ0gsyUbxfsxqFc12-Qvh5mNN5g7XcgFbBdWcdwVUucmhwIVSf5xH3hpQljus1R4x0lOd-xvGqZwB6NEFpj6CepA1kLWVh6V_YxdSxTDzdBlPoaG04a8WNybvn0rvlUjQ6pNGPv0uEDpnKNgiL8zJkWr3FaAId7gvPALhHjGIWpmp1VIfqmchscKqZZBEaqhKKs06pmWhWZTRA9DK19UA"'", "'"role"'": "'"example"'"}' \
        	http://vault:8200/v1/auth/kubernetes/login "],
                                labels={"test-airflow": "firstversion"},
                                name="passing-test",
                                task_id="passing-task",
				get_logs=True,
                                dag=dag
                                )
