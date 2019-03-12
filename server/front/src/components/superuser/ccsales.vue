<template>
<div>
  <el-switch v-model="total" active-text="总体业绩" inactive-text="个人业绩" active-color="#66b1ffc2"
  inactive-color="#30313373"></el-switch>
  <div>
  <el-card shadow="hover" v-show="total === true">
    <el-button type="text" class="button" icon="el-icon-refresh
    "></el-button>
    <span>今日业绩</span>
    <el-row class="today">
        <el-col :span="3">{{total_today.flow_num}}</el-col>
        <el-col :span="3">{{total_today.audition_num}}</el-col>
        <el-col :span="3">{{total_today.audition_income}}</el-col>
        <el-col :span="3">{{total_today.signup_num}}</el-col>
        <el-col :span="3">{{total_today.signup_income}}</el-col>
        <el-col :span="3">{{total_today.audition_rate}}%</el-col>
        <el-col :span="3">{{total_today.signup_rate}}%</el-col>
    </el-row>
    <el-row class="todaydes">
        <el-col :span="3">邀约人数</el-col>
        <el-col :span="3">试听人数</el-col>
        <el-col :span="3">注册试听收入</el-col>
        <el-col :span="3">报名人数</el-col>
        <el-col :span="3">报名收入</el-col>
        <el-col :span="3">试听率</el-col>
        <el-col :span="3">试听报名率</el-col>
    </el-row>
  </el-card>
  <el-card shadow="hover" v-show="total === true">
    <el-button type="text" class="button" icon="el-icon-refresh
    "></el-button>
    <span>过去七天</span>
    <div id="total1">
    <div id="total_7days" style="width:1200px; height:500px"></div>
  </div>
  </el-card>
  <el-card shadow="hover" v-show="total === true">
    <el-button type="text" class="button" icon="el-icon-refresh
    "></el-button>
    <span>十二个月的业绩</span>
    <div id="total2">
    <div id="total_month" style="width:1200px; height:500px"></div>
  </div>
  </el-card>
  <el-card shadow="hover" v-show="total === true">
    <el-button type="text" class="button" icon="el-icon-refresh
    "></el-button>
    <span>近两年业绩</span>
    <div id="total3">
    <div id="total_year" style="width:1200px; height:500px"></div>
  </div>
  </el-card>
  </div>
  <div>
  <el-form :inline="true" :model="form" v-show="total !== true">
  <el-form-item label="地推姓名">
    <el-input v-model="form.username" placeholder="姓名"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="checkpeerinfo()">查询</el-button>
  </el-form-item>
  </el-form>
  <el-card shadow="hover" v-show="total !== true">
    <el-button type="text" class="button" icon="el-icon-refresh
    "></el-button>
    <span>今日业绩</span>
    <el-row class="today">
        <el-col :span="3">{{total_today.flow_num}}</el-col>
        <el-col :span="3">{{total_today.audition_num}}</el-col>
        <el-col :span="3">{{total_today.audition_income}}</el-col>
        <el-col :span="3">{{total_today.signup_num}}</el-col>
        <el-col :span="3">{{total_today.signup_income}}</el-col>
        <el-col :span="3">{{total_today.audition_rate}}%</el-col>
        <el-col :span="3">{{total_today.signup_rate}}%</el-col>
    </el-row>
    <el-row class="todaydes">
        <el-col :span="3">邀约人数</el-col>
        <el-col :span="3">试听人数</el-col>
        <el-col :span="3">注册试听收入</el-col>
        <el-col :span="3">报名人数</el-col>
        <el-col :span="3">报名收入</el-col>
        <el-col :span="3">试听率</el-col>
        <el-col :span="3">试听报名率</el-col>
    </el-row>
  </el-card>
  <el-card shadow="hover" v-show="total !== true">
    <span>过去七天</span>
    <div id="peer1">
    <div id="peer_7days" style="width:1200px; height:500px"></div>
  </div>
  </el-card>
  <el-card shadow="hover" v-show="total !== true">
    <span>本月业绩</span>
    <div id="peer2">
    <div id="peer_month" style="width:1200px; height:500px"></div>
  </div>
  </el-card>
  <el-card shadow="hover" v-show="total !== true">
    <span>本年业绩</span>
    <div id="peer3">
    <div id="peer_year" style="width:1200px; height:500px"></div>
  </div>
  </el-card>
  </div>
</div>
</template>
<style scoped>
.today {
  font-size: 25px;
  text-align: center;
}
.todaydes {
  text-align: center;
}
.el-card {
  margin: 20px;
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
import DIC from '@/dictionary.json';

const echarts = require('echarts');

export default {
  data() {
    return {
      total: true,
      lastyear: [],
      thisyear: [],
      week: [],
      week_flow_num: [],
      week_audition_num: [],
      week_audition_income: [],
      week_signup_num: [],
      week_signup_income: [],
      week_audition_rate: [],
      week_signup_rate: [],
      month: [],
      month_flow_num: [],
      month_audition_num: [],
      month_audition_income: [],
      month_signup_num: [],
      month_signup_income: [],
      month_audition_rate: [],
      month_signup_rate: [],
      peername: '',
      form: {
        username: '',
      },
      total_today: {
        flow_num: 1,
        audition_num: 2,
        audition_income: 3,
        signup_num: 4,
        signup_income: 5,
        audition_rate: '100%',
        signup_rate: '80%',
      },
      peer_today: {
        flow_num: 1,
        audition_num: 2,
        audition_income: 3,
        signup_num: 4,
        signup_income: 5,
        audition_rate: '100%',
        signup_rate: '80%',
      },
    };
  },
  methods: {
    checkpeerinfo() {
      this.peername = this.form.username;
      this.axios({
        method: 'post',
        url: 'data/today_cc_grades',
        data: {
          name: this.peername,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.peer_today = response.data;
          this.$options.methods.checkpeerToday(this);
          this.$options.methods.checkpeer7days(this);
          this.$options.methods.checkpeermonth(this);
          this.$options.methods.checkpeeryear(this);
        } else {
          this.$message.error('用户名不存在!');
        }
      });
    },
    checkTotalToday() {
      this.axios({
        method: 'post',
        url: 'data/today_cc_grades',
        data: {
          name: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        this.total_today = response.data;
      });
    },
    checkpeerToday(a) {
      const that = a;
      that
        .axios({
          method: 'post',
          url: 'data/today_cc_grades',
          data: {
            name: that.peername,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        })
        .then((response) => {
          if (response.data.error === DIC.STATUS_CODE.Success) {
            that.peer_today = response.data;
          } else {
            that.$message.error('用户名不存在!');
          }
        });
    },
    checktotalmonth() {
      this.axios({
        method: 'post',
        url: 'data/months_cc_grades',
        data: {
          name: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.list[0].error === DIC.STATUS_CODE.Success) {
          for (let i = 0; i < response.data.list.length; i += 1) {
            this.month_flow_num[i] = response.data.list[i].flow_num;
            this.month_audition_num[i] = response.data.list[i].audition_num;
            this.month_audition_income[i] =
              response.data.list[i].audition_income;
            this.month_signup_num[i] = response.data.list[i].signup_num;
            this.month_signup_income[i] = response.data.list[i].signup_income;
            this.month_audition_rate[i] = response.data.list[i].audition_rate;
            this.month_signup_rate[i] = response.data.list[i].signup_rate;
            this.month[i] = i + 1;
          }
          const colors = [
            '#5793f3',
            '#d14a61',
            '#675bba',
            '#ffd85c',
            '#67c23a',
            '#1b7070',
            '#ef00b8',
          ];
          const totalmonthChart = echarts.init(
            document.getElementById('total_month'),
          );
          totalmonthChart.resize();
          totalmonthChart.setOption({
            color: colors,
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'cross',
              },
            },
            grid: {
              right: '20%',
            },
            toolbox: {
              feature: {
                dataView: { show: true, readOnly: false },
                restore: { show: true },
                saveAsImage: { show: true },
              },
            },
            legend: {
              data: [
                '邀约人数',
                '试听人数',
                '注册试听收入',
                '报名人数',
                '报名收入',
                '试听率',
                '试听报名率',
              ],
            },
            xAxis: [
              {
                type: 'category',
                axisTick: {
                  alignWithLabel: true,
                },
                data: this.month,
              },
            ],
            yAxis: [
              {
                type: 'value',
                name: '邀约人数',
                min: 0,
                max: 150,
                position: 'right',
                axisLine: {
                  lineStyle: {
                    color: colors[0],
                  },
                },
                axisLabel: {
                  formatter: '{value} 人',
                },
              },
              {
                type: 'value',
                name: '试听人数',
                min: 0,
                max: 150,
                position: 'left',
                axisLine: {
                  lineStyle: {
                    color: colors[1],
                  },
                },
                axisLabel: {
                  formatter: '{value} 人',
                },
              },
              {
                type: 'value',
                name: '注册试听收入',
                min: 0,
                max: 4000,
                position: 'left',
                offset: 65,
                axisLine: {
                  lineStyle: {
                    color: colors[2],
                  },
                },
                axisLabel: {
                  formatter: '{value} 元',
                },
              },
              {
                type: 'value',
                name: '报名人数',
                min: 0,
                max: 150,
                position: 'right',
                offset: 60,
                axisLine: {
                  lineStyle: {
                    color: colors[3],
                  },
                },
                axisLabel: {
                  formatter: '{value} 人',
                },
              },
              {
                type: 'value',
                name: '报名收入',
                min: 0,
                max: 250000,
                position: 'right',
                offset: 130,
                axisLine: {
                  lineStyle: {
                    color: colors[4],
                  },
                },
                axisLabel: {
                  formatter: '{value} 元',
                },
              },
              {
                type: 'value',
                name: '试听率',
                min: 0,
                max: 100,
                position: 'left',
                offset: 130,
                axisLine: {
                  lineStyle: {
                    color: colors[5],
                  },
                },
                axisLabel: {
                  formatter: '{value} %',
                },
              },
              {
                type: 'value',
                name: '试听报名率',
                min: 0,
                max: 100,
                position: 'right',
                offset: 195,
                axisLine: {
                  lineStyle: {
                    color: colors[6],
                  },
                },
                axisLabel: {
                  formatter: '{value} %',
                },
              },
            ],
            series: [
              {
                name: '邀约人数',
                type: 'bar',
                yAxisIndex: 0,
                data: this.month_flow_num,
              },
              {
                name: '试听人数',
                type: 'bar',
                yAxisIndex: 1,
                data: this.month_audition_num,
              },
              {
                name: '注册试听收入',
                type: 'bar',
                yAxisIndex: 2,
                data: this.month_audition_income,
              },
              {
                name: '报名人数',
                type: 'bar',
                yAxisIndex: 3,
                data: this.month_signup_num,
              },
              {
                name: '报名收入',
                type: 'bar',
                yAxisIndex: 4,
                data: this.month_signup_income,
              },
              {
                name: '试听率',
                type: 'line',
                yAxisIndex: 5,
                data: this.month_audition_rate,
              },
              {
                name: '试听报名率',
                type: 'line',
                yAxisIndex: 6,
                data: this.month_signup_rate,
              },
            ],
          });
        }
      });
    },
    checktotal7days() {
      this.axios({
        method: 'post',
        url: 'data/week_cc_grades',
        data: {
          name: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.list[0].error === DIC.STATUS_CODE.Success) {
          for (let i = 0; i < response.data.list.length; i += 1) {
            this.week_flow_num[i] = response.data.list[i].flow_num;
            this.week_audition_num[i] = response.data.list[i].audition_num;
            this.week_audition_income[i] =
              response.data.list[i].audition_income;
            this.week_signup_num[i] = response.data.list[i].signup_num;
            this.week_signup_income[i] = response.data.list[i].signup_income;
            this.week_audition_rate[i] = response.data.list[i].audition_rate;
            this.week_signup_rate[i] = response.data.list[i].signup_rate;
            this.week[i] = response.data.list[i].date;
          }
          const colors = [
            '#5793f3',
            '#d14a61',
            '#675bba',
            '#ffd85c',
            '#67c23a',
            '#1b7070',
            '#ef00b8',
          ];
          const totalweekChart = echarts.init(
            document.getElementById('total_7days'),
          );
          totalweekChart.resize();
          totalweekChart.setOption({
            color: colors,
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'cross',
              },
            },
            grid: {
              left: '20%',
              right: '25%',
            },
            toolbox: {
              feature: {
                dataView: { show: true, readOnly: false },
                restore: { show: true },
                saveAsImage: { show: true },
              },
            },
            legend: {
              data: [
                '邀约人数',
                '试听人数',
                '注册试听收入',
                '报名人数',
                '报名收入',
                '试听率',
                '试听报名率',
              ],
            },
            xAxis: [
              {
                type: 'category',
                axisTick: {
                  alignWithLabel: true,
                },
                data: this.week,
              },
            ],
            yAxis: [
              {
                type: 'value',
                name: '邀约人数',
                min: 0,
                max: 60,
                position: 'right',
                axisLine: {
                  lineStyle: {
                    color: colors[0],
                  },
                },
                axisLabel: {
                  formatter: '{value} 人',
                },
              },
              {
                type: 'value',
                name: '试听人数',
                min: 0,
                max: 60,
                position: 'left',
                axisLine: {
                  lineStyle: {
                    color: colors[1],
                  },
                },
                axisLabel: {
                  formatter: '{value} 人',
                },
              },
              {
                type: 'value',
                name: '注册试听收入',
                min: 0,
                max: 1000,
                position: 'left',
                offset: 65,
                axisLine: {
                  lineStyle: {
                    color: colors[2],
                  },
                },
                axisLabel: {
                  formatter: '{value} 元',
                },
              },
              {
                type: 'value',
                name: '报名人数',
                min: 0,
                max: 60,
                position: 'right',
                offset: 60,
                axisLine: {
                  lineStyle: {
                    color: colors[3],
                  },
                },
                axisLabel: {
                  formatter: '{value} 人',
                },
              },
              {
                type: 'value',
                name: '报名收入',
                min: 0,
                max: 100000,
                position: 'right',
                offset: 130,
                axisLine: {
                  lineStyle: {
                    color: colors[4],
                  },
                },
                axisLabel: {
                  formatter: '{value} 元',
                },
              },
              {
                type: 'value',
                name: '试听率',
                min: 0,
                max: 100,
                position: 'left',
                offset: 130,
                axisLine: {
                  lineStyle: {
                    color: colors[5],
                  },
                },
                axisLabel: {
                  formatter: '{value} %',
                },
              },
              {
                type: 'value',
                name: '试听报名率',
                min: 0,
                max: 100,
                position: 'right',
                offset: 195,
                axisLine: {
                  lineStyle: {
                    color: colors[6],
                  },
                },
                axisLabel: {
                  formatter: '{value} %',
                },
              },
            ],
            series: [
              {
                name: '邀约人数',
                type: 'bar',
                yAxisIndex: 0,
                data: this.week_flow_num,
              },
              {
                name: '试听人数',
                type: 'bar',
                yAxisIndex: 1,
                data: this.week_audition_num,
              },
              {
                name: '注册试听收入',
                type: 'bar',
                yAxisIndex: 2,
                data: this.week_audition_income,
              },
              {
                name: '报名人数',
                type: 'bar',
                yAxisIndex: 3,
                data: this.week_signup_num,
              },
              {
                name: '报名收入',
                type: 'bar',
                yAxisIndex: 4,
                data: this.week_signup_income,
              },
              {
                name: '试听率',
                type: 'line',
                yAxisIndex: 5,
                data: this.week_audition_rate,
              },
              {
                name: '试听报名率',
                type: 'line',
                yAxisIndex: 6,
                data: this.week_signup_rate,
              },
            ],
          });
        }
      });
    },
    checktotalyear() {
      this.axios({
        method: 'post',
        url: 'data/years_cc_grades',
        data: {
          name: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.last_list[0].error === DIC.STATUS_CODE.Success) {
          this.lastyear[0] = response.data.last_list[0].flow_num;
          this.thisyear[0] = response.data.this_list[0].flow_num;
          this.lastyear[1] = response.data.last_list[0].audition_num;
          this.thisyear[1] = response.data.this_list[0].audition_num;
          this.lastyear[2] = response.data.last_list[0].audition_income;
          this.thisyear[2] = response.data.this_list[0].audition_income;
          this.lastyear[3] = response.data.last_list[0].signup_num;
          this.thisyear[3] = response.data.this_list[0].signup_num;
          this.lastyear[4] = response.data.last_list[0].signup_income;
          this.thisyear[4] = response.data.this_list[0].signup_income;
          this.lastyear[5] = response.data.last_list[0].audition_rate;
          this.thisyear[5] = response.data.this_list[0].audition_rate;
          this.lastyear[6] = response.data.last_list[0].signup_rate;
          this.thisyear[6] = response.data.this_list[0].signup_rate;
          const totalyearChart = echarts.init(
            document.getElementById('total_year'),
          );
          totalyearChart.resize();
          totalyearChart.setOption({
            tooltip: {},
            legend: {
              data: ['去年业绩', '今年业绩'],
            },
            radar: {
              name: {
                textStyle: {
                  color: '#fff',
                  backgroundColor: '#999',
                  borderRadius: 3,
                  padding: [3, 5],
                },
              },
              indicator: [
                { name: '邀约人数', max: 600 },
                { name: '试听人数', max: 600 },
                { name: '注册试听收入', max: 20000 },
                { name: '报名人数', max: 500 },
                { name: '报名收入', max: 1000000 },
                { name: '试听率(百分比)', max: 100 },
                { name: '试听报名率(百分比)', max: 100 },
              ],
            },
            series: [
              {
                name: '去年业绩 vs 今年业绩',
                type: 'radar',
                data: [
                  {
                    value: this.lastyear,
                    name: '去年业绩',
                  },
                  {
                    value: this.thisyear,
                    name: '今年业绩',
                  },
                ],
              },
            ],
          });
        } else {
          this.$message.error('用户名不存在!');
        }
      });
    },
    checkpeer7days(a) {
      const that = a;
      that
        .axios({
          method: 'post',
          url: 'data/week_cc_grades',
          data: {
            name: that.peername,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        })
        .then((response) => {
          if (response.data.list[0].error === DIC.STATUS_CODE.Success) {
            for (let i = 0; i < response.data.list.length; i += 1) {
              that.week_flow_num[i] = response.data.list[i].flow_num;
              that.week_audition_num[i] = response.data.list[i].audition_num;
              that.week_audition_income[i] =
                response.data.list[i].audition_income;
              that.week_signup_num[i] = response.data.list[i].signup_num;
              that.week_signup_income[i] = response.data.list[i].signup_income;
              that.week_audition_rate[i] = response.data.list[i].audition_rate;
              that.week_signup_rate[i] = response.data.list[i].signup_rate;
              that.week[i] = response.data.list[i].date;
            }
            const colors = [
              '#5793f3',
              '#d14a61',
              '#675bba',
              '#ffd85c',
              '#67c23a',
              '#1b7070',
              '#ef00b8',
            ];
            const peerweekChart = echarts.init(
              document.getElementById('peer_7days'),
            );
            peerweekChart.resize();
            peerweekChart.setOption({
              color: colors,
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  type: 'cross',
                },
              },
              grid: {
                left: '20%',
                right: '20%',
              },
              toolbox: {
                feature: {
                  dataView: { show: true, readOnly: false },
                  restore: { show: true },
                  saveAsImage: { show: true },
                },
              },
              legend: {
                data: [
                  '邀约人数',
                  '试听人数',
                  '注册试听收入',
                  '报名人数',
                  '报名收入',
                  '试听率',
                  '试听报名率',
                ],
              },
              xAxis: [
                {
                  type: 'category',
                  axisTick: {
                    alignWithLabel: true,
                  },
                  data: this.week,
                },
              ],
              yAxis: [
                {
                  type: 'value',
                  name: '邀约人数',
                  min: 0,
                  max: 60,
                  position: 'right',
                  axisLine: {
                    lineStyle: {
                      color: colors[0],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 人',
                  },
                },
                {
                  type: 'value',
                  name: '试听人数',
                  min: 0,
                  max: 60,
                  position: 'left',
                  axisLine: {
                    lineStyle: {
                      color: colors[1],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 人',
                  },
                },
                {
                  type: 'value',
                  name: '注册试听收入',
                  min: 0,
                  max: 1000,
                  position: 'left',
                  offset: 65,
                  axisLine: {
                    lineStyle: {
                      color: colors[2],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 元',
                  },
                },
                {
                  type: 'value',
                  name: '报名人数',
                  min: 0,
                  max: 60,
                  position: 'right',
                  offset: 60,
                  axisLine: {
                    lineStyle: {
                      color: colors[3],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 人',
                  },
                },
                {
                  type: 'value',
                  name: '报名收入',
                  min: 0,
                  max: 100000,
                  position: 'right',
                  offset: 130,
                  axisLine: {
                    lineStyle: {
                      color: colors[4],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 元',
                  },
                },
                {
                  type: 'value',
                  name: '试听率',
                  min: 0,
                  max: 100,
                  position: 'left',
                  offset: 130,
                  axisLine: {
                    lineStyle: {
                      color: colors[5],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} %',
                  },
                },
                {
                  type: 'value',
                  name: '试听报名率',
                  min: 0,
                  max: 100,
                  position: 'right',
                  offset: 195,
                  axisLine: {
                    lineStyle: {
                      color: colors[6],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} %',
                  },
                },
              ],
              series: [
                {
                  name: '邀约人数',
                  type: 'bar',
                  yAxisIndex: 0,
                  data: that.week_flow_num,
                },
                {
                  name: '试听人数',
                  type: 'bar',
                  yAxisIndex: 1,
                  data: that.week_audition_num,
                },
                {
                  name: '注册试听收入',
                  type: 'bar',
                  yAxisIndex: 2,
                  data: that.week_audition_income,
                },
                {
                  name: '报名人数',
                  type: 'bar',
                  yAxisIndex: 3,
                  data: that.week_signup_num,
                },
                {
                  name: '报名收入',
                  type: 'bar',
                  yAxisIndex: 4,
                  data: that.week_signup_income,
                },
                {
                  name: '试听率',
                  type: 'line',
                  yAxisIndex: 5,
                  data: that.week_audition_rate,
                },
                {
                  name: '试听报名率',
                  type: 'line',
                  yAxisIndex: 6,
                  data: that.week_signup_rate,
                },
              ],
            });
          }
        });
    },
    checkpeermonth(a) {
      const that = a;
      that
        .axios({
          method: 'post',
          url: 'data/months_cc_grades',
          data: {
            name: that.peername,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        })
        .then((response) => {
          if (response.data.list[0].error === DIC.STATUS_CODE.Success) {
            for (let i = 0; i < response.data.list.length; i += 1) {
              that.month_flow_num[i] = response.data.list[i].flow_num;
              that.month_audition_num[i] = response.data.list[i].audition_num;
              that.month_audition_income[i] = response.data.list[i].audition_income;
              that.month_signup_num[i] = response.data.list[i].signup_num;
              that.month_signup_income[i] = response.data.list[i].signup_income;
              that.month_audition_rate[i] = response.data.list[i].audition_rate;
              that.month_signup_rate[i] = response.data.list[i].signup_rate;
              that.month[i] = i + 1;
            }
            const colors = [
              '#5793f3',
              '#d14a61',
              '#675bba',
              '#ffd85c',
              '#67c23a',
              '#1b7070',
              '#ef00b8',
            ];
            const peermonthChart = echarts.init(
              document.getElementById('peer_month'),
            );
            peermonthChart.resize();
            peermonthChart.setOption({
              color: colors,
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  type: 'cross',
                },
              },
              grid: {
                right: '20%',
              },
              toolbox: {
                feature: {
                  dataView: { show: true, readOnly: false },
                  restore: { show: true },
                  saveAsImage: { show: true },
                },
              },
              legend: {
                data: [
                  '邀约人数',
                  '试听人数',
                  '注册试听收入',
                  '报名人数',
                  '报名收入',
                  '试听率',
                  '试听报名率',
                ],
              },
              xAxis: [
                {
                  type: 'category',
                  axisTick: {
                    alignWithLabel: true,
                  },
                  data: that.month,
                },
              ],
              yAxis: [
                {
                  type: 'value',
                  name: '邀约人数',
                  min: 0,
                  max: 150,
                  position: 'right',
                  axisLine: {
                    lineStyle: {
                      color: colors[0],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 人',
                  },
                },
                {
                  type: 'value',
                  name: '试听人数',
                  min: 0,
                  max: 150,
                  position: 'left',
                  axisLine: {
                    lineStyle: {
                      color: colors[1],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 人',
                  },
                },
                {
                  type: 'value',
                  name: '注册试听收入',
                  min: 0,
                  max: 4000,
                  position: 'left',
                  offset: 65,
                  axisLine: {
                    lineStyle: {
                      color: colors[2],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 元',
                  },
                },
                {
                  type: 'value',
                  name: '报名人数',
                  min: 0,
                  max: 150,
                  position: 'right',
                  offset: 65,
                  axisLine: {
                    lineStyle: {
                      color: colors[3],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 人',
                  },
                },
                {
                  type: 'value',
                  name: '报名收入',
                  min: 0,
                  max: 250000,
                  position: 'right',
                  offset: 130,
                  axisLine: {
                    lineStyle: {
                      color: colors[4],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} 元',
                  },
                },
                {
                  type: 'value',
                  name: '试听率',
                  min: 0,
                  max: 100,
                  position: 'left',
                  offset: 130,
                  axisLine: {
                    lineStyle: {
                      color: colors[5],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} %',
                  },
                },
                {
                  type: 'value',
                  name: '试听报名率',
                  min: 0,
                  max: 100,
                  position: 'right',
                  offset: 195,
                  axisLine: {
                    lineStyle: {
                      color: colors[6],
                    },
                  },
                  axisLabel: {
                    formatter: '{value} %',
                  },
                },
              ],
              series: [
                {
                  name: '邀约人数',
                  type: 'bar',
                  yAxisIndex: 0,
                  data: that.month_flow_num,
                },
                {
                  name: '试听人数',
                  type: 'bar',
                  yAxisIndex: 1,
                  data: that.month_audition_num,
                },
                {
                  name: '注册试听收入',
                  type: 'bar',
                  yAxisIndex: 2,
                  data: that.month_audition_income,
                },
                {
                  name: '报名人数',
                  type: 'bar',
                  yAxisIndex: 3,
                  data: that.month_signup_num,
                },
                {
                  name: '报名收入',
                  type: 'bar',
                  yAxisIndex: 4,
                  data: that.month_signup_income,
                },
                {
                  name: '试听率',
                  type: 'line',
                  yAxisIndex: 5,
                  data: that.month_audition_rate,
                },
                {
                  name: '试听报名率',
                  type: 'line',
                  yAxisIndex: 6,
                  data: that.month_signup_rate,
                },
              ],
            });
          }
        });
    },
    checkpeeryear(a) {
      const that = a;
      that
        .axios({
          method: 'post',
          url: 'data/years_cc_grades',
          data: {
            name: that.peername,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        })
        .then((response) => {
          if (response.data.last_list[0].error === DIC.STATUS_CODE.Success) {
            that.lastyear[0] = response.data.last_list[0].flow_num;
            that.thisyear[0] = response.data.this_list[0].flow_num;
            that.lastyear[1] = response.data.last_list[0].audition_num;
            that.thisyear[1] = response.data.this_list[0].audition_num;
            that.lastyear[2] = response.data.last_list[0].audition_income;
            that.thisyear[2] = response.data.this_list[0].audition_income;
            that.lastyear[3] = response.data.last_list[0].signup_num;
            that.thisyear[3] = response.data.this_list[0].signup_num;
            that.lastyear[4] = response.data.last_list[0].signup_income;
            that.thisyear[4] = response.data.this_list[0].signup_income;
            that.lastyear[5] = response.data.last_list[0].audition_rate;
            that.thisyear[5] = response.data.this_list[0].audition_rate;
            that.lastyear[6] = response.data.last_list[0].signup_rate;
            that.thisyear[6] = response.data.this_list[0].signup_rate;
            const peeryearChart = echarts.init(
              document.getElementById('peer_year'),
            );
            peeryearChart.resize();
            peeryearChart.setOption({
              tooltip: {},
              legend: {
                data: ['去年业绩', '今年业绩'],
              },
              radar: {
                name: {
                  textStyle: {
                    color: '#fff',
                    backgroundColor: '#999',
                    borderRadius: 3,
                    padding: [3, 5],
                  },
                },
                indicator: [
                  { name: '邀约人数', max: 600 },
                  { name: '试听人数', max: 600 },
                  { name: '注册试听收入', max: 20000 },
                  { name: '报名人数', max: 500 },
                  { name: '报名收入', max: 1000000 },
                  { name: '试听率(百分比)', max: 100 },
                  { name: '试听报名率(百分比)', max: 100 },
                ],
              },
              series: [
                {
                  name: '去年业绩 vs 今年业绩',
                  type: 'radar',
                  data: [
                    {
                      value: that.lastyear,
                      name: '去年业绩',
                    },
                    {
                      value: that.thisyear,
                      name: '今年业绩',
                    },
                  ],
                },
              ],
            });
          } else {
            that.$message.error('用户名不存在!');
          }
        });
    },
  },
  mounted() {
    this.checkTotalToday();
    this.checktotal7days();
    this.checktotalmonth();
    this.checktotalyear();
  },
};
</script>
