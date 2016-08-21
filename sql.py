from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import ResultProxy

engine = create_engine('mysql+pymysql://root:usql123@localhost:3306/stock?charset=utf8')

db_session = sessionmaker(bind=engine)

