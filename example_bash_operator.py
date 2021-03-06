from airflow import DAG
from airflow import configuration as conf
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

dag = DAG(
    'kubernetes_sample', start_date=datetime(2020, 1, 1),
    schedule_interval=None)

start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(namespace='default',
                                image="python:3.6",
                                cmds=["python", "-c"],
                                arguments=["print('hello world')"],
                                labels={"test-airflow": "firstversion"},
                                name="passing-test",
                                task_id="passing-task",
                                get_logs=True,
                                dag=dag
                                )

failing = KubernetesPodOperator(namespace='default',
                                image="ubuntu:1604",
                                cmds=["python", "-c"],
                                arguments=["print('hello world')"],
                                labels={"test-airflow": "firstversion"},
                                name="fail",
                                task_id="failing-task",
                                get_logs=True,
                                dag=dag
                                )

passing.set_upstream(start)
failing.set_upstream(start)
