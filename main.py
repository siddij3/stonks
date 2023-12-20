# https://colab.research.google.com/drive/1qMgLSij0pdwW56cu3ZEtHvLdx3gur4S5#scrollTo=C1MZOKB3Sg0X

import implied_open
import quotes
import sql_manager
from apscheduler.schedulers.blocking import BlockingScheduler

from datetime import datetime, timedelta
from pytz import timezone

def loop():
    df_io = implied_open.get_indexes()
    df_quotes = quotes.get_stock_price()

    indexes_name = sql_manager.indexes_table()
    quotes_name = sql_manager.quotes_table()
    engine = sql_manager.connect()

    # if the table doesn't exist,  
    sql_manager.pandas_to_sql_if_exists(indexes_name, df_io, engine,  "append")
    sql_manager.pandas_to_sql_if_exists(quotes_name, df_quotes, engine,  "append")
    
    print(datetime.now(timezone('US/Eastern')))

    print(df_io)
    print(df_quotes)


if __name__ == '__main__':

    scheduler = BlockingScheduler()
    scheduler.add_job(loop, 'interval', hours=0.5)
    scheduler.start()




