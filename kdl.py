import sql
from sqlalchemy import text
import sys

code = sys.argv[1]
session = sql.db_session()
table_name= 's_' + code 
resultProxy  = session.execute('select * from ' +  table_name + ' order by date desc')
list=[]
for row in resultProxy:
	data = {'open':row.open, 'close':row.close,'high':row.high, 'low':row.low}
	list.append(data)
print(len(list))
def getKDJ(list, offset, n=9):
	if len(list) < offset + n:
		k = 50
		d = 50
		j = 3 * k - 2 * d
		return k,d,j
	nClose = list[offset]['close']
	nLow = 100000
	nHigh = 0
	for i in range(n):
		data = list[offset+i]
		low = data['low']
		if low < nLow:
			nLow = low
		high = data['high']
		if high > nHigh:
			nHigh = high
	rsv = (nClose - nLow) / (nHigh - nLow) * 100
	print('offset=%d, rsv=%f' %(offset, rsv))
	(lastK, lastD, lastJ) = getKDJ(list, offset + 1, n)
	k = 2/3 * lastK + 1/3 * rsv
	d = 2/3 * lastD + 1/3 * k
	j = 3 * k - 2 * d
	print('offset=%d,k=%f,d=%f,j=%f' %(offset,k,d,j))
	return k,d,j 
(k,d,j) = getKDJ(list,0,9)
print('k=%f,d=%f,j=%f' %(k,d,j))
