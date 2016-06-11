import history
from sql import engine
import time
import traceback

conn = engine.connect()
resultProxy = conn.execute('select code from stock_list')
results = resultProxy.fetchall()
total = len(results)
count = 0
for row in results:
  code = row.code
  count += 1
  try:
    history.saveHistory(code)
  except:
    print('save history %s failed' %code )
    traceback.print_exc()
  else:
    print('save {0} successful'.format(code))
  finally:
    print('current saved {0}, {1} left'.format(count, total - count))
  time.sleep(1)
