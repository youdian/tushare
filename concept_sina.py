#从新浪网获取股票对应的概念

import sql
import urllib.request as request
import json
from sql import engine
import time
import sys

def get_district(code):
    if code.startswith('60'):
        return 'sh'
    else:
        return 'sz'

def load_concept():
    code_list = sql.getCodeList()
    if code_list is None or len(code_list) == 0:
        print('code list is empty')
        raise ValueError('list is empty')
    base_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getSymbolGN?symbol='
    log = open('log/concept_sina.log', 'a')
    for code in code_list:
        time.sleep(0.06)
        district = get_district(code)
        url = base_url + district + code
        try:
            response = request.urlopen(url)
            if response.getcode() == 200:
                data = response.read()
                content = data.decode('gb2312')
                if content is not None and content != 'null':
                    content = content.replace('type', '"type"')
                    content = content.replace('name', '"name"')
                    l = json.loads(content)
                    if isinstance(l, list):
                        for d in l:
                            type_value = d['type']
                            name_value = d['name']
                            engine.execute('insert into stock_concept(code, type, type_name) values("' + code + '","' + type_value + '","'+ name_value + '")')          
        except Exception as e:
            print(code, 'request failed', e)
            log.write(code + '\n')

    log.close()

def query(concept):
    sql = 'select stock_concept.code, stock_list.name, stock_concept.type_name from stock_concept join stock_list on stock_concept.code=stock_list.code where stock_concept.code like "%' + concept + '%"'
    result = engine.execute(sql)
    l = []
    for row in result:
        l.append(str(row))
    print(l)
