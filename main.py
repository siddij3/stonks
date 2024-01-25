
import libs.implied_open as implied_open
import libs.quotes as quotes
import libs.sql_manager as sql_manager
import schedule
from apscheduler.schedulers.blocking import BlockingScheduler

import time
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
    scheduler.add_job(loop, 'interval', hours=1)
    scheduler.start()