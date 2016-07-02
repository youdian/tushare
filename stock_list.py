#获取所有股票列表

from sql import engine
import tushare as ts

df = ts.get_stock_basics()

if df is not None:
    try:
        df.to_sql('stock_list', engine, if_exists='append')
    except:
        engine.execute('alter table stock_list add unique(code(20))')
        df.to_sql('stock_list', engine, if_exists='append')
