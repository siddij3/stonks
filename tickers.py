
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

from datetime import datetime, timedelta


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


if __name__ == "__main__":

    date = str(datetime.now(timezone('US/Eastern'))).split()[0]
    stamp = str(datetime.now(timezone('US/Eastern'))).split()[1].split('.')[0]
  
    dict_quotes = {"date": date, "stamp": stamp}

    url_tic = f"https://finviz.com/quote.ashx?t=NVDA&ty=c&p=d&b=1"

    url_yahoo = f"https://ca.finance.yahoo.com/quote/NVDA/history?p=NVDA"

    req = Request(url_yahoo , headers=headers.headers2)

    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    close =  soup.find_all("td", class_="Py(10px) Pstart(10px)")[4] #[0].text.split(', ')[-1]   # This gives the INDEX wow
    print(close)
    date = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d')
    print(date)

    
# https://colab.research.google.com/drive/1qMgLSij0pdwW56cu3ZEtHvLdx3gur4S5#scrollTo=C1MZOKB3Sg0X





    # webpage = urlopen(req).read()
    # soup = BeautifulSoup(webpage, 'html.parser')
    
    # index = soup.find_all("td", class_="snapshot-td2")[0].text.split(', ')[-1]   # This gives the INDEX wow
    
    # price = soup.find_all("td", class_="snapshot-td2")[28].text  # This gives the RSI
    # RSI = soup.find_all("td", class_="snapshot-td2")[52].text  # This gives the RSI

    # print(index)
    # print(price)
    # print(RSI)

    # dict = {
    #     "date":date,
    #    "stamp":stamp,

    #    "price": price,
    #    "RSI": RSI
    #    }
    
    
    
    # # quotes = pd.DataFrame.from_dict([dict_quotes])
    # tickers_markers = pd.DataFrame.from_dict(table)

    # print(tickers_markers)
