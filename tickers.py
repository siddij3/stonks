
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
import re



def scrape(tic):
    url = f"https://www.marketwatch.com/investing/stock/{tic}"

    print(url)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    a = soup.find_all("h2", class_="intraday__price")

    quote = re.findall(r'[\d]*[.][\d]+', str(a))[-1]

    return quote

if __name__ == "__main__":
    

    ticker_list = pd.read_csv("nasdaq_screener.csv")['Symbol']

    date = str(datetime.now(timezone('US/Eastern'))).split()[0]
    stamp = str(datetime.now(timezone('US/Eastern'))).split()[1].split('.')[0]
  
    dict = {"date": date, "stamp": stamp}

    shortend_list =ticker_list[0:20]

    for tic in shortend_list:
        if '^' in tic:
            continue

        quote = scrape(tic)

        dict[tic] = quote 
        

    print(pd.DataFrame.from_dict([dict]))