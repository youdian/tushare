function init(e) {
    console.log('content loaded');
    var stocks = "601020,002792,300516,300503,300500,603822,603101,300474,603798,002793,603861,002778,603520,300511,300502,002791,603608,603919,300513,300484,300519,603027,002796,603726,002788,002789,002801,002797,300518,603028,601127,603737,300506,300501,300510,603528,601611,002802,300508,002799,002798,603339,300505,002800,603377,300509,300515,603029,300499,002790,603868,300507,300512,603959,603779,603131,603701,002795,601900";
    var list = document.getElementById('list');
    var stock_list = stocks.split(',');
    var len = stock_list.length;
    for (var i=0;i<len;i++) {
        stock = stock_list[i];
        prefix = '';
        if (stock.substring(0,1) == '6') {
            prefix = 'sh';
        } else {
            prefix = 'sz';
        }
        var a = document.createElement('a');
        var url = 'http://finance.sina.com.cn/realstock/company/' + prefix + stock + '/nc.shtml'
        a.textContent = stock;
        a.href = url;
        list.appendChild(a);
        var br = document.createElement('br');
        list.appendChild(br);
    }
}
document.addEventListener('DOMContentLoaded', init);