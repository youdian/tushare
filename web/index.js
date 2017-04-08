function init(e) {
    var stock = new Vue({
        el: '#stock',
        data: {
            policies: [
                { "name": "hot", "desc": "最近10天内某天涨幅大于3%" },
                { "name": "new", "desc": "次新股" },
                { "name": "still", "desc": "最近几天成交量显著降低" }
            ],
            items: [
                { "code": '000002', "name": "万科A" },
                { "code": "603833", "name": "欧派家居" }
            ],
            selected_stock: -1,
            selected_policy: -1,
            realtime: {
                "open": 12,
                "now": 13,
                "high": 15,
                "low": 10
            },
            bids: [
            ]
        },
        methods: {
            requestPolicy: function (policy, index) {
                console.log("requst " + policy.name);
                this.selected_policy = index;
                let host = "127.0.0.1";
                let port = "8000";
                let url = "http://" + host + ":" + port + "/policy/" + policy.name;
                axios.get(url)
                    .then(function (response) {
                        console.log(response)
                        let data = response.data;
                        this.items = data;
                    }.bind(this))
                    .catch(function (error) {
                        console.log(error);
                    });
            },
            show: function (item, index) {
                console.log(item);
                console.log(index);
                this.selected_stock = index;
                requestData(item.code);
            }
        }
    })
    let intervalId = 0;
    var button = document.getElementById('submit');
    button.addEventListener('click', searchData);

    function searchData() {
        let codeInput = document.getElementById('code');
        let code = codeInput.value;
        requestData(code);
    }
    function requestData(code) {
        if (intervalId !== 0) {
            clearInterval(intervalId);
        }
        console.log("start request " + code);
        let host = "127.0.0.1";
        let port = "8000";
        let url = "http://" + host + ":" + port + "/history/" + code;
        axios.get(url)
            .then(function (response) {
                console.log(response)
                var data = splitData(response.data);
                fillChart(data);
                intervalId = setInterval(function () {
                    requestRealtimeData(data, code);
                }, 3000);
            })
            .catch(function (error) {
                console.log(error);
            });

    }

    function requestRealtimeData(historyData, code) {
        // setInterval
        let host = "127.0.0.1";
        let port = "8000";
        let url = "http://" + host + ":" + port + "/realtime/" + code;
        axios.get(url)
            .then(function (response) {
                console.log(response)
                let data = JSON.parse(response.data);
                let realtime = {
                    "open": data.open["0"],
                    "now": data.price["0"],
                    "high": data.high["0"],
                    "low": data.low["0"]
                }
                let bids = [
                    { "name": "卖5", "price": data.a5_p["0"], "amount": data.a5_v["0"] },
                    { "name": "卖4", "price": data.a4_p["0"], "amount": data.a4_v["0"] },
                    { "name": "卖3", "price": data.a3_p["0"], "amount": data.a3_v["0"] },
                    { "name": "卖2", "price": data.a2_p["0"], "amount": data.a2_v["0"] },
                    { "name": "卖1", "price": data.a1_p["0"], "amount": data.a1_v["0"] },
                    { "name": "买1", "price": data.b1_p["0"], "amount": data.b1_v["0"] },
                    { "name": "买2", "price": data.b2_p["0"], "amount": data.b2_v["0"] },
                    { "name": "买3", "price": data.b3_p["0"], "amount": data.b3_v["0"] },
                    { "name": "买4", "price": data.b4_p["0"], "amount": data.b4_v["0"] },
                    { "name": "买5", "price": data.b5_p["0"], "amount": data.b5_v["0"] }
                ]
                stock.realtime = realtime;
                stock.bids = bids;
                updateKLine(historyData, data)
            })
            .catch(function (error) {

            });
    }

    function updateKLine(historyData, updateData) {
        let categoryData = historyData.categoryData;
        let count = categoryData.length
        let last_date = categoryData[count - 1];
        let update_date = updateData.date["0"];
        let value = [updateData.open["0"], updateData.price["0"], updateData.low["0"], updateData.high["0"]];
        let volume = updateData.volume["0"];
        if (last_date === update_date) {
            historyData.values[count - 1] = value;
            historyData.volumns[count - 1] = volume;
        } else {
            historyData.categoryData.push(update_date);
            historyData.values.push(value);
            historyData.volumns.push(volume);
        }
        fillChart
    }

    function splitData(rawData) {
        var j_data = JSON.parse(rawData);
        var categoryData = [];
        var datas = j_data['data'];
        var values = [];
        var volumns = []
        for (var i = 0; i < datas.length; i++) {
            let data = datas[i];
            let ordered_data = [data[1], data[2], data[4], data[3]];
            categoryData.push(data[0]);
            values.push(ordered_data);
            volumns.push(datas[i][5]);
        }
        return {
            categoryData: categoryData,
            values: values,
            volumns: volumns
        };
    }

    function getDefaultShowCount(array) {
        let count = array.length;
        let min = 200;
        return count - Math.min(count, min);
    }

    function fillChart(data) {
        var myChart = echarts.init(document.getElementById('stock_chart'));
        let red_color = "rgb(236, 0, 5)";
        let green_color = "rgb(21, 167, 2)";
        let def_color = "black";
        let def_show_count = getDefaultShowCount(data.categoryData);
        myChart.setOption(option = {
            backgroundColor: '#eee',
            animation: false,
            legend: {
                bottom: 10,
                left: 'center',
                data: ['index', 'MA5', 'MA10', 'MA20', 'MA30']
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'line'
                },
                backgroundColor: "rgba(255, 255, 255, 0.8)",
                borderColor: def_color,
                textStyle: {
                    color: def_color
                },
                formatter: function (params) {
                    let data_index = params[0].dataIndex;
                    let last_data_index = data_index - 1;
                    let open = data.values[data_index][0];
                    let close = data.values[data_index][1];
                    let low = data.values[data_index][2];
                    let high = data.values[data_index][3];
                    let volume = data.volumns[data_index];
                    let color_open = def_color;
                    let color_close = def_color;
                    let color_low = def_color;
                    let color_high = def_color;
                    function color(p) {
                        if (p > 0) {
                            return red_color;
                        } else if (p < 0) {
                            return green_color;
                        } else {
                            return def_color;
                        }
                    }
                    if (last_data_index >= 0) {
                        let last_close = data.values[last_data_index][1];
                        if (last_close > 0) {
                            let p_open = (open / last_close - 1) * 100;
                            let p_close = (close / last_close - 1) * 100;
                            let p_low = (low / last_close - 1) * 100;
                            let p_high = (high / last_close - 1) * 100;
                            open += "(" + p_open.toFixed(2) + "%)";
                            close += "(" + p_close.toFixed(2) + "%)";
                            low += "(" + p_low.toFixed(2) + "%)";
                            high += "(" + p_high.toFixed(2) + "%)";
                            color_open = color(p_open);
                            color_close = color(p_close);
                            color_low = color(p_low);
                            color_high = color(p_high);
                        }
                    }
                    return [
                        'Date: ' + params[0].name + '<hr size=1 style="margin: 3px 0">',
                        '开盘: <strong style="color:' + color_open + '">' + open + '</strong><br/>',
                        '收盘: <strong style="color:' + color_close + '">' + close + '</strong><br/>',
                        '最低: <strong style="color:' + color_low + '">' + low + '</strong><br/>',
                        '最高: <strong style="color:' + color_high + '">' + high + '</strong><br/>',
                        '成交量: ' + (volume / 10000).toFixed(2) + '万手<br/>'
                    ].join('');
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: false
                    },
                    brush: {
                        type: ['lineX', 'clear']
                    }
                }
            },
            grid: [
                {
                    left: '10%',
                    right: '8%',
                    height: '50%'
                },
                {
                    left: '10%',
                    right: '8%',
                    top: '63%',
                    height: '16%'
                }
            ],
            xAxis: [
                {
                    type: 'category',
                    data: data.categoryData,
                    scale: true,
                    boundaryGap: false,
                    axisLine: { onZero: false },
                    splitLine: { show: false },
                    splitNumber: 20,
                    min: 'dataMin',
                    max: 'dataMax'
                },
                {
                    type: 'category',
                    gridIndex: 1,
                    data: data.categoryData,
                    scale: true,
                    boundaryGap: false,
                    axisLine: { onZero: false },
                    axisTick: { show: false },
                    splitLine: { show: false },
                    axisLabel: { show: false },
                    splitNumber: 20,
                    min: 'dataMin',
                    max: 'dataMax'
                }
            ],
            yAxis: [
                {
                    scale: true,
                    splitArea: {
                        show: true
                    }
                },
                {
                    scale: true,
                    gridIndex: 1,
                    splitNumber: 2,
                    axisLabel: { show: false },
                    axisLine: { show: false },
                    axisTick: { show: false },
                    splitLine: { show: false }
                }
            ],
            dataZoom: [
                {
                    type: 'inside',
                    xAxisIndex: [0, 1],
                    startValue: def_show_count,
                    end: 100
                },
                {
                    show: true,
                    xAxisIndex: [0, 1],
                    type: 'slider',
                    top: '85%',
                    startValue: def_show_count,
                    end: 100
                }
            ],
            series: [
                {
                    name: 'index',
                    type: 'candlestick',
                    data: customBarColor(data.values),
                    itemStyle: {
                        normal: {
                            color: red_color,
                            color0: green_color,
                            borderColor: null,
                            borderColor0: null
                        }
                    }
                },
                {
                    name: 'MA5',
                    type: 'line',
                    data: calculateMA(5, data),
                    smooth: true,
                    symbolSize: 0,
                    lineStyle: {
                        normal: { opacity: 0.5 }
                    }
                },
                {
                    name: 'MA10',
                    type: 'line',
                    data: calculateMA(10, data),
                    smooth: true,
                    symbolSize: 0,
                    lineStyle: {
                        normal: { opacity: 0.5 }
                    }
                },
                {
                    name: 'MA20',
                    type: 'line',
                    data: calculateMA(20, data),
                    smooth: true,
                    symbolSize: 0,
                    lineStyle: {
                        normal: { opacity: 0.5 }
                    }
                },
                {
                    name: 'MA30',
                    type: 'line',
                    data: calculateMA(30, data),
                    smooth: true,
                    symbolSize: 0,
                    lineStyle: {
                        normal: { opacity: 0.5 }
                    }
                },
                {
                    name: 'Volumn',
                    type: 'bar',
                    xAxisIndex: 1,
                    yAxisIndex: 1,
                    data: data.volumns,
                    itemStyle: {
                        normal: {
                            color: function (params) {
                                let dataIndex = params.dataIndex;
                                let day_data = data.values[dataIndex];
                                let day_open = day_data[0];
                                let day_close = day_data[1];
                                return day_close >= day_open ? red_color : green_color;
                            }
                        }
                    }
                }
            ]
        }, true);
    }

    function calculateMA(dayCount, data) {
        var result = [];
        for (var i = 0, len = data.values.length; i < len; i++) {
            if (i < dayCount) {
                result.push('-');
                continue;
            }
            var sum = 0;
            for (var j = 0; j < dayCount; j++) {
                sum += data.values[i - j][1];
            }
            result.push(+(sum / dayCount).toFixed(3));
        }
        return result;
    }

    function customBarColor(values) {
        if (values == false || values.length <= 1) {
            return;
        }
        let new_values = [];
        let len = values.length;
        let hot_limit = 0.03;
        new_values.push(values[0]);
        for (let i = 1; i < len; i++) {
            let close = values[i][1];
            let high = values[i][3];
            let last_close = values[i - 1][1];
            let hot = close / last_close - 1 >= hot_limit;
            if (hot) {
                let d = {
                    value: values[i],
                    itemStyle: {
                        normal: {
                            color: "blue",
                            color0: "blue"
                        }
                    }
                };
                new_values.push(d);
            } else {
                new_values.push(values[i]);
            }
        }
        return new_values;
    }
}
document.addEventListener('DOMContentLoaded', init);