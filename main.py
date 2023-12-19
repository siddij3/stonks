import implied_open
import tickers


if __name__ == '__main__':

    df_io = implied_open.get_indexes()
    df_ticker = tickers.get_stock_price()

    print(df_io)
    print(df_ticker)
# https://colab.research.google.com/drive/1qMgLSij0pdwW56cu3ZEtHvLdx3gur4S5#scrollTo=C1MZOKB3Sg0X


