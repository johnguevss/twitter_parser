from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from twitter import twitter_app

default_args = {

}

dag = DAG