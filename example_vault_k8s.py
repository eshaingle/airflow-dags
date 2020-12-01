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
os.environ['AIRFLOW__SECRETS__BACKEND_KWARGS'] = '{"connections_path": "myapp", "mount_point": "secret", "auth_type": "token", "token":"s.Jaqyd5pwV0raCaigktNrO44J", "url": "http://localhost:8200", "kv_engine_version": 1}'

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
    op_kwargs={'my_conn_id': 'smtp_default'},
    dag=dag)

passing = KubernetesPodOperator(namespace='default',
				service_account_name="vault-auth",
                                image="alpine:3.7",
                                cmds=["sh", "-cx"],
                                arguments=["apk add curl && curl --request POST \
        	--data '{"'"jwt"'": "'"eyJhbGciOiJSUzI1NiIsImtpZCI6IndjZ3RUNGFwUzVMV1FKNl9YTnZER2c5OUk4c1l6aE9ERzFhOHh0QkdxRVkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6InZhdWx0LWF1dGgtdG9rZW4teDVscjgiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidmF1bHQtYXV0aCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljYTBhOTk5LTYzOGUtNDgyNS1hNTkxLWM0MDU2YTU5NmVkZCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OnZhdWx0LWF1dGgifQ.uSo_RnaM3LxwDxnRDCwezCSccG0ynqXPjc5Ez9c0s_VbqdnAUaQuiGeO1wO9fWAsDb-dMNYIqUyXRD71z6POLew2MUR4trxWaicuOxbb5XLWoaE3XCKPubpEHWuXOExTuRT8QttVHX1QUEGxKqFfZeRezSsfLirZSOaqYijBS7qkPtDTggNCHKL9NVL0I3ssLLUDa7QVvDSFOLKhimXZqzWqsiaXlwdgel-F3UxAlKh-9EBIXHxvW8-1optkn-dnFAXzqfD3U61t6E2y_3JLcjwJWpGYNR3sFhXeglNdvhe9UNHsf_P3IqjN-IsRNdNq54luPHCetJDqvpZFzA94_w"'", "'"role"'": "'"example"'"}' \
        	http://vault:8200/v1/auth/kubernetes/login "],
                                labels={"test-airflow": "firstversion"},
                                name="passing-test",
                                task_id="passing-task",
				get_logs=True,
                                dag=dag
                                )
