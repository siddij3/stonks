import tensorflow as tf
import os
import pandas as pd
import numpy as np
import libs.sql_manager as sql_manager
import sql_queries

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import RNN
# from tensorflow.keras.layers import CNN
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam


from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

def periodicity(df):
    day = 60*60*24
    week = 7*day
    year = 365.2425*day

    df['Day sin'] = np.sin(df['Seconds'] * (2* np.pi / day))
    df['Day cos'] = np.cos(df['Seconds'] * (2 * np.pi / day))

    df['Week sin'] = np.sin(df['Seconds'] * (2* np.pi / week))
    df['Week cos'] = np.cos(df['Seconds'] * (2 * np.pi / week))

    df['Year sin'] = np.sin(df['Seconds'] * (2 * np.pi / year))
    df['Year cos'] = np.cos(df['Seconds'] * (2 * np.pi / year))

    return df

def str_to_datetime(s):
    import datetime
    split = s.split('-')
    year, month, day = int(split[0]), int(split[1]), int(split[2])
    return datetime.datetime(year=year, month=month, day=day)

def windowed_df_to_date_X_y(windowed_dataframe):
    df_as_np = windowed_dataframe.to_numpy()
    
    print()
    
    dates = df_as_np[:, 0]
    # TODO
    # [[[1, a, !,], [2, b, @], [3, , ], [4, , ], [5]]] [6]
    # [[[2], [3], [4], [5], [6]]] [7]
    # [[[3], [4], [5], [6], [7]]] [8]

    middle_matrix = df_as_np[:, 2:]
    X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))

    Y = df_as_np[:, 1]

    return dates, X.astype(np.float32), Y.astype(np.float32)

def split_data():

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=5)
    return X_train, X_test, y_train, y_test

def build_LSTM():
    model5 = Sequential()
    model5.add(InputLayer((7, 6)))
    model5.add(LSTM(64))
    model5.add(Dense(8, 'relu'))
    model5.add(Dense(2, 'linear'))

    model5.summary()

if __name__ == '__main__':

    engine = sql_manager.connect()
    nvdia_ts = pd.read_sql_query(sql_queries.query_quotes, engine)

    for key in nvdia_ts:
        if "date_time" not in key:
            nvdia_ts[key] = nvdia_ts[key].astype('float').interpolate()

        elif "date_time" in key:
            nvdia_ts[key] = pd.to_datetime(nvdia_ts[key])
    

    nvdia_ts.index = nvdia_ts.pop('t0_date_time')
    nvdia_ts['Seconds'] = nvdia_ts.index.map(pd.Timestamp.timestamp)
    nvdia_ts = periodicity(nvdia_ts)


    nvdia_ts = nvdia_ts.drop('Seconds', axis=1)
    # ML stuff

    dates, X, y = windowed_df_to_date_X_y(nvdia_ts)

    print(X)

    exit()

    # plt.plot(np.array(nvdia_ts['Day sin'])[:200])
    # plt.plot(np.array(nvdia_ts['Day cos'])[:200])
    # plt.xlabel('Time [h]')
    # plt.title('Time of day signal')
    # plt.show()

    fft_price = tf.signal.rfft(nvdia_ts['price'])
    fft_rsi = tf.signal.rfft(nvdia_ts['rsi'])

    
    f_per_dataset_price = np.arange(0, len(fft_price))
    f_per_dataset_rsi = np.arange(0, len(fft_rsi))

    n_samples_h = len(nvdia_ts['price'])
    hours_per_year = 24*365.2524
    years_per_dataset = n_samples_h/(hours_per_year)

    # f_per_year_price = f_per_dataset_price/years_per_dataset
    # plt.step(f_per_year_price, np.abs(fft_price))
    # plt.xscale('log')
    # plt.ylim(0, 400000)
    # plt.xlim([0.1, max(plt.xlim())])
    # plt.xticks([1, 365.2524], labels=['1/Year', '1/day'])
    # _ = plt.xlabel('Frequency (log scale)')
    # plt.show()

# LSTM Time Series Forecasting.ipynb
    # Check Youtube for this one
# https://colab.research.google.com/drive/1qMgLSij0pdwW56cu3ZEtHvLdx3gur4S5#scrollTo=J-YOd8tLhpE0

# time_series.ipynb
# https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/structured_data/time_series.ipynb#scrollTo=6GmSTHXw6lI1

