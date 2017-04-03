function init(e) {
    var list = new Vue({
        el: '#list',
        data: {
            items: [
                { "code": '000002', "name": "万科A" }
            ],
            selected: 0
        },
        methods: {
            requestPolicy: function (name) {
                console.log("requst " + name);
                let host = "127.0.0.1";
                let port = "8000";
                let url = "http://" + host + ":" + port + "/policy/" + name;
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
                this.selected = index;
                requestData(item.code);
            }
        }
    })
    var button = document.getElementById('submit');
    button.addEventListener('click', searchData);

    function searchData() {
        let codeInput = document.getElementById('code');
        let code = codeInput.value;
        requestData(code);
    }
    function requestData(code) {
        console.log("start request " + code);
        let host = "127.0.0.1";
        let port = "8000";
        let url = "http://" + host + ":" + port + "/history/" + code;
        axios.get(url)
            .then(function (response) {
                console.log(response)
                fillChart(response.data);
            })
            .catch(function (error) {
                console.log(error);
            });

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

    function fillChart(rawData) {
        var myChart = echarts.init(document.getElementById('chart'));
        var data = splitData(rawData);
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
        if (values == false || values.length <=1) {
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