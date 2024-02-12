import seaborn as sns

# def weights_():
# One advantage to linear models is that they're relatively simple to  interpret.
# Sometimes the model doesn't even place the most weight on the input T (degC). This is one of the risks of random initialization. 
#     plt.bar(x = range(len(train_df.columns)),
#     height=linear.layers[0].kernel[:,0].numpy())
#     axis = plt.gca()
#     axis.set_xticks(range(len(train_df.columns)))
#     _ = axis.set_xticklabels(train_df.columns, rotation=90)


# def fftransform(df):
#     fft = tf.signal.rfft(df['price'])
#     f_per_dataset = np.arange(0, len(fft))

#     n_samples_h = len(df['price'])
#     hours_per_month = 24*30
#     months_per_dataset = n_samples_h/(hours_per_month)

#     f_per_month = f_per_dataset/months_per_dataset
#     plt.step(f_per_month, np.abs(fft))
#     plt.xscale('log')
#     plt.ylim(0, 20000)
#     plt.xlim([0.1, max(plt.xlim())])
#     plt.xticks([1, 30], labels=['1/Month', '1/day'])
#     _ = plt.xlabel('Frequency (log scale)')
#     plt.show()
   
# def matplotlib_plot(df):
    # plt.plot(np.array(df['Day sin']), 'bo')
    # plt.plot(np.array(df['Day cos']), 'ro')
    # plt.xlabel('Time [h]')
    # plt.title('Time of day signal')
    # plt.show()

# def peak_dist(df, train_mean, train_std):
#     df_std = (df - train_mean) / train_std
#     df_std = df_std.melt(var_name='Column', value_name='Normalized')
#     plt.figure(figsize=(12, 6))
#     ax = sns.violinplot(x='Column', y='Normalized', data=df_std)
#     _ = ax.set_xticklabels(df.keys(), rotation=90)
#     plt.show()