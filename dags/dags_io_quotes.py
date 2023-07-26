from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from airflow import models
from airflow.models.xcom_arg import XComArg
from airflow.providers.google.cloud.operators.cloud_sql import (
    CloudSQLCloneInstanceOperator,
    CloudSQLCreateInstanceDatabaseOperator,
    CloudSQLCreateInstanceOperator,
    CloudSQLDeleteInstanceDatabaseOperator,
    CloudSQLDeleteInstanceOperator,
    CloudSQLExportInstanceOperator,
    CloudSQLImportInstanceOperator,
    CloudSQLInstancePatchOperator,
    CloudSQLPatchInstanceDatabaseOperator,
)

import sys
sys.path.append('/opt/airflow/dags/libs')
import json
import requests
from bs4 import BeautifulSoup
from pytz import timezone
import pandas as pd


default_args = {
    'owner': 'junaid',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}


def get_io():
    import libs.af_urls as urls
    from libs.af_headers import headers

    

    # Randomize the numbers so it doesn't get repetitive
    response_dow = requests.get(url=urls.url_dow, headers=headers)
    response_sp = requests.get(url=urls.url_sp, headers=headers)
    response_nasdaq = requests.get(url=urls.url_nasdaq, headers=headers)

    # Parse the whole HTML page using BeautifulSoup
    dow = BeautifulSoup(response_dow.text, 'html.parser')
    sp = BeautifulSoup(response_sp.text, 'html.parser')
    nasdaq = BeautifulSoup(response_nasdaq.text, 'html.parser')

    date = str(datetime.now(timezone('US/Eastern'))).split()[0]
    stamp = str(datetime.now(timezone('US/Eastern'))).split()[1].split('.')[0]

    json_dow = json.loads(dow.string)[0]
    json_sp = json.loads(sp.string)[0]
    json_nasdaq = json.loads(nasdaq.string)[0]

    dow_io = json_nasdaq['implied_open']
    sp_io = json_sp['implied_open']
    nasdaq_io = json_nasdaq['implied_open']

    dow_price = json_nasdaq['price']
    sp_price = json_sp['price']
    nasdaq_price = json_nasdaq['price']
    
    date = str(datetime.now(timezone('US/Eastern'))).split()[0]
    stamp = str(datetime.now(timezone('US/Eastern'))).split()[1].split('.')[0]
    updated_at = str(json_nasdaq["last_updated"]).split('T')[1].split('.')[0]

    dict = {
        "date":date,
       "stamp":stamp,

       "dow_io":dow_io,
       "dow_price":dow_price,

       "sp_io":sp_io,
       "sp_price":sp_price,

       "nasdaq_io":nasdaq_io,
       "nasdaq_price":nasdaq_price,

       "updated_at_GMT": updated_at
       }
    entry = pd.DataFrame.from_dict([dict])


def get_quotes():
    print("ok")

with DAG(
    default_args=default_args,
    dag_id="dag_io_quotes",
    start_date=datetime(2023, 7, 25),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='get_io',
        python_callable=get_io
    )
    
    update_table = BigQueryUpdateTableOperator(
    task_id="update_table",
    dataset_id=DATASET_NAME,
    table_id="test_table",
    fields=["friendlyName", "description"],
    table_resource={
        "friendlyName": "Updated Table",
        "description": "Updated Table",
    },
)

    task1 >> task2