from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:u5412sql@10.66.155.192:3306/tushare?charset=utf8')

db_session = sessionmaker(bind=engine)

def getCodeList():
  conn = engine.connect()
  resultProxy = conn.execute('select * from stock_list')
  list = []
  for row in resultProxy:
    code = row.code
    list.append(code)
  print('list size = %d' %len(list))
  return list
