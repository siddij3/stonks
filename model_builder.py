import pandas as pd
import numpy as np
import libs.sql_manager as sql_manager

import tensorflow as tf
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
from window import WindowGenerator
from window import Baseline
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from residual import ResidualWrapper
from multistepbaseline import MultiStepLastBaseline
from residual import FeedBack

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

def compile_and_fit(model, window, patience=2, max_epochs=100):
  
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

    single_step_window = WindowGenerator(input_width=1, label_width=1, shift=1, 
                         train_df = train_df,
                         val_df = val_df,
                         test_df = test_df,
                         label_columns=['price'])

    # baseline = Baseline(label_index=column_indices['price'])

    # baseline.compile(loss=tf.keras.losses.MeanSquaredError(),
    #                 metrics=[tf.keras.metrics.MeanAbsoluteError()])

    val_performance = {}
    performance = {}
    # val_performance['Baseline'] = baseline.evaluate(single_step_window.val)
    # performance['Baseline'] = baseline.evaluate(single_step_window.test, verbose=1)

    # print('Input shape:', wide_window.example[0].shape)
    # print('Output shape:', baseline(wide_window.example[0]).shape)


    # -----------------------------------------------------------------------  DENSE MODEL
    dense = tf.keras.Sequential([
            tf.keras.layers.Dense(units=64, activation='relu'),
            tf.keras.layers.Dense(units=64, activation='relu'),
            tf.keras.layers.Dense(units=1)
        ])
    # history = compile_and_fit(dense, single_step_window)
    # val_performance['Dense'] = dense.evaluate(single_step_window.val)
    # performance['Dense'] = dense.evaluate(single_step_window.test, verbose=0)

    # wide_window.plot(dense)

    #  -----------------------------------------------------------------------  MULTI STEP DENSE   
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
    multi_step_dense = tf.keras.Sequential([
        # Shape: (time, features) => (time*features)
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=32, activation='relu'),
        tf.keras.layers.Dense(units=32, activation='relu'),
        tf.keras.layers.Dense(units=1),
        # Add back the time dimension.
        # Shape: (outputs) => (1, outputs)
        tf.keras.layers.Reshape([1, -1]),
    ])
    # history = compile_and_fit(multi_step_dense, conv_window)


    #  ----------------------------------------------------------------------- CONVOLUTIONAL NEURAL NETWORKS
    LABEL_WIDTH = 32
    INPUT_WIDTH = LABEL_WIDTH + (CONV_WIDTH - 1)
    # Note that the output is shorter than the input. To make training or plotting work, you need the labels, and prediction to have the same length. 
    # So build a WindowGenerator to produce wide windows with a few extra input time steps so the label and prediction lengths match: 

    # Now, you can plot the model's predictions on a wider window. 

    wide_conv_window = WindowGenerator(
        input_width=INPUT_WIDTH,
        label_width=LABEL_WIDTH,
        shift=1,
        train_df = train_df,
        val_df = val_df,
        test_df = test_df,
        label_columns=['price'])

    #  Note the 3 input time steps before the first prediction. 
    #  Every prediction here is based on the 3 preceding time steps: THIS IS THE CONV WIDTH
    conv_model = tf.keras.Sequential([
        tf.keras.layers.Conv1D(filters=32,
                            kernel_size=(CONV_WIDTH,),
                            activation='relu'),
        tf.keras.layers.Dense(units=32, activation='relu'),
        tf.keras.layers.Dense(units=1),
    ])

    # history = compile_and_fit(conv_model, wide_conv_window)
    # wide_conv_window.plot(conv_model)


    # -----------------------------------------------------------------------  RECURRENT NEURAL NETWORK

    lstm_model = tf.keras.models.Sequential([
                # Shape [batch, time, features] => [batch, time, lstm_units]
                tf.keras.layers.LSTM(32, return_sequences=True),
                # Shape => [batch, time, features]
                tf.keras.layers.Dense(units=1)
            ])
    
    # history = compile_and_fit(lstm_model, wide_window)
    # wide_window.plot(lstm_model)


    ############################################### MULTI OUTPUT MODELS ###################################
    wide_window = WindowGenerator(
        input_width=24, label_width=24, shift=1, 
        train_df = train_df,
        val_df = val_df,
        test_df = test_df,
        label_columns=['price', 'RSI'])

    # --------------------------------------------- Baseline -------
    # baseline = Baseline(1)
    # baseline.compile(loss=tf.keras.losses.MeanSquaredError(),
    #                 metrics=[tf.keras.metrics.MeanAbsoluteError()])

    val_performance = {}
    performance = {}
    # val_performance['Baseline'] = baseline.evaluate(wide_window.val)
    # performance['Baseline'] = baseline.evaluate(wide_window.test, verbose=0)

    num_features = 6
    dense = tf.keras.Sequential([
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=num_features)
    ])

    # history = compile_and_fit(dense, single_step_window)
    # wide_window.plot(dense)

    lstm_model = tf.keras.models.Sequential([
        # Shape [batch, time, features] => [batch, time, lstm_units]
        tf.keras.layers.LSTM(32, return_sequences=True),
        # Shape => [batch, time, features]
        tf.keras.layers.Dense(units=num_features)
        ])

    # history = compile_and_fit(lstm_model, wide_window)
    # wide_window.plot(lstm_model)

    OUT_STEPS = 24
    multi_window = WindowGenerator(
        input_width=24, label_width=OUT_STEPS, shift=OUT_STEPS, 
        train_df = train_df,
        val_df = val_df,
        test_df = test_df)
    

    # ---------------------------------------------------------- Dense Multistep Model
    multi_dense_model = tf.keras.Sequential([
        # Take the last time step.
        # Shape [batch, time, features] => [batch, 1, features]
        tf.keras.layers.Lambda(lambda x: x[:, -1:, :]),
        # Shape => [batch, 1, dense_units]
        tf.keras.layers.Dense(512, activation='relu'),
        # Shape => [batch, out_steps*features]
        tf.keras.layers.Dense(OUT_STEPS*num_features,
                            kernel_initializer=tf.initializers.zeros()),
        # Shape => [batch, out_steps, features]
        tf.keras.layers.Reshape([OUT_STEPS, num_features])
    ])
    # history = compile_and_fit(multi_dense_model, multi_window)
    # multi_window.plot(multi_dense_model)


    # ---------------------------------------------------------- Convolution CNN Multistep Model
    
    CONV_WIDTH = 3
    multi_conv_model = tf.keras.Sequential([
        # Shape [batch, time, features] => [batch, CONV_WIDTH, features]
        tf.keras.layers.Lambda(lambda x: x[:, -CONV_WIDTH:, :]),
        # Shape => [batch, 1, conv_units]
        tf.keras.layers.Conv1D(256, activation='relu', kernel_size=(CONV_WIDTH)),
        # Shape => [batch, 1,  out_steps*features]
        tf.keras.layers.Dense(OUT_STEPS*num_features,
                            kernel_initializer=tf.initializers.zeros()),
        # Shape => [batch, out_steps, features]
        tf.keras.layers.Reshape([OUT_STEPS, num_features])
    ])

    
    # history = compile_and_fit(multi_conv_model, multi_window)
    # multi_window.plot(multi_conv_model)

    # ---------------------------------------------------------- RNN Multistep

    
    feedback_model = FeedBack(units=32, out_steps=OUT_STEPS)
    prediction, state = feedback_model.warmup(multi_window.example[0])

    history = compile_and_fit(feedback_model, multi_window)
    multi_window.plot(feedback_model)

    plt.show()