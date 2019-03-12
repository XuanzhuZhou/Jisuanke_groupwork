<template>
<div>
    <el-card>
        <div>
          <el-form ref="form" :model="form" :inline="true">
            <el-form-item label="搜索时间">
              <el-col :span="11">
                <el-date-picker v-model="form.value0"
                                value-format="yyyy-MM-dd"
                                type="date"
                                placeholder="开始日期">
                </el-date-picker>
                </el-col>
              <el-col class="line" :span="2">-</el-col>
              <el-col :span="11">
                <el-date-picker v-model="form.value1"
                                value-format="yyyy-MM-dd"
                                type="date"
                                placeholder="结束日期">
                </el-date-picker>
              </el-col>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" icon="el-icon-search" @click="getSales()">
                  搜索
              </el-button>
            </el-form-item>
          </el-form>
        </div>
        <div class="sellersales">
        <el-table :data="tableData">
            <el-table-column prop="today_count" label="今日客户数"></el-table-column>
            <el-table-column prop="today_money" label="今日总销售额"></el-table-column>
            <el-table-column prop="history_count" label="已选日期总客户数"></el-table-column>
            <el-table-column prop="history_money" label="已选日期总销售额"></el-table-column>
        </el-table>
        </div>
    </el-card>
</div>
</template>
<style scoped>
.el-main {
  padding-top: 0;
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
.el-table th {
  text-align: center;
}
.sellersales {
  width: 80%;
  margin: 0 10% 0 10%;
  min-height: 800px;
}
.el-card is-hover-shadow {
  margin: 25px;
}
.el-form-item__label {
  margin-top: 10px;
}
</style>
<script>
import { getCookie } from '@/utils/utils';

export default {
  data() {
    return {
      name: this.$route.params.user,
      form: {
        value0: null,
        value1: null,
      },
      tableData: [{
        today_count: '',
        today_money: '',
        history_count: '',
        history_money: '',
      }],
    };
  },
  methods: {
    getSales() {
      this.axios({
        method: 'post',
        url: 'api/get_sellrecords',
        data: {
          date0: this.form.value0,
          date1: this.form.value1,
          username: this.$route.params.user,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        this.tableData = response.data.list;
      });
    },
  },
};
</script>
