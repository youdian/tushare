import tushare as ts
from sql import engine

df = ts.get_concept_classified()
df.to_sql('concept', engine)
