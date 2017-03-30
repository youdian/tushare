'''获取和更新股票行情历史'''
import os

import pandas
import tushare as ts


def fetch_history(stock):
    '''从服务器获取股票日行情'''
    df = None
    try:
        df = ts.get_k_data(code=stock, pause=0.01)
    except IndexError as err:
        print("sotck ", stock, " fetch error:", str(err))
        pass
    if df is not None:
        add_percent(df)
        file_name = get_file_path(stock)
        df.to_csv(file_name)
        return df
    else:
        print(stock, 'fetch history failed')
        return None


def get_history(stock):
    file_name = get_file_path(stock)
    df = None
    if not os.path.exists(file_name):
        df = fetch_history(stock)
    else:
        df = pandas.read_csv(file_name, index_col=0)
    return df


def get_file_path(stock):
    return 'csv/' + stock + '.csv'


def fetch_all():
    df = pandas.read_csv('csv/stocks.csv', dtype={'code': str})
    count = len(df)
    i = 0
    for code in df.code:
        i += 1
        print('total stocks ', count, ", now fetching ", i)
        fetch_history(code)

def add_percent(df):
    if df is None:
        return
    length = len(df)
    l_p_high = []
    l_p_low = []
    l_p_open = []
    l_swing = []
    l_up = []
    for i in range(length - 1):
        last_close = df.close[i + 1]
        p_high = round(100 * (df.high[i] / last_close - 1), 2)
        p_low = round(100 * (df.low[i] / last_close - 1), 2)
        p_open = round(100 * (df.open[i] / last_close - 1), 2)
        p_change = round(100 * (df.close[i] / last_close - 1), 2)
        swing = round(p_high - p_low, 2)
        up = round(p_change[i] - p_open, 2)
        l_p_high.append(p_high)
        l_p_low.append(p_low)
        l_p_open.append(p_open)
        l_swing.append(swing)
        l_up.append(up)
    l_p_high.append(0)
    l_p_low.append(0)
    l_p_open.append(0)
    l_swing.append(0)
    l_up.append(0)
    df['p_high'] = l_p_high
    df['p_low'] = l_p_low
    df['p_open'] = l_p_open
    df['swing'] = l_swing
    df['up'] = l_up
