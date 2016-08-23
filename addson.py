import stock
import history
import pandas as pd


'''df增加最高值变化'''
def add_h_change(df):
  if df is None:
    return
  length = len(df)
  l_high = []
  for i in range(length):
    high = df.high[df.index[i]]
    h_change = 0
    if i < length - 1:
      close = df.close[df.index[i + 1]]
      h_change = high / close - 1
    l_high.append(round(h_change*100, 2))
  df['h_change']= pd.Series(l_high, index=df.index)
       
