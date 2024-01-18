
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from pytz import timezone
from datetime import datetime, timedelta
import json
import re
from libs.headers import headers


def isHaram(sector):

    if type(sector) != 'str':
         return 1
    
    if "Real Estate" in sector or "Finance" in sector or "Consumer" in sector or "Miscellaneous" in sector :
        return 1
    return 0

def isDoubtful(sector):

    if sector == "" :
        return 1
    return 0

def isHalal(sector):
    return  not isHaram(sector) or not isDoubtful(sector)

if __name__ == "__main__":


    halal_list = pd.read_csv("halal.csv", encoding='cp1252')

    ticker_list = pd.read_csv("nasdaq_screener.csv")

    dicts = []

    for tic in halal_list.index:
            dict = {
                "ticker": halal_list["Ticker"][tic],
                "halal":  1 if halal_list["Status"][tic] == "Halal" else 0,
                "haram":  1 if halal_list["Status"][tic] == "Not Halal" else 0,
                "doubtful": 1 if halal_list["Status"][tic] == "Doubtful" else 0
            }

            dicts.append(dict)

    ticker_keys = ticker_list.keys()[0]
    i = 0


    for tic in ticker_list.index:
        dict = {
            "ticker": ticker_list["Symbol"][tic],
             "halal": isHalal(ticker_list["Sector"][tic]),
             "haram":  isHaram(ticker_list["Sector"][tic]),
             "doubtful": isDoubtful(ticker_list["Sector"][tic])
        }
        dicts.append(dict)

