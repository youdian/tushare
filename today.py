import tushare as ts
from sql import engine
df = ts.get_today_all()
if df is not None:
    engine.execute('delete from today;')
    df.to_sql('today', engine, if_exists='append')
