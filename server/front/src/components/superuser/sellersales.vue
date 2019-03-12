<template>
  <div>
    <el-switch v-model="total" active-text="总体业绩" inactive-text="个人业绩"
    active-color="#66b1ffc2"
    inactive-color="#30313373">
    </el-switch>
    <div>
      <el-card shadow="hover" v-show="total === true"
      v-loading="todayloading"
      element-loading-text="加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)">
        <el-button type="text" class="button" @click="checkTotalToday()" icon="el-icon-refresh
        "></el-button>
        <span>今日业绩</span>
        <el-row class="today">
          <el-col :span="5">{{total_today.audition_count}}</el-col>
          <el-col :span="5">{{total_today.audition_income}}</el-col>
          <el-col :span="5">{{total_today.entered_count}}</el-col>
          <el-col :span="5">{{total_today.entered_income}}</el-col>
        </el-row>
        <el-row class="todaydes">
          <el-col :span="5">试听人数</el-col>
          <el-col :span="5">注册试听收入</el-col>
          <el-col :span="5">报名人数</el-col>
          <el-col :span="5">报名收入</el-col>
        </el-row>
      </el-card>
    <el-card shadow="hover" v-show="total === true"
      v-loading="weekloading"
      element-loading-text="加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)">
      <el-button type="text" class="button" icon="el-icon-refresh"
      @click="checktotal7days()"></el-button>
      <span>过去七天业绩</span>
      <div id="total1">
        <div id="total_7days" style="width:1000px; height:500px">
        </div>
      </div>
    </el-card>
    <el-card shadow="hover" v-show="total === true"
    v-loading="monthloading"
      element-loading-text="加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)">
      <el-button type="text" class="button" icon="el-icon-refresh"
      @click="checktotalmonth()"></el-button>
      <span>月销售业绩</span>
      <div id="total2">
      <div id="total_month" style="width:1000px; height:500px"></div>
    </div>
    </el-card>
    <el-card shadow="hover" v-show="total === true"
      v-loading="yearloading"
      element-loading-text="加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)">
      <el-button type="text" class="button" icon="el-icon-refresh"
      @click="checktotalyear()"></el-button>
      <span>两年业绩对比</span>
      <div id="total3">
      <div id="total_year" style="width:1000px; height:500px"></div>
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
      <el-button type="text" class="button" @click="checkpeerToday()" icon="el-icon-refresh
      "></el-button>
      <span>今日业绩</span>
      <el-row class="today">
          <el-col :span="5">{{peer_today.today_sellcount}}</el-col>
          <el-col :span="5">{{peer_today.today_sellmoney}}</el-col>
          <el-col :span="5">{{peer_today.today_signcount}}</el-col>
          <el-col :span="5">{{peer_today.today_signmoney}}</el-col>
      </el-row>
      <el-row class="todaydes">
          <el-col :span="5">试听人数</el-col>
          <el-col :span="5">注册试听收入</el-col>
          <el-col :span="5">报名人数</el-col>
          <el-col :span="5">报名收入</el-col>
      </el-row>
    </el-card>
    <el-card shadow="hover" v-show="total !== true"
    v-loading="myweekloading"
      element-loading-text="加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)">
      <span>过去七天业绩</span>
      <div id="peer1">
      <div id="peer_7days" style="width:1000px; height:500px"></div>
    </div>
    </el-card>
    <el-card shadow="hover" v-show="total !== true"
      v-loading="mymonthloading"
      element-loading-text="加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)">
      <span>月销售业绩</span>
      <div id="peer2">
      <div id="peer_month" style="width:1000px; height:500px"></div>
    </div>
    </el-card>
    <el-card shadow="hover" v-show="total !== true"
    v-loading="myyearloading"
      element-loading-text="加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)">
      <span>两年业绩对比</span>
      <div id="peer3">
      <div id="peer_year" style="width:1000px; height:500px"></div>
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
      todayloading: false,
      weekloading: false,
      monthloading: false,
      yearloading: false,
      myweekloading: true,
      mymonthloading: false,
      myyearloading: false,
      total: true,
      lastyear: [],
      thisyear: [],
      week: [],
      week_invite_num: [],
      week_audition_num: [],
      week_sign_num: [],
      week_audition_rate: [],
      week_sign_rate: [],
      month: [],
      month_audition_num: [],
      month_sign_num: [],
      month_audition_rate: [],
      month_sign_rate: [],
      peername: '',
      form: {
        username: '',
      },
      total_today: {
        audition_count: 3,
        audition_income: 89.6999,
        entered_count: 3,
        entered_income: 8999.7,
      },
      peer_today: {
        audition_count: 0,
        audition_income: 0,
        entered_count: 0,
        entered_income: 0,
      },
    };
  },
  methods: {
    checkpeerinfo() {
      this.peername = this.form.username;
      this.axios({
        method: 'post',
        url: 'data/today_seller_grades',
        data: {
          name: this.peername,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.peer_today = response.data;
          this.$options.methods.checkpeerToday(this);
        } else {
          this.$message.error('用户名不存在!');
        }
      });
    },
    checkTotalToday() {
      this.todayloading = true;
      this.axios({
        method: 'post',
        url: 'data/today_grades',
        data: {
          name: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        this.total_today = response.data;
      });
      this.todayloading = false;
    },
    checkpeermonth(a) {
      this.mymonthloading = true;
      const that = a;
      that.axios({
        method: 'post',
        url: 'data/months_seller_grades',
        data: {
          name: that.peername,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        that.month_audition_num = [];
        that.month_sign_num = [];
        that.month_audition_rate = [];
        that.month_sign_rate = [];
        that.month = [];
        if (response.data.list[0].error === DIC.STATUS_CODE.Success) {
          for (let i = 0; i < response.data.list.length; i += 1) {
            that.month_audition_num[i] = response.data.list[i].auditioncount;
            that.month_sign_num[i] = response.data.list[i].signcount;
            that.month_audition_rate[i] = response.data.list[i].audition_rate;
            that.month_sign_rate[i] = response.data.list[i].sign_rate;
            that.month[i] = i + 1;
          }
          const colors = ['#5793f3', '#d14a61', '#675bba', '#ffd85c', '#67c23a', '#1b7070', '#ef00b8'];
          const peermonthChart = echarts.init(document.getElementById('peer_month'));
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
              data: ['试听人数', '报名人数', '试听率', '试听报名率'],
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
                name: '试听人数',
                min: 0,
                max: 150,
                position: 'right',
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
                name: '报名人数',
                min: 0,
                max: 150,
                position: 'left',
                axisLine: {
                  lineStyle: {
                    color: colors[2],
                  },
                },
                axisLabel: {
                  formatter: '{value} 人',
                },
              },
              {
                type: 'value',
                name: '试听率',
                min: 0,
                max: 100,
                position: 'right',
                offset: 55,
                axisLine: {
                  lineStyle: {
                    color: colors[3],
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
                offset: 110,
                axisLine: {
                  lineStyle: {
                    color: colors[0],
                  },
                },
                axisLabel: {
                  formatter: '{value} %',
                },
              },
            ],
            series: [
              {
                name: '试听人数',
                type: 'bar',
                yAxisIndex: 0,
                data: that.month_audition_num,
              },
              {
                name: '报名人数',
                type: 'bar',
                yAxisIndex: 1,
                data: that.month_sign_num,
              },
              {
                name: '试听率',
                type: 'line',
                yAxisIndex: 2,
                data: that.month_audition_rate,
              },
              {
                name: '试听报名率',
                type: 'line',
                yAxisIndex: 3,
                data: that.month_sign_rate,
              },
            ],
          });
          that.$options.methods.checkpeeryear(that);
        } else {
          that.$message.error('用户名不存在!');
        }
      });
      this.mymonthloading = false;
    },
    checkpeerToday(a) {
      const that = a;
      that.axios({
        method: 'post',
        url: 'data/today_seller_grades',
        data: {
          name: that.peername,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          that.peer_today = response.data;
          that.$options.methods.checkpeer7days(that);
        } else {
          that.$message.error('用户名不存在!');
        }
      });
    },
    checkpeer7days(a) {
      this.myweekloading = true;
      const that = a;
      that.axios({
        method: 'post',
        url: 'data/week_seller_grades',
        data: {
          name: that.peername,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        that.week_invite_num = [];
        that.week_audition_num = [];
        that.week_sign_num = [];
        that.week_audition_rate = [];
        that.week_sign_rate = [];
        that.week = [];
        if (response.data.list[0].error === DIC.STATUS_CODE.Success) {
          for (let i = 0; i < response.data.list.length; i += 1) {
            that.week_invite_num[i] = response.data.list[i].sellcount;
            that.week_audition_num[i] = response.data.list[i].auditioncount;
            that.week_sign_num[i] = response.data.list[i].signcount;
            that.week_audition_rate[i] = response.data.list[i].audition_rate;
            that.week_sign_rate[i] = response.data.list[i].sign_rate;
            that.week[i] = response.data.list[i].date;
          }
          const colors = ['#5793f3', '#d14a61', '#675bba', '#ffd85c', '#67c23a', '#1b7070', '#ef00b8'];
          const peerweekChart = echarts.init(document.getElementById('peer_7days'));
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
              data: ['邀约人数', '试听人数', '报名人数', '试听率', '试听报名率'],
            },
            xAxis: [
              {
                type: 'category',
                axisTick: {
                  alignWithLabel: true,
                },
                data: that.week,
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
                position: 'right',
                offset: 55,
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
                name: '报名人数',
                min: 0,
                max: 60,
                position: 'left',
                axisLine: {
                  lineStyle: {
                    color: colors[2],
                  },
                },
                axisLabel: {
                  formatter: '{value} 人',
                },
              },
              {
                type: 'value',
                name: '试听率',
                min: 0,
                max: 100,
                position: 'left',
                offset: 55,
                axisLine: {
                  lineStyle: {
                    color: colors[3],
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
                offset: 110,
                axisLine: {
                  lineStyle: {
                    color: colors[4],
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
                data: that.week_invite_num,
              },
              {
                name: '试听人数',
                type: 'bar',
                yAxisIndex: 1,
                data: that.week_audition_num,
              },
              {
                name: '报名人数',
                type: 'bar',
                yAxisIndex: 2,
                data: that.week_sign_num,
              },
              {
                name: '试听率',
                type: 'line',
                yAxisIndex: 3,
                data: that.week_audition_rate,
              },
              {
                name: '试听报名率',
                type: 'line',
                yAxisIndex: 4,
                data: that.week_sign_rate,
              },
            ],
          });
          that.$options.methods.checkpeermonth(that);
        } else {
          that.$message.error('用户名不存在!');
        }
      });
      this.myweekloading = false;
    },
    checktotalmonth() {
      this.monthloading = true;
      this.axios({
        method: 'post',
        url: 'data/months_seller_grades',
        data: {
          name: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        this.month_audition_num = [];
        this.month_sign_num = [];
        this.month_audition_rate = [];
        this.month_sign_rate = [];
        this.month = [];
        if (response.data.list[0].error === DIC.STATUS_CODE.Success) {
          for (let i = 0; i < response.data.list.length; i += 1) {
            this.month_audition_num.push(response.data.list[i].auditioncount);
            this.month_sign_num.push(response.data.list[i].signcount);
            this.month_audition_rate.push(response.data.list[i].audition_rate);
            this.month_sign_rate.push(response.data.list[i].sign_rate);
            this.month.push(i + 1);
          }
        }
        const colors = ['#5793f3', '#d14a61', '#675bba', '#ffd85c', '#67c23a', '#1b7070', '#ef00b8'];
        const totalmonthChart = echarts.init(document.getElementById('total_month'));
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
            data: ['试听人数', '报名人数', '试听率', '试听报名率'],
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
              name: '试听人数',
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
              name: '报名人数',
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
              name: '试听率',
              min: 0,
              max: 100,
              position: 'right',
              offset: 55,
              axisLine: {
                lineStyle: {
                  color: colors[2],
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
              offset: 110,
              axisLine: {
                lineStyle: {
                  color: colors[3],
                },
              },
              axisLabel: {
                formatter: '{value} %',
              },
            },
          ],
          series: [
            {
              name: '试听人数',
              type: 'bar',
              yAxisIndex: 0,
              data: this.month_audition_num,
            },
            {
              name: '报名人数',
              type: 'bar',
              yAxisIndex: 1,
              data: this.month_sign_num,
            },
            {
              name: '试听率',
              type: 'line',
              yAxisIndex: 2,
              data: this.month_audition_rate,
            },
            {
              name: '试听报名率',
              type: 'line',
              yAxisIndex: 3,
              data: this.month_sign_rate,
            },
          ],
        });
      });
      this.monthloading = false;
    },
    checktotal7days() {
      this.weekloading = true;
      this.axios({
        method: 'post',
        url: 'data/week_seller_grades',
        data: {
          name: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        this.week_invite_num = [];
        this.week_audition_num = [];
        this.week_sign_num = [];
        this.week_audition_rate = [];
        this.week_sign_rate = [];
        this.week = [];
        if (response.data.list[0].error === DIC.STATUS_CODE.Success) {
          for (let i = 0; i < response.data.list.length; i += 1) {
            this.week_invite_num.push(response.data.list[i].sellcount);
            this.week_audition_num.push(response.data.list[i].auditioncount);
            this.week_sign_num.push(response.data.list[i].signcount);
            this.week_audition_rate.push(response.data.list[i].audition_rate);
            this.week_sign_rate.push(response.data.list[i].sign_rate);
            this.week.push(response.data.list[i].date);
          }
        }
        const colors = ['#5793f3', '#d14a61', '#675bba', '#ffd85c', '#67c23a', '#1b7070', '#ef00b8'];
        const totalweekChart = echarts.init(document.getElementById('total_7days'));
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
            data: ['邀约人数', '试听人数', '报名人数', '试听率', '试听报名率'],
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
              position: 'right',
              offset: 55,
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
              name: '报名人数',
              min: 0,
              max: 60,
              position: 'left',
              axisLine: {
                lineStyle: {
                  color: colors[2],
                },
              },
              axisLabel: {
                formatter: '{value} 人',
              },
            },
            {
              type: 'value',
              name: '试听率',
              min: 0,
              max: 100,
              position: 'left',
              offset: 55,
              axisLine: {
                lineStyle: {
                  color: colors[3],
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
              offset: 110,
              axisLine: {
                lineStyle: {
                  color: colors[4],
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
              data: this.week_invite_num,
            },
            {
              name: '试听人数',
              type: 'bar',
              yAxisIndex: 1,
              data: this.week_audition_num,
            },
            {
              name: '报名人数',
              type: 'bar',
              yAxisIndex: 2,
              data: this.week_sign_num,
            },
            {
              name: '试听率',
              type: 'line',
              yAxisIndex: 3,
              data: this.week_audition_rate,
            },
            {
              name: '试听报名率',
              type: 'line',
              yAxisIndex: 4,
              data: this.week_sign_rate,
            },
          ],
        });
      });
      this.weekloading = false;
    },
    checktotalyear() {
      this.yearloading = true;
      this.axios({
        method: 'post',
        url: 'data/years_seller_grades',
        data: {
          name: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        this.lastyear = [];
        this.thisyear = [];
        if (response.data.last_list[0].error === DIC.STATUS_CODE.Success) {
          this.lastyear.push(response.data.last_list[0].sellcount);
          this.thisyear.push(response.data.this_list[0].sellcount);
          this.lastyear.push(response.data.last_list[0].auditioncount);
          this.thisyear.push(response.data.this_list[0].auditioncount);
          this.lastyear.push(response.data.last_list[0].sellmoney);
          this.thisyear.push(response.data.this_list[0].sellmoney);
          this.lastyear.push(response.data.last_list[0].signcount);
          this.thisyear.push(response.data.this_list[0].signcount);
          this.lastyear.push(response.data.last_list[0].signmoney);
          this.thisyear.push(response.data.this_list[0].signmoney);
          this.lastyear.push(response.data.last_list[0].audition_rate);
          this.thisyear.push(response.data.this_list[0].audition_rate);
          this.lastyear.push(response.data.last_list[0].sign_rate);
          this.thisyear.push(response.data.this_list[0].sign_rate);
        }
        const totalyearChart = echarts.init(document.getElementById('total_year'));
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
          series: [{
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
          }],
        });
      });
      this.yearloading = false;
    },
    checkpeeryear(a) {
      this.myyearloading = true;
      const that = a;
      that.axios({
        method: 'post',
        url: 'data/years_seller_grades',
        data: {
          name: that.peername,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        that.lastyear = [];
        that.thisyear = [];
        if (response.data.last_list[0].error === DIC.STATUS_CODE.Success) {
          that.lastyear[0] = response.data.last_list[0].sellcount;
          that.thisyear[0] = response.data.this_list[0].sellcount;
          that.lastyear[1] = response.data.last_list[0].auditioncount;
          that.thisyear[1] = response.data.this_list[0].auditioncount;
          that.lastyear[2] = response.data.last_list[0].sellmoney;
          that.thisyear[2] = response.data.this_list[0].sellmoney;
          that.lastyear[3] = response.data.last_list[0].signcount;
          that.thisyear[3] = response.data.this_list[0].signcount;
          that.lastyear[4] = response.data.last_list[0].signmoney;
          that.thisyear[4] = response.data.this_list[0].signmoney;
          that.lastyear[5] = response.data.last_list[0].audition_rate;
          that.thisyear[5] = response.data.this_list[0].audition_rate;
          that.lastyear[6] = response.data.last_list[0].sign_rate;
          that.thisyear[6] = response.data.this_list[0].sign_rate;
          const peeryearChart = echarts.init(document.getElementById('peer_year'));
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
            series: [{
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
            }],
          });
        } else {
          that.$message.error('用户名不存在!');
        }
      });
      this.myyearloading = false;
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
