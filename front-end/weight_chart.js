

function create_echart(date, weight) {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.getElementById('weight_echarts'));
  let max = Math.max.apply(null, weight)
  let min = Math.min.apply(null, weight)
  // 指定图表的配置项和数据
  var option = {
    title: {
      text: '近期体重变化',
      // subtext: '一月'
    },
    tooltip: {
      trigger: 'axis'
    },
    toolbox: {
      show: true,
      feature: {
        dataZoom: {
          yAxisIndex: 'none'
        },
        dataView: { readOnly: false },
        magicType: { type: ['line', 'bar'] },
        restore: {},
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: date,
    },
    yAxis: {
      type: 'value',
      position: 'left',
      // name: 'weight',
      min: Math.floor(min) ,
      max: Math.ceil(max)
    },
    series: [{
      data: weight,
      type: 'line',
      markPoint: {
        data: [
          { type: 'max', name: '最大值' },
          { type: 'min', name: '最小值' }
        ]
      },
      markLine: {
        data: [
          { type: 'average', name: '平均值' }
        ]
      }
    }]
  };

  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option);
  return myChart
}

function get_data(api) {
  let ret_val = 0;

  $.get({
    url: url + api,
    async: false,
    success: function (data, status) {
      data = jQuery.parseJSON(data)
      ret_val = data

      if (status == 400) {
        alert(data)
      }

    }
  })
  return ret_val

}

function post_data(api, form_data) {

  $.post(
    {
      url: url + api,
      data: form_data,
      processData: false,
      contentType: false,
      success: function (data, staus) {
        location.reload();
        if (status == 400) {
          alert(data)
        }
      }
    })

}