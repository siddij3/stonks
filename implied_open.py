# Imports
import requests
from datetime import datetime, timedelta

import pandas as pd
from bs4 import BeautifulSoup

from pytz import timezone

import json
from headers import headers
import urls



def get_indexes():

    # Randomize the numbers so it doesn't get repetitive
    response_dow = requests.get(url=urls.url_dow, headers=headers)
    response_sp = requests.get(url=urls.url_sp, headers=headers)
    response_nasdaq = requests.get(url=urls.url_nasdaq, headers=headers)

    # Parse the whole HTML page using BeautifulSoup
    dow = BeautifulSoup(response_dow.text, 'html.parser')
    sp = BeautifulSoup(response_sp.text, 'html.parser')
    nasdaq = BeautifulSoup(response_nasdaq.text, 'html.parser')


    json_dow = json.loads(dow.string)[0]
    json_sp = json.loads(sp.string)[0]
    json_nasdaq = json.loads(nasdaq.string)[0]

    dow_io = json_dow['implied_open']
    sp_io = json_sp['implied_open']
    nasdaq_io = json_nasdaq['implied_open']

    dow_price = json_dow['price']
    sp_price = json_sp['price']
    nasdaq_price = json_nasdaq['price']

    updated_at = str(datetime.fromisoformat(str(json_nasdaq["last_updated"]).split('.')[0]))
   
    import time
    dict = {
        "date_time": datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'),

       "dow_io":dow_io,
       "dow_price":dow_price,

       "sp_io":sp_io,
       "sp_price":sp_price,

       "nasdaq_io":nasdaq_io,
       "nasdaq_price":nasdaq_price,

       "updated_at_GMT": updated_at,
       "id": int(time.time())
       }

    # project_id = logins.project_id
    # table_id = f"{logins.database}.{logins.io_raw}"
    def fix_datetime(df, pd):
        df['date_time'] = pd.to_datetime(df['date_time'])
        return df


    df = fix_datetime(pd.DataFrame([dict]), pd)
    
    df['updated_at_GMT'] = pd.to_datetime(df['updated_at_GMT'])
    
    return df




