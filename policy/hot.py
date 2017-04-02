from stock import stock
from stock import history
from datetime import datetime
from datetime import timedelta

day = 10
min_count = 20
normal_p_change = 3
min_p_change = 2.5
min_p_high = 5
last_trading_day = "2017-03-31"

def get():
    stock_list = stock.get_stock_list()
    codes = stock_list.index
    l= []
    for code in codes:
        name = stock_list.loc[[code]].name[0]
        if st(name):
            continue
        market = history.get_history(code)
        if market is not None:
            if time(market) and k_close(market):
                l.append({"code": code, "name": name})
    return l


def time(kdata):
    '''min record count'''
    return len(kdata) >= min_count

def k_close(kdata):
    count = len(kdata)
    for i in range(day):
        index = count - 1 - i
        p_change = kdata.p_change[index]
        p_high = kdata.p_high[index]
        if p_change >= normal_p_change or p_change >= min_p_change and p_high >= min_p_high:
            return True
    return False

def st(name):
    '''not a st stock'''
    st = "st"
    star_st = "*st";
    valid = name.lower().startswith(st) or name.lower().startswith(star_st)
    return valid

def updated(kdata):
    date = kdata.date[len(kdata) - 1]
    return date == lastTradingDate()

def lastTradingDate():
    now = datetime.now()
    delta = 0
    if now.weekday == 5:
        delta = 1
    elif now.weekday == 6:
        delta = 2
    elif now.hour < 16:
        delta = 1
    trading_day = now - timedelta(days=delta)
    format = '%Y-%m-%d'
    day_str = trading_day.strftime(format)
    return day_str

