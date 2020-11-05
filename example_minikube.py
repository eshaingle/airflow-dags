import os
from os import environ
import json
from airflow import DAG
from subprocess import check_output
from airflow.models import Variable
from datetime import datetime
from airflow.operators.python_operator import PythonOperator


def get_minikube_host():
    if "MINIKUBE_IP" in os.environ:
        host_ip = os.environ['MINIKUBE_IP']
    else:
        host_ip = check_output(['/usr/local/bin/minikube', 'ip']).decode('UTF-8')

    host = '{}:30809'.format(host_ip.strip())
    return host
   
dag = DAG(
    dag_id='minikube_test', start_date=datetime(2020, 1, 1),
    schedule_interval=None)

test_task = PythonOperator(
    task_id='test-minikube',
    python_callable=get_minikube_host,
    dag=dag)
