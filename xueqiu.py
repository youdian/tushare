#从雪球网站获取股票信息
import httputils
from datetime import datetime

def get_stock_basics(stock):
    base_url = 'https://xueqiu.com/v4/stock/quote.json'
    prefix = 'SZ'
    if stock.startswith('6'):
        prefix = 'SH'
    stock = prefix + stock
    now_in_millis = int(datetime.now().timestamp() * 1000)
    params = {}
    params['code'] = stock
    params['_'] = str(now_in_millis)
    headers = build_headers()
    content = httputils.get(base_url, params, headers)
    if content is not None:
        f = open('xueqiu.csv', 'a')
        f.write(content)
    else:
        print(stock, '获取数据失败')






#访问雪球的headers
def build_headers():
    headers = {}
    headers['Host'] = 'xueqiu.com'
    headers['Cookie']='s=22uh12eqlo; xq_a_token=ed3a6f41cd40749a7026f25f4f3e936379e415ed; xq_r_token=d54ca76f529ff87e19b08c546ed16a464caa90ef; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1468770339; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1468770369; __utma=1.800355725.1468770351.1468770351.1468770351.1; __utmb=1.2.10.1468770351; __utmc=1; __utmz=1.1468770351.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    headers['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    headers['Upgrade-Insecure-Requests']='1'
    #headers['Accept-Encoding']='gzip, deflate, sdch'
    return headers
