import tushare as ts
import sys
from sql import engine
import sql
import time
import traceback

def dropTable(conn,table_name):
  try:
    conn.execute('drop table ' + table_name)
    print('drop table %s success' %table_name)
  except:
    pass

def createTable(conn, code):
  table_name = 'z_' + code
  create_sql = 'create table if not exists ' + table_name + r' (id int(11) not null  auto_increment, date text, open double, high double, close double, low double, volume double, price_change double,p_change double, ma5 double, ma10 double, ma20 double, v_ma5 double, v_ma10 double, v_ma20 double, turnover double, primary key (id))'
  conn.execute(create_sql)

if __name__ == '__main__':
  conn = engine.connect()
  resultProxy = conn.execute('select code, name from stock_list')
  for row in resultProxy:
    code = row.code
    try:
      createTable(conn, code)
    except:
      print('creata table %s failed' %code)
      traceback.print_exc()
  conn.close()	
