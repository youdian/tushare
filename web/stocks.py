result = open('result.txt', 'w')
sb = ''
with open('stocks.txt') as stocks:
    for line in stocks:
        stock = line[:6]
        sb += stock
        sb += ','
sb = sb.strip(',')
result.write(sb)
result.close()
