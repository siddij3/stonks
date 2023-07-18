
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
import re
import sql_manager



def scrape(tic):
    url = f"https://www.marketwatch.com/investing/stock/{tic}"

    print(url)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    market = getmarket(soup)

    quote = getquote(soup)

    return  market, quote

def getmarket(soup):
    a = soup.find('meta', attrs={'name': 'exchange'})

    exchange_content = a.get('content') if a else None
    print(exchange_content)

    if exchange_content == None:
        return 0
     
    market = exchange_content.split(" ")[1:]
    market = ' '.join(market)
    return market

def getquote(soup):


    
    a = soup.find_all("h2", class_="intraday__price")
    if a == None:
        return 0
    
    quote = re.findall(r'[\d]*[.][\d]+', str(a))[-1]
    return quote

if __name__ == "__main__":
    ticker_list = pd.read_csv("nasdaq_screener.csv")['Symbol']

    date = str(datetime.now(timezone('US/Eastern'))).split()[0]
    stamp = str(datetime.now(timezone('US/Eastern'))).split()[1].split('.')[0]
  
    dict_quotes = {"date": date, "stamp": stamp}
    markets = []
    tickers = []
    
    shortend_list = ticker_list[600: 700]

    for tic in shortend_list:
        if '^' in tic or '/' in tic:
            continue

        market, quote  = scrape(tic)

        if market == 0:
            continue;

        markets.append(market)
        tickers.append(tic)

        dict_quotes[tic] = quote 

 
    # df = pd.DataFrame([tickers, markets], columns=["tickers","markets"])
    table = {
         "ticker": tickers,
         "market": markets
     }
    
    
    quotes = pd.DataFrame.from_dict([dict_quotes])
    tickers_markers = pd.DataFrame.from_dict(table)

    quotes_table_name = sql_manager.quotes_table()
    markets_table_name = sql_manager.markets_table()

    engine = connect()

    if (not check_tables(engine, quotes_table_name)):
        pandas_to_sql(quotes_table_name, quotes, engine)

    else:
        pandas_to_sql(quotes_table_name, quotes, engine)

    if (not check_tables(engine, markets_table_name)):
        pandas_to_sql(markets_table_name, tickers_markers, engine)

    else:
        pandas_to_sql(markets_table_name, tickers_markers, engine)