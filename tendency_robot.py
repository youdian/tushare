from bs4 import BeautifulSoup
from sql import engine
import urllib.request


url = input('please input url:')
response = urllib.request.urlopen(url)
content = response.read()
document = BeautifulSoup(content)
a_list = document.find_all('a')
length = len(a_list)
li = []
for i in range(1, length):
    a = a_list[i]
    print(a)
    href = a['href']
    string = a.string
    index1 = string.index(' ')
    index2 = string.rindex(' ')
    code = string[:index1]
    name = string[index1 + 1: index2].strip()
    price = string[index2 + 1:]
    li.append((code, name, price, href))
print(li)

save = input('save data? yes/no:')
if save == 'yes':
    create_table_sql = 'create table if not exists up_robot(id int  auto_increment, code varchar(50), name varchar(50), price double, href text, primary key(id))'
    engine.execute(create_table_sql)
    for i in li:
        insert_sql = "insert into up_robot(code, name,price,href) values ('{0}', '{1}',{2},'{3}')".format(i[0], i[1], i[2], i[3])
        engine.execute(insert_sql)
    


