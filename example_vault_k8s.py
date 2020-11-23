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
        	--data '{"'"jwt"'": "'"eyJhbGciOiJSUzI1NiIsImtpZCI6IndjZ3RUNGFwUzVMV1FKNl9YTnZER2c5OUk4c1l6aE9ERzFhOHh0QkdxRVkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6InZhdWx0LWF1dGgtdG9rZW4tN3Z3eHIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidmF1bHQtYXV0aCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjQ5Y2M4MTJkLTQ4MmItNGNmYi05Yzg3LThjMDExYTQyYzMyZSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OnZhdWx0LWF1dGgifQ.aeVOgelVei3NX9PQm_qzhPIXL0iEamOsHhNfMrGXfat15nfIdRG1FmpSTkH7URvIxIprWbx6gvwaWhKsB4LDz7GEPjxEYr-c2sUU54ZaC2csauru2xWAuvf93MZTIVww7db_Huhq-YMiJsFjULjswWLIARd-8xOec8DMj9dx_w03B01YKhjDdplTynwAnoIaIZLvC7Wp81ZrgpwihsiGWOFc_oOtxr3QOlZfGSGLkc2Bxnm446Nc-EeUOMs0ctW1xra5yAvNo05iKcsO3tZ5fdQj6xT-WMF-Gt_lbmyvP1-26-b55jcVSpXSOSWmrFb2FYG-3FmsGiTRYvwLV_grKg"'", "'"role"'": "'"example"'"}' \
        	http://vault:8200/v1/auth/kubernetes/login "],
                                labels={"test-airflow": "firstversion"},
                                name="passing-test",
                                task_id="passing-task",
				get_logs=True,
                                dag=dag
                                )
