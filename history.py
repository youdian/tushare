import tushare as ts
import sys
from sql import engine
import sql

code = sys.argv[1]

df = ts.get_hist_data(code)
table_name = 's_' + code
try:
	df.to_sql(table_name,engine, if_exists='append')
except:
	session = sql.db_session()
	session.execute("alter table " + table_name + " change 'date' 'date' text character set utf8 collate utf8_general_ci NULL default null" )
	session.close()
	df.to_sql(table_name, engine, if_exists='append')
