# Imports
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from pytz import timezone
from datetime import datetime, timedelta
import json
from sql_manager import pandas_to_sql
from sql_manager import check_tables
from sql_manager import connect
from sql_manager import impliedopen_table
from sql_manager import pandas_to_sql_if_exists
from headers import headers

if __name__ == '__main__':

    url_dow = "https://production.dataviz.cnn.io/markets/futures/summary/YM00-USA:D"
    url_sp = "https://production.dataviz.cnn.io/markets/futures/summary/ES00-USA:D"
    url_nasdaq = "https://production.dataviz.cnn.io/markets/futures/summary/NQ00-USA:D"
   
    # Randomize the numbers so it doesn't get repetitive
    response_dow = requests.get(url=url_dow, headers=headers)
    response_sp = requests.get(url=url_sp, headers=headers)
    response_nasdaq = requests.get(url=url_nasdaq, headers=headers)

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




