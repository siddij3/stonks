
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pytz import timezone
from datetime import datetime, timedelta
import time
import headers
import urls
from urllib.request import Request, urlopen



def getmarket(soup):
    a = soup.find('meta', attrs={'name': 'exchange'})

    exchange_content = a.get('content') if a else None

    if exchange_content == None or exchange_content == []:
        return 0
    
    print(exchange_content)
    market = exchange_content.split(" ")[1:]
    market = ' '.join(market)
    return market

def scrapefinviz():
    
    def get_market(soup):
        market = soup.find("td", class_="fullview-links").find_all('a')
        market = market[-1].text

        return market

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

def get_actual_price(tic, BeautifulSoup):
    import requests
    import re

    url = f"https://www.marketwatch.com/investing/stock/{tic}"
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    a = soup.find_all("h2", class_="intraday__price")

    if a == None or a == []:
        return 0
    
    quote = re.findall(r'[\d]*[.][\d]+', str(a))[-1]
    return quote

def get_RSI(tic, BeautifulSoup):

    url_nvda = urls.url_nvda
    req = Request(url_nvda , headers=headers.headers2)

    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    a = soup.find_all("td", class_="snapshot-td2")  
    # b = soup.find_all("td", string="RSI (14)")  # This gives the RSI/

    i = 0
    for item in a:
        if item.text == "RSI (14)":
            return a[i+1].text
        i +=1

    return 0

def get_stock_price():

    date = str(datetime.now(timezone('US/Eastern'))).split()[0]
    stamp = str(datetime.now(timezone('US/Eastern'))).split()[1].split('.')[0]
  
    dict_quotes = {"date": date, "stamp": stamp}
    date = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d')
 
    price = get_actual_price("NVDA", BeautifulSoup) # soup.find_all("td", class_="snapshot-td2")[28].text  # This gives the RSI
    RSI = get_RSI("NVDA", BeautifulSoup) 
    

    def fix_datetime(df, pd):
        df['date_time'] = pd.to_datetime(df['date_time'])
        return df
    
    dict = {
        "date_time":datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'),

       "price": price,
       "RSI": RSI,
       "id": int(time.time())
       }
    
    df = fix_datetime(pd.DataFrame([dict]), pd)
    
    return df