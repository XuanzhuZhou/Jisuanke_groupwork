<template>
<div>
  <div>
    <el-card shadow="hover" class="mycard">
      <el-table :data="stulist" stripe=true>
        <el-table-column prop="id" label="编号" align="center">
        </el-table-column>
        <el-table-column prop="child_name" label="孩子姓名" align="center">
        </el-table-column>
        <el-table-column prop="parent_name" label="家长姓名" align="center">
        </el-table-column>
        <el-table-column prop="tel" label="手机号" align="center">
        </el-table-column>
        <el-table-column prop="demand" label="要求" align="center">
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button @click="cc(scope.row)" type="text" size="small">分配课程顾问</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    </div>
    <el-dialog title="课程顾问信息"  :visible.sync="showcclist">
      <el-table :data="cclist" stripe=true>
        <el-table-column property="id" label="编号" align="center">
        </el-table-column>
        <el-table-column property="username" label="姓名" align="center">
        </el-table-column>
        <el-table-column property="gender" label="性别" align="center">
        </el-table-column>
        <el-table-column property="count" label="已有学生数目" align="center">
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button @click="assign(scope.row)" type="text" size="small">确定分配</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
</div>
</template>
<style scoped>
.mycard {
  min-height: 800px;
}
.el-card {
  margin: 15px;
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
  watch: {
    initial(nv) {
      this.currValue = nv;
      if (nv === '15') {
        this.refresh();
      }
    },
  },
  mounted() {
    if (this.initial === '15') {
      this.refresh();
    }
  },
  data() {
    return {
      showcclist: false,
      stulist: [],
      stu_id: '',
    };
  },
  methods: {
    handleClose() {
      this.showcclist = false;
    },
    cc(row) {
      this.stu_id = row.id;
      this.showcclist = true;
      this.axios({
        method: 'post',
        url: 'user/superuser_get_cc',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.cclist = response.data.list;
          this.$message({
            message: '数据已更新！',
            type: 'success',
          });
        } else {
          this.$message.error('无符合条件的课程顾问结果!');
        }
      });
    },
    assign(row) {
      this.showcclist = false;
      this.axios({
        method: 'post',
        url: 'user/superuser_arrange_cc',
        data: {
          customer_id: this.stu_id,
          cc_id: row.id,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.$message({
            message: '分配成功！',
            type: 'success',
          });
        } else {
          this.$message.error('id不存在!请重新输入!');
        }
      });
      this.showcclist = false;
    },
    refresh() {
      this.axios({
        method: 'post',
        url: 'user/superuser_view_newstu',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.stulist = response.data.list;
          this.$message({
            message: '数据已更新！',
            type: 'success',
          });
        } else {
          this.$message.error('无符合条件的客户结果!');
        }
      });
    },
  },
};
</script>
