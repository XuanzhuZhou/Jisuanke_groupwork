<template>
    <el-table :data="tableData" stripe v-if="currValue === '5'"
    class='demos' height="400">
    <el-table-column prop="id" label="课程序号" width="180"></el-table-column>
    <el-table-column prop="course" label="课程名" width="180"></el-table-column>
    <el-table-column prop="sec" label="总课时" width="180"></el-table-column>
    <el-table-column prop="name" label="孩子姓名" width="180"></el-table-column>
    <el-table-column prop="teacher" label="老师姓名" width="140">
    </el-table-column>
    <el-table-column label="申请退款" width="250">
      <template slot-scope="scope">
        <el-button type="primary" size="mini" disabled
        v-if="scope.row.hasdone === 3">
        已退款</el-button>
        <el-button type="danger" size="mini"
        @click="fund(scope.$index, scope.row)"
        v-else-if="scope.row.hasdone === 0">
        退款</el-button>
        <el-button type="success" size="mini" disabled
        @click="fund(scope.$index, scope.row)"
        v-else-if="scope.row.hasdone === 2">
        退款中</el-button>
        <el-button-group v-else>
          <el-button type="warning" size="mini" disabled>
          审核中</el-button>
          <el-button size="mini" @click="cancel(scope.$index, scope.row)">
          取消退款</el-button>
        </el-button-group>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
/**
 * 家长退款页面
 * @module refund
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
   * @prop {Boolean} isTrans 判断是否需要重新发送请求获取退款信息
   * @prop {Array} tableData 存放需要退款的课程信息
   * @prop {String} info 家长退款时输入的退款理由
   * @prop {String} message 退款成功与否给出家长的提示信息
   */
  data() {
    return {
      currValue: '0',
      isTrans: true,
      tableData: [],
      info: '',
      message: '',
    };
  },
  methods: {
    /**
     * @function fund
     * @description 申请退款并给出退款课程的具体信息，打开支付页面
     */
    fund(index, row) {
      const h = this.$createElement;
      this.$msgbox({
        title: '退款',
        message: h('p', null, [
          h('span', null, '请输入退款理由：'),
        ]),
        showInput: true,
        inputType: 'textarea',
        showCancelButton: true,
        roundButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            const ins = instance;
            ins.confirmButtonLoading = true;
            ins.confirmButtonText = '执行中...';
            setTimeout(() => {
              done();
              setTimeout(() => {
                ins.confirmButtonLoading = false;
              }, 300);
            }, 1000);
          } else {
            done();
          }
        },
      }).then(({ value }) => {
        this.message = value;
      }).then(() => {
        this.axios({
          method: 'post',
          url: 'customer/refund',
          data: {
            info: this.message,
            course_id: row.id,
            child_name: row.name,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then((response) => {
          if (response.data.msg === DIC.STATUS_CODE.Success) {
            this.tableData[index].hasdone = DIC.REFUND_STATUS['Under Review'];
            this.$message({
              type: 'info',
              message: '退款申请成功！请耐心等待后台处理',
            });
          } else {
            this.$message({
              type: 'info',
              message: '退款申请失败！请询问相关工作人员',
            });
          }
        });
      });
    },
    /**
     * @function cancel
     * @description 取消退款并发送给后端相关信息
     */
    cancel(index, row) {
      this.$confirm('此操作将取消该课程退款, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        this.tableData[index].hasdone = DIC.REFUND_STATUS['No Refund Received'];
        this.axios({
          method: 'post',
          url: 'customer/refund_cancel',
          data: {
            course_id: row.id,
            child_name: row.name,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then((response) => {
          if (response.data.msg === DIC.STATUS_CODE.Success) {
            this.tableData[index].hasdone =
            DIC.REFUND_STATUS['No Refund Received'];
            this.$message({
              type: 'success',
              message: '取消退款成功!',
            });
          } else {
            this.$message({
              type: 'info',
              message: '取消退款失败',
            });
          }
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消退款失败',
        });
      });
    },
  },
  watch: {
    initial(nv) {
      this.currValue = nv;
      if (nv === '5') {
        this.axios({
          method: 'post',
          url: 'customer/courses',
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then((response) => {
          if (response.data.msg === DIC.STATUS_CODE.Success && this.isTrans) {
            for (let i = 1; i < response.data.list.length; i += 1) {
              const lesson = {};
              lesson.id = response.data.list[i].id;
              lesson.course = response.data.list[i].name;
              lesson.sec = response.data.list[i].total_sec;
              lesson.name = response.data.list[i].child_name;
              lesson.teacher = response.data.list[i].teacher_name;
              lesson.hasdone = response.data.list[i].refund_apply;
              this.tableData.push(lesson);
            }
            this.isTrans = false;
          }
        });
      }
    },
  },
};
</script>

<style scoped>
.demos {
  margin: 0 auto;
  height: 55%;
  width: 83%;
  margin-top: 3.5%;
}
</style>
