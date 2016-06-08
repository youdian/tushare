import tushare as ts
import sys
from sql import engine
import sql

def saveHistory(code):
	df = ts.get_hist_data(code)
	table_name = 's_' + code
	#先尝试清空表内容
	try:
		session = sql.db_session()
		session.execute('delete from ' + table_name)
	except:
		pass
	try:
		df.to_sql(table_name,engine, if_exists='append')
	except:
		session.execute("alter table " + table_name + " change 'date' 'date' text character set utf8 collate utf8_general_ci NULL default null" )
		session.close()
		df.to_sql(table_name, engine, if_exists='append')

code = sys.argv[1]
getHistory(code)