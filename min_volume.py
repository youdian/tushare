from stock import stock
from stock import history

stock_list = stock.get_stock_list()
stocks = stock_list.index
p_volume = []
day = 7
for stock in stocks:
	his = history.get_history(stock)
	if his is not None:
		volumes = his.volume
		length = len(volumes)
		if length < 10:
			continue
		previous = volumes[length-2]
		day = 0
		for i in range(length-3, -1 , -1):
			volume = volumes[i]
			if volume <= previous:
				break
			day += 1
		value = (stock, day)
		p_volume.append(value)
p_volume = sorted(p_volume, key = lambda a: a[1], reverse=True)
for i in p_volume:
	print(i)
