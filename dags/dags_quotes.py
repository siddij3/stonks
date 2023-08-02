from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import sys
sys.path.append('/opt/airflow/dags/libs')



from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryDeleteDatasetOperator,
    BigQueryGetDatasetOperator,
    BigQueryUpdateDatasetOperator,
    BigQueryUpdateTableOperator,
    BigQueryExecuteQueryOperator
)


DAG_ID = 1
ENV_ID = 1
DATASET_NAME = f"dataset_{DAG_ID}_{ENV_ID}"


default_args = {
    'owner': 'junaid',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}


def get_io():
    import libs.af_urls as urls
    from libs.af_headers import headers
    import libs.af_libs as libs
    import libs.af_logins as logins
    import time
    import json
    import requests
    from bs4 import BeautifulSoup
    from pytz import timezone
    import pandas as pd

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

    dow_io = json_dow['implied_open']
    sp_io = json_sp['implied_open']
    nasdaq_io = json_nasdaq['implied_open']

    dow_price = json_dow['price']
    sp_price = json_sp['price']
    nasdaq_price = json_nasdaq['price']
    
    date = str(datetime.now(timezone('US/Eastern'))).split()[0]
    stamp = str(datetime.now(timezone('US/Eastern'))).split()[1].split('.')[0]
    updated_at = str(datetime.fromisoformat(str(json_nasdaq["last_updated"]).split('.')[0]))


    dict = {
        "date":time.strftime('%Y-%m-%d %H:%M:%S'),

       "dow_io":dow_io,
       "dow_price":dow_price,

       "sp_io":sp_io,
       "sp_price":sp_price,

       "nasdaq_io":nasdaq_io,
       "nasdaq_price":nasdaq_price,

       "updated_at_GMT": updated_at
       }
    print(dict)
    project_id = logins.project_id
    table_id = f"{logins.database}.{logins.io_raw}"
    libs.toBQ(pd.DataFrame([dict]), project_id, table_id)


def get_quote():
    from libs.af_headers import headers2
    import libs.af_urls as urls
    import libs.af_logins as logins
    import libs.af_libs as libs
    import time

    from pytz import timezone
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup

    import pandas as pd


    date = str(datetime.now(timezone('US/Eastern'))).split()[0]
    stamp = str(datetime.now(timezone('US/Eastern'))).split()[1].split('.')[0]
  
    url_nvda = f"https://finviz.com/quote.ashx?t=NVDA&ty=c&p=d&b=1"

    req = Request(url_nvda , headers=headers2)

    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    
    index = soup.find_all("td", class_="snapshot-td2")[0].text.split(', ')[-1]   # This gives the INDEX wow
    
    price = soup.find_all("td", class_="snapshot-td2")[28].text  # This gives the RSI
    RSI = soup.find_all("td", class_="snapshot-td2")[52].text  # This gives the RSI

    print(index)
    print(price)
    print(RSI)

     
    dict = {
        "date":time.strftime('%Y-%m-%d %H:%M:%S'),

       "price": price,
       "RSI": RSI
       }
    
    project_id = logins.project_id
    table_id = f"{logins.database}.{logins.table_nvda}"
    libs.toBQ(pd.DataFrame([dict]), project_id, table_id)


with DAG(
    default_args=default_args,
    dag_id="dag_quotes",
    start_date=datetime(2023, 8, 2),
    schedule_interval='@hourly',
    tags = ["stocks","bigquery"]
) as dag:
    task1 = PythonOperator(
        task_id='get_io',
        python_callable=get_io
    )

    task2= PythonOperator(
        task_id='get_quote',
        python_callable=get_quote
    )

    run_this = BashOperator(
        task_id="run_after_loop",
        bash_command="echo 1 This was run after the implied open scrape",
    )

    # markets_2 = BigQueryExecuteQueryOperator(
    #     task_id="markets_2",
    #     sql="""SELECT * FROM `ivory-oarlock-388916.stonks.io_raw`""",
    #     destination_dataset_table=f"ivory-oarlock-388916.stonks.io_raw_2",
    #     write_disposition="WRITE_TRUNCATE",
    #     gcp_conn_id="stocks_bigquery",
    #     use_legacy_sql=False,
    # )

    # task1  >> markets_2

    [task1, task2] >> run_this 
#     create_dataset = BigQueryCreateEmptyDatasetOperator(task_id="create_dataset", dataset_id=DATASET_NAME)
    
#     update_table = BigQueryUpdateTableOperator(
#     task_id="update_table",
#     dataset_id=DATASET_ID,
#     table_id="impliedopen",
#     fields=["date", "stamp", "dow_io", "dow_price", "sp_io", "sp_price", "nasdaq_io", "nasdaq_price", "updated_at_GMT"],
#     table_resource=dict,
# )


