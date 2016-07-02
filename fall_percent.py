
l_count = [100]
l_price = []
def calc(ratio=2, percent=0.1, count =5, init_price = 100):
	l_price.append(init_price)
	for i in range(1, count + 1):
		count = l_count[i-1] * ratio
		l_count.append(count)
		price = l_price[i-1] * (1-percent)
		l_price.append(price)
		total_count = sum(l_count)
		total_value = 0
		for j in range(0, i + 1):
			total_value += l_count[j] * l_price[j]
		avg_price = total_value / total_count
		extra_price = avg_price / price - 1
		print('extra_price', extra_price)
		fall_percent = 1 - price / init_price
		print('当前价格:', round(price,2), '持股数量:', total_count, '平均持股价格:', round(avg_price,2), '盈亏涨幅:', str(round(extra_price * 100,2)) + '%', '跌幅:', str(round(fall_percent * 100,2)) + '%')


def custom_calc(ratio, price, l =[], c = []):
	if len(l) == 0:
		l.append(price)
		c.append(100)
		print('初始价格:', price, '买入数量:', str(100))
	else:
		l.append(price)
		init_price = l[0]
		fall_percent = (price - init_price) / init_price
		count = c[-1]* ratio
		c.append(count)
		total_count =  sum(c)
		level = len(l)
		total_price = 0
		for i in range(level):
			total_price += l[i] * c[i]
		avg_price = total_price / total_count
		even_percent = (avg_price - price) / price
		print('加仓价格', price, '持仓成本', round(avg_price,2), '买入数量:', total_count, '平仓涨幅',\
		str(round(even_percent* 100, 2)) + '%', '涨幅:', str(round(fall_percent * 100, 2)) + '%')
	
	
if __name__ == '__main__':
	
	ratio = input('input ratio:')
	if ratio == '':
		ratio = '2'
	while True:
		price = input('input current price:')
		if price == '':
			break
		custom_calc(float(ratio), float(price))
	#calc(float(ratio), float(percent), 8, float(price))
