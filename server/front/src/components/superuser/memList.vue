<template>
    <div>
      <el-card shadow="hover" class="mycard">
      <el-table :data="tempList" stripe=true>
        <el-table-column prop="id" label="用户编号" align="center">
        </el-table-column>
        <el-table-column prop="username" label="用户名" align="center">
        </el-table-column>
        <el-table-column prop="email" label="邮件地址" align="center">
        </el-table-column>
        <el-table-column prop="gender" label="性别" align="center">
        </el-table-column>
        <el-table-column prop="date_joined" label="上次登录时间" align="center">
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button @click="edit(scope.row)" type="text">编辑</el-button>
            <el-button @click="del(scope.row)" type="text">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-size="pageSize"
          layout="total, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </div>
      </el-card>
      <el-dialog title="修改信息" :visible.sync="dialogFormVisible" class="conversation">
        <el-form :model="form">
          <el-form-item label="密码" class="itemlabel">
            <el-input type="password" v-model="form.password" auto-complete=this.autopassword>
            </el-input>
          </el-form-item>
          <el-form-item label="邮件地址">
            <el-input v-model="form.email" auto-complete=this.autoemail></el-input>
          </el-form-item>
          <el-form-item label="性别">
            <el-input v-model="form.gender" auto-complete=this.autogender></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="submit()">确 定</el-button>
        </div>
      </el-dialog>
    </div>
</template>
<style scoped>
.el-main {
  text-align: left;
}
.mycard {
  min-height: 800px;
}
.conversation {
  width: 50%;
  margin: 0 30% 0 30%;
}
.el-table tr {
  background-color: #e4e7ed;
}
.el-table thead {
    color: #363232;
    font-weight: 400;
}
.el-table__header-wrapper {
  margin-top: 0;
}
.itemlabel {
  margin-left: 0;
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
    usertype: {
      type: Number,
      require: true,
    },
  },
  watch: {
    usertype(val) {
      this.usert = val;
    },
    initial(nv) {
      this.currValue = nv;
      if (nv === '3' || nv === '4' || nv === '5') {
        this.refresh();
      }
    },
  },
  data() {
    return {
      currValue: '0',
      autousername: '',
      usert: this.usertype,
      dialogFormVisible: false,
      form: {
        email: '',
        username: '',
        gender: '',
        password: '',
      },
      edulist: [],
      tempList: [],
      pageSize: 10,
      total: 0,
      currentPage: 1,
      person: [
        {
          type: '教务老师列表',
        },
        {
          type: '课程顾问列表',
        },
        {
          type: '地推人员列表',
        },
      ],
    };
  },
  mounted() {
    const nv = this.initial;
    if (nv === '3' || nv === '4' || nv === '5') {
      this.refresh();
    }
  },
  methods: {
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
      this.currentChangePage(this.edulist, currentPage);
    },
    currentChangePage(list, currentPage) {
      let listFrom = (currentPage - 1) * this.pageSize;
      const listTo = currentPage * this.pageSize;
      this.tempList = [];
      for (; listFrom < listTo; listFrom += 1) {
        if (list[listFrom]) {
          this.tempList.push(list[listFrom]);
        }
      }
    },
    del(row) {
      this.$confirm('是否确认删除该用户?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        this.axios({
          method: 'post',
          url: '/api/delete_user',
          data: {
            username: row.username,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then((response) => {
          if (response.data.msg === DIC.STATUS_CODE.Success) {
            this.$message({
              message: '删除成功！',
              type: 'success',
            });
            this.refresh();
            this.axios({
              method: 'post',
              url: '/api/sup_view_users',
              data: {
                user_type: this.usert,
                username: '',
              },
              headers: { 'X-CSRFToken': getCookie('csrftoken') },
            }).then((res) => {
              if (res.data.msg === DIC.STATUS_CODE.Success) {
                this.edulist = res.data.list;
                this.total = this.edulist.length;
                this.handleCurrentChange(this.currentPage);
              } else {
                this.$message.error('身份错误!');
              }
            });
            this.form.email = '';
            this.form.username = '';
            this.form.gender = '';
            this.form.password = '';
          }
          if (response.data.msg === DIC.STATUS_CODE['User Not Found']) {
            this.$message.error('未找到客户!');
          }
          if (response.data.msg === DIC.STATUS_CODE['Identity Error']) {
            this.$message.error('身份错误!');
          }
          if (response.data.msg === DIC.STATUS_CODE['Frontend Value Error']) {
            this.$message.error('输入数据有误!');
          }
        });
      });
    },
    edit(row) {
      this.dialogFormVisible = true;
      this.autousername = row.username;
    },
    submit() {
      this.dialogFormVisible = false;
      this.axios({
        method: 'post',
        url: '/api/modify_user',
        data: {
          username: this.autousername,
          email: this.form.email,
          password: this.form.password,
          gender: this.form.gender,
          user_type: this.usert,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.$message({
            message: '修改成功！',
            type: 'success',
          });
          this.axios({
            method: 'post',
            url: '/api/sup_view_users',
            data: {
              user_type: this.usert,
              username: '',
            },
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
          }).then((res) => {
            if (res.data.msg === DIC.STATUS_CODE.Success) {
              this.edulist = res.data.list;
              this.total = this.edulist.length;
              this.handleCurrentChange(this.currentPage);
            } else {
              this.$message.error('身份错误!');
            }
          });
          this.form.email = '';
          this.form.username = '';
          this.form.gender = '';
          this.form.password = '';
        } else {
          this.$message.error('Identity error!');
        }
      });
    },
    refresh() {
      this.axios({
        method: 'post',
        url: '/api/sup_view_users',
        data: {
          user_type: this.usert,
          username: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.edulist = response.data.list;
          this.currentPage = 1;
          this.total = this.edulist.length;
          this.handleCurrentChange(this.currentPage);
        } else {
          this.$message.error('身份错误!');
        }
      });
    },
  },
};
</script>
