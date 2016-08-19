import tushare as ts
import os
import pandas
import time

def fetch_history(stock):
    df = ts.get_hist_data(stock)
    if df is not None:
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
    df = pandas.read_csv('csv/stocks.csv', dtype={'code':str})
    for code in df.code:
        fetch_history(code)
        time.sleep(0.1)    
