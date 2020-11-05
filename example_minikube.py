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
        print("no ip set")

    host = '{}:30809'.format(host_ip.strip())
    print("minikube ip:", {host})
    return host
   
dag = DAG(
    dag_id='minikube_test', start_date=datetime(2020, 1, 1),
    schedule_interval=None)

test_task = PythonOperator(
    task_id='test-minikube',
    python_callable=get_minikube_host,
    dag=dag)
