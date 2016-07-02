from sql import engine

stocks = engine.execute('select * from stock_list join hs300 on stock_list.code = hs300.code ')
