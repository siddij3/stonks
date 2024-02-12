import pandas as pd
import numpy as np
import libs.sql_manager as sql_manager

import tensorflow as tf
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
from window import WindowGenerator
from window import Baseline
import os
# time_series.ipynb
# https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/structured_data/time_series.ipynb#scrollTo=6GmSTHXw6lI1

def periodicity(df):
    day = 60*60*24
    week = 7*day
    year = 365.2425*day

    df['Day sin'] = np.sin(df['Seconds'] * (2* np.pi / day))
    df['Day cos'] = np.cos(df['Seconds'] * (2 * np.pi / day))

    df['Week sin'] = np.sin(df['Seconds'] * (2* np.pi / week))
    df['Week cos'] = np.cos(df['Seconds'] * (2 * np.pi / week))

    return df



def str_to_datetime(s):
    import datetime
    split = s.split('-')
    year, month, day = int(split[0]), int(split[1]), int(split[2])
    return datetime.datetime(year=year, month=month, day=day)


def split_data(X, y):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=5)
    return X_train, X_test, y_train, y_test

def compile_and_fit(model, window, patience=2, max_epochs=200):
  
#   early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
#                                                     patience=patience,
#                                                     mode='min')

  model.compile(loss=tf.keras.losses.MeanSquaredError(),
                optimizer=tf.keras.optimizers.Adam(),
                metrics=[tf.keras.metrics.MeanAbsoluteError()])

  history = model.fit(window.train, epochs=max_epochs,
                      validation_data=window.val
                      )
  return history

def df_to_X_y(df, window_size=5):
    df_as_np = df.to_numpy()
    X = []
    y = []

    for i in range(len(df_as_np)-window_size):
        row = [[a] for a in df_as_np[i:i+window_size]]
        X.append(row)
        label = df_as_np[i+window_size]
        y.append(label)

  

if __name__ == '__main__':

    engine = sql_manager.connect()
    nvdia_ts = pd.read_sql_query("select * from quotes;", engine)
   
    for key in nvdia_ts:
        if "date_time" not in key:
            nvdia_ts[key] = nvdia_ts[key].astype('float').interpolate()

        elif "date_time" in key:
            nvdia_ts[key] = pd.to_datetime(nvdia_ts[key])
    
    #Removing non-business hours and weekends
    nvdia_ts = nvdia_ts[(nvdia_ts['date_time'].dt.hour > 4) & (nvdia_ts['date_time'].dt.hour < 18)]
    nvdia_ts = nvdia_ts[nvdia_ts['date_time'].dt.dayofweek < 5]

    nvdia_ts.index = nvdia_ts.pop('date_time')
    
    nvdia_ts['Seconds'] = nvdia_ts.index.map(pd.Timestamp.timestamp)
    nvdia_ts = periodicity(nvdia_ts)

    nvdia_ts = nvdia_ts.drop('Seconds', axis=1)
    nvdia_ts = nvdia_ts.drop('id', axis=1)

    
    # ML stuff
    column_indices = {name: i for i, name in enumerate(nvdia_ts.columns)}
    
    n = len(nvdia_ts)
    
    train_df = nvdia_ts[0:int(n*0.7)]
    val_df = nvdia_ts[int(n*0.7):int(n*0.9)]
    test_df = nvdia_ts[int(n*0.9):]

    train_mean = train_df.mean()
    train_std = train_df.std()

    train_df = (train_df - train_mean) / train_std
    val_df = (val_df - train_mean) / train_std
    test_df = (test_df - train_mean) / train_std

    wide_window = WindowGenerator(input_width=16, label_width=16, shift=1, 
                         train_df = train_df,
                         val_df = val_df,
                         test_df = test_df,
                         label_columns=['price'])

    # print(wide_window.train)
    # print(wide_window.train.element_spec)

    # single_step_window = WindowGenerator(input_width=1, label_width=1, shift=1, 
    #                      train_df = train_df,
    #                      val_df = val_df,
    #                      test_df = test_df,
    #                      label_columns=['price'])

    # baseline = Baseline(label_index=column_indices['price'])

    # baseline.compile(loss=tf.keras.losses.MeanSquaredError(),
    #                 metrics=[tf.keras.metrics.MeanAbsoluteError()])

    val_performance = {}
    performance = {}
    # val_performance['Baseline'] = baseline.evaluate(single_step_window.val)
    # performance['Baseline'] = baseline.evaluate(single_step_window.test, verbose=1)

    # print('Input shape:', wide_window.example[0].shape)
    # print('Output shape:', baseline(wide_window.example[0]).shape)

    #                                                                      LINEAR MODEL
    # linear = tf.keras.Sequential([
    #             tf.keras.layers.Dense(units=1)
    #         ])   
    # history = compile_and_fit(linear, single_step_window)

    #                                                                       DENSE MODEL
    # dense = tf.keras.Sequential([
    #         tf.keras.layers.Dense(units=64, activation='relu'),
    #         tf.keras.layers.Dense(units=64, activation='relu'),
    #         tf.keras.layers.Dense(units=1)
    #     ])
    # history = compile_and_fit(dense, single_step_window)
    # val_performance['Dense'] = dense.evaluate(single_step_window.val)
    # performance['Dense'] = dense.evaluate(single_step_window.test, verbose=0)

    # wide_window.plot(dense)

    #                                                                 MULTI STEP DENSE   
    CONV_WIDTH = 8
                              
    conv_window = WindowGenerator(
        input_width=CONV_WIDTH,
        label_width=1,
        shift=1,
        train_df = train_df,
        val_df = val_df,
        test_df = test_df,
        label_columns=['price'])

    # The main down-side of this approach is that the resulting model can only be executed on input windows of exactly this shape. 
    # multi_step_dense = tf.keras.Sequential([
    #     # Shape: (time, features) => (time*features)
    #     tf.keras.layers.Flatten(),
    #     tf.keras.layers.Dense(units=32, activation='relu'),
    #     tf.keras.layers.Dense(units=32, activation='relu'),
    #     tf.keras.layers.Dense(units=1),
    #     # Add back the time dimension.
    #     # Shape: (outputs) => (1, outputs)
    #     tf.keras.layers.Reshape([1, -1]),
    # ])
    # history = compile_and_fit(multi_step_dense, conv_window)

    LABEL_WIDTH = 24
    INPUT_WIDTH = LABEL_WIDTH + (CONV_WIDTH - 1)
    # Note that the output is shorter than the input. To make training or plotting work, you need the labels, and prediction to have the same length. 
    # So build a WindowGenerator to produce wide windows with a few extra input time steps so the label and prediction lengths match: 
    wide_conv_window = WindowGenerator(
        input_width=INPUT_WIDTH,
        label_width=LABEL_WIDTH,
        shift=1,
        train_df = train_df,
        val_df = val_df,
        test_df = test_df,
        label_columns=['price'])


    conv_model = tf.keras.Sequential([
        tf.keras.layers.Conv1D(filters=32,
                            kernel_size=(CONV_WIDTH,),
                            activation='relu'),
        tf.keras.layers.Dense(units=32, activation='relu'),
        tf.keras.layers.Dense(units=1),
    ])

    history = compile_and_fit(conv_model, wide_conv_window)
    conv_window.plot(multi_step_dense)

    plt.show()