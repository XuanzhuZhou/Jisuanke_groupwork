<template>
  <div>
    <el-card shadow="hover" class="mycard">
    <el-table :data="notRefund">
      <el-table-column prop="id" label="退款编号"></el-table-column>
      <el-table-column prop="date" label="申请退款日期"></el-table-column>
      <el-table-column prop="stu_name" label="孩子姓名"></el-table-column>
      <el-table-column prop="phone" label="家长的手机号"></el-table-column>
      <el-table-column prop="course_id" label="课程编号"></el-table-column>
      <el-table-column prop="coursename" label="课程名称"></el-table-column>
      <el-table-column prop="cncl_num" label="已销课程数目"></el-table-column>
      <el-table-column prop="total_sec" label="总课时"></el-table-column>
      <el-table-column prop="payment" label="课程价格"></el-table-column>
      <el-table-column prop="reason" label="退款理由"></el-table-column>
      <el-table-column>
        <template slot-scope="scope">
          <el-button @click="willRefund(scope.row)" type="text">
            退课
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.el-table th>.cell {
  width: 100%;
}
.el-table th>.cell {
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
.mycard {
  min-height: 800px;
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
    name: {
      type: String,
      require: true,
    },
  },
  data() {
    return {
      currValue: '0',
      username: '',
      notRefund: [],
    };
  },
  watch: {
    name(nv) {
      this.username = nv;
    },
    initial(nv) {
      this.currValue = nv;
      if (nv === '2') {
        this.refresh();
      }
    },
  },
  methods: {
    willRefund(row) {
      this.$prompt('请输入退款金额', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        this.axios({
          method: 'post',
          url: 'api/cc_ensure_refund',
          data: {
            id: row.id,
            refund: value,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then((response) => {
          if (response.data.error === DIC.STATUS_CODE['Not Found']) {
            this.$message.error('退款失败!');
          } else {
            this.$message({
              message: '退款成功!',
              type: 'success',
            });
          }
        });
      });
    },
    refresh() {
      this.axios({
        method: 'post',
        url: 'api/cc_check_refund',
        data: {
          username: this.$route.params.user,
          refund: false,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.count === 0) {
          this.$message('暂无数据！');
          this.notRefund = [];
        } else {
          this.notRefund = response.data.list;
          this.$message({
            message: '数据已更新!',
            type: 'success',
          });
        }
      });
    },
  },
};
</script>

