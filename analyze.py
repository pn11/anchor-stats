import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_label(filename):
    """Assume CSV file name to be EPISODENUMBER_EPISODETITLE eg.) 1_TheFirstEpisode.csv
    and get the number from the file name."""
    filename = filename.split('/')[-1]
    filename = filename.split('_')[0]
    return filename


def create_timedelta(df):
    df_ = df[:]
    # Convert to Datetime to get timedelta
    df_['Time (UTC)'] = pd.to_datetime(
        df['Time (UTC)'], format='%m/%d/%Y %H:%M:%S')
    df_diff = pd.DataFrame.from_dict({"diff": df_["Time (UTC)"][i]-df_[
                                     "Time (UTC)"][0], df_.columns.values[1]: df_.iat[i, 1]} for i in range(len(df_)))
    print(df_diff)
    return df_diff


def load_data():
    csvs = [csv for csv in glob.glob('./data/*.csv')]
    csvs = sorted(csvs)
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

    df['Time (UTC)'] = pd.to_datetime(
        df['Time (UTC)'], format='%m/%d/%Y %H:%M:%S')
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
    ax2 = fig.add_subplot(223)
    ax3 = fig.add_subplot(222)
    ax4 = fig.add_subplot(224)
    for i, col in enumerate(y.columns.to_list()):
        ax1.plot(x, y.iloc[:, i], label=col)
        ax2.plot(x, np.cumsum(y.iloc[:, i]), label=col)
        ax3.plot(x_diff, y_diff.iloc[:, i], label=col)
        ax4.plot(x_diff, np.cumsum(y_diff.iloc[:, i]), label=col)

    ax1.legend()

    plt.show()


def main():
    df, df_diff = load_data()
    plot_data(df, df_diff)


if __name__ == '__main__':
    main()
