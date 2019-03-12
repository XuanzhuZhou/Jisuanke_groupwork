<template>
  <el-table :data="tableData" stripe v-if="currValue === '5'"
  height="400" class="table">
    <el-table-column prop="id" class="hides"></el-table-column>
    <el-table-column prop="child_name" label="孩子姓名" width="180">
    </el-table-column>
    <el-table-column prop="date" label="报名日期" width="180">
    </el-table-column>
    <el-table-column prop="cc_name" label="课顾姓名" width="180">
    </el-table-column>
    <el-table-column prop="price" label="价格" width="180">
    </el-table-column>
    <el-table-column prop="info" label="详细信息" width="180">
    </el-table-column>
    <el-table-column label="支付情况" width="120">
      <template slot-scope="scope">
        <el-button size="mini" disabled v-if="scope.row.hasdone">
          已支付</el-button>
        <el-button type="primary" size="small"
        @click="pay(scope.$index, scope.row)"
        v-else>待支付</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
/**
 * 家长手机端支付课程页面
 * @module pay
 */
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';

export default {
  props: {
    initial: {
      default: '0',
    },
  },
  /**
   * @prop {String} currValue 判断页面所处状态
   * @prop {Boolean} isTrans 判断是否需要重新发送请求获取支付信息
   * @prop {Array} tableData 存放家长支付课程信息
   */
  data() {
    return {
      currValue: '0',
      isTrans: true,
      tableData: [],
    };
  },
  watch: {
    initial(nv) {
      this.currValue = nv;
      if (nv === '5') {
        this.axios({
          method: 'post',
          url: 'customer/pay_records',
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then((response) => {
          if (response.data.msg === DIC.STATUS_CODE.Success && this.isTrans) {
            for (let i = 0; i < response.data.list.length; i += 1) {
              const courses = {};
              courses.id = response.data.list[i].id;
              courses.child_name = response.data.list[i].child_name;
              courses.date = response.data.list[i].date;
              courses.cc_name = response.data.list[i].cc_name;
              courses.price = response.data.list[i].money;
              courses.info = response.data.list[i].info;
              courses.hasdone = response.data.list[i].is_paid;
              this.tableData.push(courses);
            }
            this.isTrans = false;
          }
        });
      }
    },
  },
  methods: {
    /**
     * @function pay
     * @description 发送支付请求并打开支付宝供用户支付
     */
    pay(index, row) {
      this.axios({
        method: 'post',
        url: 'customer/payclass',
        data: {
          id: row.id,
          price: row.price,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        this.tableData = response.data.list;
      });
    },
  },
};
</script>

<style scoped>
.hides {
  visibility: hidden;
}
.table, .table td, .table th {
  background-color: rgba(240, 248, 255, 0.705);
}
</style>
