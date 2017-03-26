''' update stock data after the market is closed'''
import stock
import history
stock_list = stock.fetch_stock_list()
if stock_list is not None:
    print("fetch stock list success")
    history.fetch_all()
else:
    print("fetch stock list failed")
