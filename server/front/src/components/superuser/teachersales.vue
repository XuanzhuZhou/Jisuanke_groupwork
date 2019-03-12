<template>
<div>
  <el-card shadow="hover" class="mycard">
    <div class="form">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px"
      class="demo-ruleForm">
        <el-form-item label="名字" prop="username">
          <el-input v-model="ruleForm.username"></el-input>
        </el-form-item>
        <el-form-item label="时间">
          <el-col :span="11">
            <el-form-item prop="date1">
              <el-date-picker type="date" placeholder="选择日期" v-model="ruleForm.date1"
              style="width: 100%;" value-format="yyyy-MM-dd"></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col class="line" :span="2">-</el-col>
          <el-col :span="11">
            <el-form-item prop="date2">
              <el-date-picker type="date" placeholder="选择日期" v-model="ruleForm.date2"
              style="width: 100%;" value-format="yyyy-MM-dd"></el-date-picker>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm()">查询</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="results">
      <el-table :data="tableData" stripe>
        <el-table-column prop="name" label="姓名" align="center">
        </el-table-column>
        <el-table-column prop="audition_num" label="试听人数" align="center">
        </el-table-column>
        <el-table-column prop="signup_num" label="报名人数" align="center">
        </el-table-column>
        <el-table-column prop="rate" label="试听转化率" align="center">
        </el-table-column>
        <el-table-column prop="tag" label="类型"
          :filters="[{ text: '本周', value: '本周' }, { text: '本月', value: '本月' },
          { text: '本年', value: '本年' }, { text: '指定时间段', value: '指定时间段' }]"
          :filter-method="filterTag" filter-placement="bottom-end" align="center">
          <template slot-scope="scope">
            <el-tag :type='success'>{{scope.row.type}}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-card>
</div>
</template>
<script>
import { getCookie } from '@/utils/utils';

export default {
  data() {
    return {
      ruleForm: {
        username: '',
        date1: null,
        date2: null,
      },
      tableData: [],
    };
  },
  methods: {
    filterTag(value, row) {
      return row.tag === value;
    },
    submitForm() {
      this.axios({
        method: 'post',
        url: 'data/audition_grades',
        data: {
          name: this.ruleForm.username,
          date_to: this.ruleForm.date1,
          date_from: this.ruleForm.date2,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (this.ruleForm.username === '' && this.ruleForm.date1 === null) {
          this.tableData = [];
          for (let i = 0; i < response.data.list.length; i += 1) {
            const temp = {};
            temp.name = response.data.list[i].name;
            temp.audition_num = response.data.list[i].audition_num;
            temp.signup_num = response.data.list[i].signup_num;
            temp.rate = response.data.list[i].rate;
            temp.type = '本月';
            this.tableData.push(temp);
          }
        }
        if (this.ruleForm.username !== '' && this.ruleForm.date1 === null) {
          this.tableData = [];
          const temp1 = {};
          temp1.name = response.data.week[1].name;
          temp1.audition_num = response.data.week[1].audition_num;
          temp1.signup_num = response.data.week[1].signup_num;
          temp1.rate = response.data.week[1].rate;
          temp1.type = '本周';
          this.tableData.push(temp1);
          const temp2 = {};
          temp2.name = response.data.month[1].name;
          temp2.audition_num = response.data.month[1].audition_num;
          temp2.signup_num = response.data.month[1].signup_num;
          temp2.rate = response.data.month[1].rate;
          temp2.type = '本月';
          this.tableData.push(temp2);
          const temp3 = {};
          temp3.name = response.data.year[1].name;
          temp3.audition_num = response.data.year[1].audition_num;
          temp3.signup_num = response.data.year[1].signup_num;
          temp3.rate = response.data.year[1].rate;
          temp3.type = '本年';
          this.tableData.push(temp3);
        }
        if (this.ruleForm.username === '' && this.ruleForm.date1 !== null) {
          this.tableData = [];
          for (let i = 0; i < response.data.list.length; i += 1) {
            const temp = {};
            temp.name = response.data.list[i].name;
            temp.audition_num = response.data.list[i].audition_num;
            temp.signup_num = response.data.list[i].signup_num;
            temp.rate = response.data.list[i].rate;
            temp.type = '指定时间段';
            this.tableData.push(temp);
          }
        }
        if (this.ruleForm.username !== '' && this.ruleForm.date1 !== null) {
          this.tableData = [];
          for (let i = 1; i < response.data.list.length; i += 1) {
            const temp = {};
            temp.name = response.data.list[i].name;
            temp.audition_num = response.data.list[i].audition_num;
            temp.signup_num = response.data.list[i].signup_num;
            temp.rate = response.data.list[i].rate;
            temp.type = '指定时间段';
            this.tableData.push(temp);
          }
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>
<style scoped>
.mycard {
  min-height: 800px;
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
