
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
import time
import headers
from urllib.request import Request, urlopen


def scrape(tic):
    url = f"https://www.marketwatch.com/investing/stock/{tic}"
    print(url)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    market = getmarket(soup)
    # quote = getquote(soup)

    return  market #, quote

def getmarket(soup):
    a = soup.find('meta', attrs={'name': 'exchange'})

    exchange_content = a.get('content') if a else None

    if exchange_content == None or exchange_content == []:
        return 0
    
    print(exchange_content)
    market = exchange_content.split(" ")[1:]
    market = ' '.join(market)
    return market

def getquote(soup):
    a = soup.find_all("h2", class_="intraday__price")

    if a == None or a == []:
        return 0
    
    print(a)
    quote = re.findall(r'[\d]*[.][\d]+', str(a))[-1]
    return quote


def scrapefinviz():

    numtics = int(8562)

    # tickers = ['A', 'AA', 'AAAU', 'AAC', 'AACG']
    tickers = []

    for i in range(1, numtics):

        if i % 20 == 1:
            time.sleep(0.5)
            
            print(i)
            url = f"https://finviz.com/screener.ashx?v=111&r={i}"

            req = Request(url , headers=headers.headers2)
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'html.parser')
            a = soup.find_all("a", class_="screener-link-primary")

            for tag in a:
                tickers.append(tag.string)

    print(tickers)

    markets = []
    for tic in tickers:
        time.sleep(0.5)
        url_tic = f"https://finviz.com/quote.ashx?t={tic}&ty=c&p=d&b=1"
        print(url_tic)
        req = Request(url_tic , headers=headers.headers2)

        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        
        markets.append(get_market(soup))


    return tickers, markets

def get_market(soup):
    market = soup.find("td", class_="fullview-links").find_all('a')
    market = market[-1].text
    # for m in market:
    return market


            
# def get_RSI():
#     return rsi

# def get_price():
#     return price:


if __name__ == "__main__":
    ticker_list = pd.read_csv("nasdaq_screener.csv")['Symbol'].dropna()

    date = str(datetime.now(timezone('US/Eastern'))).split()[0]
    stamp = str(datetime.now(timezone('US/Eastern'))).split()[1].split('.')[0]
  
    dict_quotes = {"date": date, "stamp": stamp}
    markets = []
    tickers = []
    
    shortend_list = ticker_list

    # for tic in shortend_list:

    #     if '^' in tic or '/' in tic:
    #         continue

        # market, quote  = scrape(tic)
        # market = scrape(tic)

        # if market == 0:
        #     continue;

        # markets.append(market)
        # tickers.append(tic)

        # dict_quotes[tic] = quote 

        # time.sleep(3)?
    tickers, markets  = scrapefinviz()


    table = {
         "ticker": tickers,
         "market": markets
     }
    
    # quotes = pd.DataFrame.from_dict([dict_quotes])
    tickers_markers = pd.DataFrame.from_dict(table)

    # quotes_table_name = sql_manager.quotes_table()
    markets_table_name = sql_manager.markets_table()

    print(tickers_markers)
    engine = connect()

    # if (not check_tables(engine, quotes_table_name)):
    #     pandas_to_sql(quotes_table_name, quotes, engine)

    # else:
    #     pandas_to_sql(quotes_table_name, quotes, engine)

    if (not check_tables(engine, markets_table_name)):
        pandas_to_sql(markets_table_name, tickers_markers, engine)

    else:
        sql_manager.pandas_to_sql_if_exists(markets_table_name, tickers_markers, engine, "append")