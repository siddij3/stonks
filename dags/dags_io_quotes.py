from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

import sys
sys.path.append('/opt/airflow/dags/libs')

from sklearn.preprocessing import StandardScaler
from keras.models import load_model
import pandas as pd
from pandas import DataFrame

import cloudinary
import sqlalchemy as sa

import requests
import shutil

import numpy as np

import os
import re

default_args = {
    'owner': 'junaid',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}


def download_models():
 

    print(response)
    print(os.listdir("dags/libs"))
    print(os.listdir("dags"))
    print(os.listdir())


def retrain_models():


    save_model(path, functions)

    

def save_model(path, functions):

    
    print("Response", response)
     

with DAG(
    default_args=default_args,
    dag_id="dag_for_wqm_v01",
    start_date=datetime(2023, 7, 1),
    schedule_interval='@daily' # 0 0 1,14 * * At 12:00 AM, on day 1 and 14 of the month 0 * * * *
) as dag:
    task1 = PythonOperator(
        task_id='download_models',
        python_callable=download_models
    )
    
    task2 = PythonOperator(
        task_id='retrain_models',
        python_callable=retrain_models
    )

    task1 >> task2