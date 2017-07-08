from datetime import datetime
import sys
import time
import pandas as pd
def  transform(d):
  date = datetime.strptime(d, '%Y/%m/%d')
  return date.strftime('%Y-%m-%d')


if __name__ == '__main__':
  df = pd.read_csv('calAll.csv')
  d = df.calendarDate
  fd = [transform(i) for i in d]
  df['date'] = fd
  df.to_csv('calAll_1.csv')
