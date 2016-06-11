import sql
import kdj

code_list = sql.getCodeList()
list = []
for code in code_list:
  if kdj.calcKDJ(code):
    list.append(code)
print('right codes are listed below:')
for code in list:
  print(code)

