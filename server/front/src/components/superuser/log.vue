<template>
    <div>
      <div>
      <el-date-picker v-model="value0"
        value-format="yyyy-MM-dd"
        type="date"
        placeholder="开始日期">
      </el-date-picker>
      <el-date-picker v-model="value1"
        value-format="yyyy-MM-dd"
        type="date"
        placeholder="结束日期">
      </el-date-picker>
        <el-button type="primary" icon="el-icon-search" @click="getlog()">
          搜索
        </el-button>
    </div>
    <el-card shadow="hover" class="mycard">
      <el-table :data="loglist">
        <el-table-column prop="id" label="#" align="center">
        </el-table-column>
        <el-table-column prop="date" label="操作时间" align="center">
        </el-table-column>
        <el-table-column prop="operator" label="操作者" align="center">
        </el-table-column>
        <el-table-column prop="info" label="操作内容" align="center">
        </el-table-column>
        <el-table-column prop="username" label="对象" align="center">
        </el-table-column>
        <el-table-column prop="type" label="类型" align="center"
          :filters="[{ text: '删除用户', value: '删除用户' }, { text: '退款', value: '退款' },
          { text: '删除客户', value: '删除客户' }, { text: '添加用户', value: '添加用户' }]"
          :filter-method="filterTag" filter-placement="bottom-end">
          <template slot-scope="scope">
            <el-tag :type='success' disable-transitions>{{scope.row.type}}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    </div>
</template>
<style scoped>
.mycard {
  min-height:800px;
}
.el-table__header-wrapper {
  margin-top: 0;
}
.el-main {
  text-align: center;
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
  data() {
    return {
      value0: null,
      value1: null,
      loglist: [{
        date: '2016-05-02',
        username: '王小虎',
        id: 1,
        operator: '猪猪侠',
        info: '猪猪侠添加了一个地推',
        type: '添加用户',
      }, {
        date: '2016-05-02',
        username: '王小虎',
        id: 2,
        operator: '猪猪侠',
        info: '猪猪侠添加了一个地推',
        type: '删除用户',
      }, {
        date: '2016-05-02',
        username: '王小虎',
        id: 3,
        operator: '猪猪侠',
        info: '猪猪侠添加了一个地推',
        type: '删除客户',
      }, {
        date: '2016-05-02',
        username: '王小虎',
        id: 4,
        operator: '猪猪侠',
        info: '猪猪侠添加了一个地推',
        type: '退款',
      }],
    };
  },
  mounted() {
    this.getlog();
  },
  methods: {
    filterTag(value, row) {
      return row.type === value;
    },
    filterHandler(value, row, column) {
      const property = column.property;
      return row[property] === value;
    },
    getlog() {
      this.axios({
        method: 'post',
        url: 'user/superuser_viewlog',
        data: {
          start: this.value0,
          end: this.value1,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE['Not Found']) {
          this.$message({
            message: '无结果！',
            type: 'warning',
          });
        }
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.$message({
            message: '搜索成功！',
            type: 'success',
          });
          this.loglist = response.data.list;
          for (let i = 0; i < this.loglist.length; i += 1) {
            if (this.loglist[i].type === DIC.LOG_TYPE.Refund) {
              this.loglist[i].type = '退款';
            }
            if (this.loglist[i].type === DIC.LOG_TYPE['Delete User']) {
              this.loglist[i].type = '删除用户';
            }
            if (this.loglist[i].type === DIC.LOG_TYPE['Delete Customer']) {
              this.loglist[i].type = '删除客户';
            }
            if (this.loglist[i].type === DIC.LOG_TYPE['Add User']) {
              this.loglist[i].type = '添加用户';
            }
          }
        }
      });
    },
  },
};
</script>

