import tushare as ts
from sql import engine
df = ts.get_today_all()

df.to_sql('today', engine)
