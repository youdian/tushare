import tushare as ts
import sys
from sql import engine
import sql

def saveHistory(code):
	df = ts.get_hist_data(code)
	if df is None:
		print('df is none, code= %s' %code)
		return
	table_name = 'z_' + code
	df.to_sql(table_name,engine, if_exists='append')
if __name__ == '__main__':
	code = sys.argv[1]
	saveHistory(code)
