from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:u5412sql@10.66.155.192:3306/tushare?charset=utf8')

db_session = sessionmaker(bind=engine)


