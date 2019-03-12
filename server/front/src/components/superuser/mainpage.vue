<template>
  <div>
    <el-card shadow="hover" class="mycard">
        <div id="mapContainer" class="maps"></div>
    </el-card>
  </div>
</template>
<style scoped>
.mycard {
  min-height: 800px;
}
.el-card {
  margin: auto;
}
.maps {
  width: 800px;
  height: 800px;
  margin: 20px 15% 0 15%;
}
.bread {
  margin: -20px -20px 10px -20px;
  height: 40px;
  border-left: 10px solid #48576a;
  background-color: white;
}
.el-breadcrumb {
  font-size: 16px;
  line-height: 3;
}
</style>
<script>
import { getCookie } from '@/utils/utils';
import 'echarts/map/js/china.js';

const echarts = require('echarts');

export default {
  data() {
    return {
      sellernum: [],
    };
  },
  methods: {
    getdata() {
      this.axios({
        method: 'post',
        url: 'data/get_seller_distribution',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        for (let i = 0; i < response.data.list.length; i += 1) {
          const temp = {};
          temp.name = response.data.list[i].city;
          temp.value = response.data.list[i].num;
          this.sellernum.push(temp);
        }
        const myChart = echarts.init(document.getElementById('mapContainer'));
        myChart.setOption({
          title: {
            text: 'seller分布',
            x: 'center',
          },
          tooltip: {
            trigger: 'item',
          },
          legend: {
            orient: 'vertical',
            x: 'left',
            data: ['seller数目'],
          },
          dataRange: {
            min: 0,
            max: 120,
            x: 'left',
            y: 'bottom',
            text: ['高', '低'],
            calculable: true,
          },
          toolbox: {
            show: true,
            orient: 'vertical',
            x: 'right',
            y: 'center',
            feature: {
              mark: { show: true },
              dataView: { show: true, readOnly: false },
              restore: { show: true },
              saveAsImage: { show: true },
            },
          },
          roamController: {
            show: true,
            x: 'right',
            mapTypeControl: {
              china: true,
            },
          },
          series: [
            {
              name: 'seller数目',
              type: 'map',
              mapType: 'china',
              roam: false,
              itemStyle: {
                normal: { label: { show: true } },
                emphasis: { label: { show: true } },
              },
              data: this.sellernum,
            },
          ],
        });
      });
    },
  },
  mounted() {
    this.getdata();
  },
};
</script>
