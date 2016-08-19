import stock
import history

def p_range(day=3,_min=-0.1, _max=0.1):
  stocks = stock.get_stock_list()
  for stock in stocks.index:
    his = history.get_history(stock)
    if his is not None and his.size >= day:
      n_his = his.head(day)
      plist = n_his.p_change
            
