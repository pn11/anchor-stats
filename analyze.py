import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_label(filename):
    filename = filename.split('/')[-1]
    filename = filename.split('_')[0]
    # sometimes unexpected '%'
    filename = filename.split('%')[0]
    filename = filename[:10]
    return filename


def parse_time(series):
    """Convert to Datetime to get timedelta"""
    # ignore 24:00:00 (cannot parse with strptime)
    series = series.apply(lambda x: x.split(' ')[0])
    series = pd.to_datetime(series, format='%m/%d/%Y')
    return series


def create_timedelta(df):
    df_ = df[:]
    df_['Time (UTC)'] = parse_time(df_['Time (UTC)'])
    df_diff = pd.DataFrame.from_dict({"diff": df_["Time (UTC)"][i]-df_[
                                     "Time (UTC)"][0], df_.columns.values[1]: df_.iat[i, 1]} for i in range(len(df_)))
    print(df_diff)
    return df_diff


def load_data():
    csvs = [csv for csv in glob.glob('./data/*.csv')]
    csvs = sorted(csvs, key=lambda x: make_label(x))
    df = pd.read_csv(f"{csvs[0]}")

    df = df.rename(columns={"Time (UTC)": "Time (UTC)",
                            "Plays": f"{make_label(csvs[0])}"})
    df_diff = create_timedelta(df)

    for csv in csvs[1:]:
        df_ = pd.read_csv(f"{csv}")
        df_ = df_.rename(
            columns={"Time (UTC)": "Time (UTC)", "Plays": f"{make_label(csv)}"})
        df_diff = pd.merge(df_diff, create_timedelta(df_))
        df = pd.merge(df, df_, on='Time (UTC)', how='outer')
    df['Time (UTC)'] = parse_time(df['Time (UTC)'])
    df = df.fillna(0)
    df = df.sort_values('Time (UTC)')
    print(df)
    print(df_diff)
    df.to_csv("merge.csv")

    return df, df_diff


def plot_data(df, df_diff):
    x = df['Time (UTC)']
    y = df.iloc[:, 1:]
    x_diff = df_diff['diff']
    x_diff = [a.days for a in x_diff]
    y_diff = df_diff.iloc[:, 1:]

    # plot

    fig = plt.figure(figsize=(15, 8))
    ax1 = fig.add_subplot(221)
    ax1.set_title('Plays / day')
    ax2 = fig.add_subplot(223)
    ax2.set_title('Plays (cumulative)')
    ax3 = fig.add_subplot(222)
    ax3.set_title('Plays / day (in first few days)')
    ax4 = fig.add_subplot(224)
    ax3.set_title('Plays / day (cumulative, in first few days)')
    for i, col in enumerate(y.columns.to_list()):
        ax1.plot(x, y.iloc[:, i], label=col)
        ax2.plot(x, np.cumsum(y.iloc[:, i]), label=col)
        ax3.plot(x_diff, y_diff.iloc[:, i], label=col)
        ax4.plot(x_diff, np.cumsum(y_diff.iloc[:, i]), label=col)

    ax1.legend()

    total = df.sum(axis=1)
    
    # Total
    fig2 = plt.figure(figsize=(15, 8))
    ax5 = fig2.add_subplot(121)
    ax5.plot(df['Time (UTC)'], total)
    ax5.set_title('Total Plays / day')

    ax6 = fig2.add_subplot(122)
    ax6.plot(df['Time (UTC)'], np.cumsum(total))
    ax6.set_title('Total Plays (cumulative)')
    #ax6.set_yscale('log')

    plt.show()


def main():
    df, df_diff = load_data()
    plot_data(df, df_diff)


if __name__ == '__main__':
    main()
