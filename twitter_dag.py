from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from twitter import twitter_app
from configurations.config import TWITTER_USER, EMAIL_RECIPIENT


html_email_str = """
latest tweets from {{ params.username }} has been uploaded to S3
"""

default_args = {
  'owner': 'johnguev',
  'start_date': datetime(2023, 4, 1),
  'email': ['airflowresults@datacamp.com'],
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 3,
  'retry_delay': timedelta(minutes=20)
}

twitter_dag = DAG(
    dag_id='twitter_dag',
    default_args=default_args,
    schedule_interval='@monthly'
)

get_tweets_task = PythonOperator(
    task_id='get_tweets',
    python_callable=twitter_app,
    op_args=[TWITTER_USER]
)

send_notif_task = EmailOperator(
    task_id='email_manager',
    to=EMAIL_RECIPIENT,
    subject='New tweets uploaded to S3 bucket',
    html_content=html_email_str,
    params={'username': TWITTER_USER}
)

get_tweets_task >> send_notif_task