class Stock:
  code = '' #代码
  name = '' #名称
  industry = '' #所属行业
  area = ''  #地区
  pe = 0.0  #市盈率
  outstanding = 0.0 #流通股本
  totals = 0.0 #总股本（万）
  totalAssets = 0.0 #总资产（万）
  liquidAssets = 0.0 #流动资产
  fixedAssets = 0.0 #固定资产
  reserved = 0.0 #公积金
  reservedPerShare = 0.0 #每股公积金
  esp = 0.0 #每股收益
  bvps = 0.0 #每股净资
  pb = 0.0 #市净率
  timeToMarket = '' #上市日期

if __name__ == '__main__':
  stock = Stock()
  stock.code = '600848'
