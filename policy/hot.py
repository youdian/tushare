from stock import stock
from stock import history
day = 10
min_count = 20
normal_p_change = 3
min_p_change = 2.5
min_p_high = 5
def get():
    stock_list = stock.get_stock_list()
    codes = stock_list.index
    l= []
    for code in codes:
        name = stock_list.loc[[code]]
        if st(name):
            continue
        market = history.get_history(code)
        if market is not None:
            if time(market) and k_close(market):
                l.append((code, name))
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
    valid = name.lower().startsWith(st)
    return valid