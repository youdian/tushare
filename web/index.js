function init(e) {
    var list = new Vue({
        el: '#list',
        data: {
            items: [
                { "code": '000002', "name": "万科A" }
            ]
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
            show: function(item) {
                console.log(item);
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

    function fillChart(rawData) {
        var myChart = echarts.init(document.getElementById('chart'));
        var data = splitData(rawData);
        let red_color = "rgb(236, 0, 5)";
        let green_color = "rgb(21, 167, 2)";
        myChart.setOption(option = {
            backgroundColor: '#eee',
            animation: false,
            legend: {
                bottom: 10,
                left: 'center',
                data: ['Dow-Jones index', 'MA5', 'MA10', 'MA20', 'MA30']
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'line'
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
                    start: 80,
                    end: 100
                },
                {
                    show: true,
                    xAxisIndex: [0, 1],
                    type: 'slider',
                    top: '85%',
                    start: 80,
                    end: 100
                }
            ],
            series: [
                {
                    name: 'Dow-Jones index',
                    type: 'candlestick',
                    data: data.values,
                    itemStyle: {
                        normal: {
                            color: red_color,
                            color0: green_color,
                            borderColor: null,
                            borderColor0: null
                        }
                    },
                    tooltip: {
                        formatter: function (param) {
                            var param = param[0];
                            return [
                                'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                                'Open: ' + param.data[0] + '<br/>',
                                'Close: ' + param.data[1] + '<br/>',
                                'Lowest: ' + param.data[2] + '<br/>',
                                'Highest: ' + param.data[3] + '<br/>'
                            ].join('');
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
                            color: function(params){
                                let dataIndex = params.dataIndex;
                                let day_data = data.values[dataIndex];
                                console.log(day_data);
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
}
document.addEventListener('DOMContentLoaded', init);