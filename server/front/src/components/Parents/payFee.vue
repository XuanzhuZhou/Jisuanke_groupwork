<template>
  <el-table :data="tableData" stripe v-if="currValue === '7'"
  class='demos' height="400">
    <el-table-column prop="id" class="hides" label="ID"
    width="0"></el-table-column>
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
        @click="pay(scope.$index, scope.row)" v-else>待支付</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
/**
 * 家长支付课程页面
 * @module payFee
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
   * @prop {String} currValue 更改当前页面
   * @prop {Boolean} isTrans 判断是否需要重新发送获取需要付款的课程信息的请求
   * @prop {Array} tableData 存放需要支付的课程信息
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
      if (nv === '7') {
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
     * @description 获取所要支付的课程信息并发送请求弹出支付页面
     */
    pay(index, row) {
      this.axios({
        method: 'post',
        url: 'api/payclass',
        data: {
          id: row.id,
          price: row.price,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        window.open(response.data.url);
        this.$confirm('支付情况', '提示', {
          confirmButtonText: '支付成功',
          cancelButtonText: '支付遇到问题',
          type: 'success',
        }).then(() => {
          this.$message({
            type: 'success',
            message: '快去享受试听盛宴吧!',
          });
          this.axios({
            method: 'post',
            url: 'customer/register_success',
            data: {
              username: this.ruleForm2.tel,
              child_name: this.ruleForm2.name,
            },
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '注意查看您的支付账户哦！',
          });
        });
      });
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
    },
  },
};
</script>

<style scoped>
.demos {
  margin: 0 auto;
  height: 80%;
  width: 85%;
  margin-top: 1%;
}
.hides {
  visibility: hidden;
}
</style>
