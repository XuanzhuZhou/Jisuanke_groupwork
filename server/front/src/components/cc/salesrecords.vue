<template>
  <div>
    <el-card shadow="hover" class="mycard">
      <div>
        <el-form ref="form" :model="form" :inline="true">
          <el-form-item label="活动时间">
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
      <el-table :data="tableData">
        <el-table-column prop="flow_num" label="流量总数"></el-table-column>
        <el-table-column prop="audition_num" label="试听总数"></el-table-column>
        <el-table-column prop="audition_rate" label="试听率"></el-table-column>
        <el-table-column prop="consumption_num" label="报课人数">
        </el-table-column>
        <el-table-column prop="consumption_rate" label="报课率"></el-table-column>
        <el-table-column prop="flow_change_rate" label="流量转化率">
        </el-table-column>
        <el-table-column prop="income" label="总收入"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>
<style scoped>
.mycard {
  min-height: 800px;
}
.el-table th {
  text-align: center;
}
.sellersales {
  width: 80%;
  margin: 0 12% 0 12%;
}
.el-card is-hover-shadow {
  margin: 25px;
}
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
</style>
<script>
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';

export default {
  props: {
    initial: {
      default: '0',
    },
  },
  data() {
    return {
      currValue: '0',
      tableData: [],
      form: {
        value0: null,
        value1: null,
      },
    };
  },
  watch: {
    initial(nv) {
      this.currValue = nv;
    },
  },
  methods: {
    getSales() {
      this.axios({
        method: 'post',
        url: 'api/view_ccrecords',
        data: {
          date_from: this.form.value0,
          date_to: this.form.value1,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.tableData = [];
          this.tableData.push(response.data.list);
          this.$message({
            message: '数据已更新！',
            type: 'success',
          });
        }
      });
    },
  },

};
</script>

