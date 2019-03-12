<template>
    <div>
      <el-card shadow="hover" class="mycard">
      <el-table :data="tempList" stripe=true style="width: 100%" align="center">
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
            <el-button @click="check(scope.row)" type="text">查看学生信息</el-button>
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
      <el-dialog title="修改家长信息" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="密码" :label-width="formLabelWidth">
            <el-input type="password" v-model="form.password"
              auto-complete=this.autopassword></el-input>
          </el-form-item>
          <el-form-item label="邮件地址" :label-width="formLabelWidth">
            <el-input v-model="form.email" auto-complete=this.autoemail></el-input>
          </el-form-item>
          <el-form-item label="性别" :label-width="formLabelWidth">
            <el-input v-model="form.gender" auto-complete=this.autogender></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="submit()">确 定</el-button>
        </div>
      </el-dialog>
      <el-card shadow="hover"  v-show="showkidlist">
      <el-table :data="kidlist">
        <el-table-column property="user_id" label="编号" align="center">
        </el-table-column>
        <el-table-column property="child_name" label="孩子姓名" align="center">
        </el-table-column>
        <el-table-column property="parent_name" label="家长姓名" align="center">
        </el-table-column>
        <el-table-column property="classin_id" label="classin账号" align="center">
        </el-table-column>
        <el-table-column property="classin_name" label="classin昵称" align="center">
        </el-table-column>
        <el-table-column property="birthday" label="生日" align="center">
        <el-date-picker
          value-format="yyyy-MM-dd"
          type="date"
          placeholder="生日">
        </el-date-picker>
        </el-table-column>
        <el-table-column property="cc_id" label="课程顾问名字" align="center">
        </el-table-column>
        <el-table-column property="audition_count" label="试听次数" align="center">
        </el-table-column>
        <el-table-column property="is_signedup" label="是否报名常规课" align="center">
        </el-table-column>
        <el-table-column property="is_paid" label="是否付过注册费" align="center">
        </el-table-column>
        <el-table-column property="old_user_id" label="老用户的id" align="center">
        </el-table-column>
        <el-table-column property="date_cc" label="第一次联系cc的时间" align="center">
        </el-table-column>
        <el-table-column property="demand" label="课程需求" align="center">
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button @click="changeinfo(scope.row)" type="text" size="small">编辑</el-button>
            <el-button @click="delcustomer(scope.row)" type="text" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
          <el-dialog title="修改孩子信息" :visible.sync="dialogFormVisible1" class="conversation">
        <el-form :model="form1">
          <el-form-item label="孩子姓名" :label-width="formLabelWidth">
            <el-input v-model="form1.child_name"></el-input>
          </el-form-item>
          <el-form-item label="家长姓名" :label-width="formLabelWidth">
            <el-input v-model="form1.parent_name"></el-input>
          </el-form-item>
          <el-form-item label="classin账号" :label-width="formLabelWidth">
            <el-input v-model="form1.classin_id"></el-input>
          </el-form-item>
          <el-form-item label="classin昵称" :label-width="formLabelWidth">
            <el-input v-model="form1.classin_name"></el-input>
          </el-form-item>
         <el-form-item label="生日" :label-width="formLabelWidth">
            <el-input v-model="form1.birthday"></el-input>
          </el-form-item>
         <el-form-item label="课程顾问姓名" :label-width="formLabelWidth">
            <el-input v-model="form1.cc"></el-input>
          </el-form-item>
         <el-form-item label="老顾客姓名" :label-width="formLabelWidth">
            <el-input v-model="form1.old_user_username"></el-input>
          </el-form-item>
         <el-form-item label="是否报名常规课" :label-width="formLabelWidth">
            <el-input v-model="form1.is_signedup"></el-input>
          </el-form-item>
         <el-form-item label="是否付过注册费" :label-width="formLabelWidth">
            <el-input v-model="form1.is_paid"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible1 = false">取 消</el-button>
          <el-button type="primary" @click="submit1()">确 定</el-button>
        </div>
      </el-dialog>
    </div>
</template>
<style scoped>
.conversation {
  width: 50%;
  margin: 0 30% 0 30%;
}
.el-main {
  text-align: left;
}
.mycard {
  min-height: 800px;
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
    usertype: {
      type: Number,
      require: true,
    },
  },
  mounted() {
    if (this.initial === '6') {
      this.refresh(this.currentPage);
    }
  },
  data() {
    return {
      currValue: '0',
      cusid: '',
      kidlist: [],
      showkidlist: false,
      autoemail: '',
      autousername: '',
      autogender: '',
      autopassword: '',
      user: this.usertype,
      dialogFormVisible: false,
      dialogFormVisible1: false,
      form: {
        email: '',
        username: '',
        gender: '',
      },
      form1: {
        child_name: '',
        parent_name: '',
        classin_id: '',
        classin_name: '',
        birthday: '',
        cc: '',
        old_user_username: '',
        is_signedup: '',
        is_paid: '',
      },
      edulist: [],
      tempList: [],
      pageSize: 10,
      total: 0,
      currentPage: 1,
    };
  },
  watch: {
    initial(nv) {
      this.currValue = nv;
      if (nv === '6') {
        this.refresh(this.currentPage);
      }
    },
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
    submit1() {
      this.dialogFormVisible1 = false;
      this.showkidlist = false;
      this.axios({
        method: 'post',
        url: '/api/modify_customer',
        data: {
          customer_id: this.cusid,
          child_name: this.form1.child_name,
          parent_name: this.form1.parent_name,
          classin_id: this.form1.classin_id,
          classin_name: this.form1.classin_name,
          birthday: this.form1.birthday,
          cc: this.form1.cc,
          old_user_username: this.form1.old_user_username,
          is_signedup: this.form1.is_signedup,
          is_paid: this.form1.is_paid,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.$message({
            message: '修改成功！',
            type: 'success',
          });
        } else {
          this.$message.error('身份错误！');
        }
      });
    },
    check(row) {
      this.showkidlist = true;
      this.axios({
        method: 'post',
        url: '/api/sup_view_customers',
        data: {
          username: row.username,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE['Identity Error']) {
          this.$message.error('身份错误!');
        } else {
          this.kidlist = response.data.list;
          this.$message({
            message: '数据已更新！',
            type: 'success',
          });
        }
      });
    },
    changeinfo(row) {
      this.dialogFormVisible1 = true;
      this.cusid = row.user_id;
    },
    edit(row) {
      this.dialogFormVisible = true;
      this.autousername = row.username;
    },
    delcustomer(row) {
      this.axios({
        method: 'post',
        url: '/api/delete_customer',
        data: {
          customer_id: row.id,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.$message({
            message: '删除成功！',
            type: 'success',
          });
        }
        if (response.data.msg === DIC.STATUS_CODE['Customer Not Found']) {
          this.$message.error('未找到客户!');
        }
        if (response.data.msg === DIC.STATUS_CODE['Identity Error']) {
          this.$message.error('身份错误!');
        }
        if (response.data.msg === DIC.STATUS_CODE['Frontend Value Error']) {
          this.$message.error('输入数据有误!');
        }
      });
    },
    del(row) {
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
        this.refresh(this.currentPage);
      });
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
          user_type: this.user,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.refresh(this.currentPage);
          this.$message({
            message: '修改成功！',
            type: 'success',
          });
        } else {
          this.$message.error('身份错误!');
        }
      });
    },
    refresh(page) {
      this.axios({
        method: 'post',
        url: '/api/sup_view_users',
        data: {
          usertype: this.user,
          username: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.edulist = response.data.list;
          this.currentPage = page;
          this.total = this.edulist.length;
          this.handleCurrentChange(this.currentPage);
          // this.$message({
          //   message: '数据已更新！',
          //   type: 'success',
          // });
        }
      });
    },
  },
};
</script>
