import tushare as ts
import os
import pandas
import numpy as np

def fetch_stock_list():
    df = ts.get_stock_basics()
    if df is not None:
        df = df.drop([code for code in df.index if df.timeToMarket[code]==0])
        df.to_csv(get_stock_path())
    return df
def get_stock_list():
    path = get_stock_path()
    df = None    
    if os.path.exists(path):
        df = pandas.read_csv(path,index_col=0, dtype={'code':np.object})
        df.index = [format_code(code) for code in df.index]
    else:
        df = fetch_stock_list()
    return df 

def get_stock_path():
    return 'csv/stocks.csv'

def format_code(code):
    length = len(str(code))
    if length < 6:
        s = '0' * (6 - length)
        s += str(code)
        return s
    return str(code)

