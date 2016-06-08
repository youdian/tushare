import tushare as ts
import sys
from sql import engine
import sql
from history import saveHistory
import time

session = sql.db_session()
resultProxy = session.execute('select code, name from stock_list')
for row in resultProxy:
	code = row.code
	try:
		saveHistory(code)
	except:
		print('error loading code %s' %code)
	time.sleep(2)
		