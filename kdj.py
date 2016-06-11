import sql
from sqlalchemy import text
import sys
from sql import engine

def calcKDJ(code):
  conn = engine.connect()
  table_name = 's_' + code
  resultProxy = conn.execute('select * from ' + table_name + ' order by date desc')
  list = []
  for row in resultProxy:
    data = {'open':row.open, 'close':row.close,'high':row.high, 'low':row.low, 'date':row.date}
    list.append(data)
  print(len(list))
  if len(list) < 50:
    print('data too small, skip %s' %code)
    return False
  (k,d,j) = getKDJ(list, 0 ,9)
  offset = 4
  upward = True
  i=1
  while i <= offset:
    (k1,d1,j1)= getKDJ(list,i,9)
    if k1 < j1 or d1 < j1:
      upward = False
      break
    i +=1
  kj = abs((k-j)/j)
  dj = abs((d-j)/j)
  kd = abs((k-d)/d)
  #print('kj=%f,dj=%f' %(kj,dj))
  if kj < 0.1 and dj < 0.1 and kd < 0.1 and upward:
    print('code=%s,kj=%f, dj=%f,kd=%f, k=%f,d=%f,j=%f' %(code,kj,dj,kd,k,d,j))
    return True
  print('k=%f,d=%f,j=%f' %(k,d,j))
  return False
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
	(lastK, lastD, lastJ) = getKDJ(list, offset + 1, n)
	k = 2/3 * lastK + 1/3 * rsv
	d = 2/3 * lastD + 1/3 * k
	j = 3 * k - 2 * d
	return k,d,j 
if __name__  == '__main__':
  code = sys.argv[1]
  print('start calc')
  calcKDJ(code)
