<template>
  <el-container>
    <el-header><headbar></headbar></el-header>
    <el-container>
    <el-aside width="200px">
        <el-menu
            class="el-menu-vertical-demo"
            background-color="#48576a"
            text-color="#bfcbd9"
            active-text-color="#66b1ff">
          <el-menu-item index="1" v-on:click="onMain()">
          <i class="el-icon-menu"></i>
          <span slot="title" class=main>首页</span>
          </el-menu-item>
        <el-submenu index="2">
          <template slot="title">
          <i class="el-icon-menu"></i>
          <span>人员管理</span>
          </template>
          <el-menu-item-group>
          <el-menu-item index="2-1" @click="onEduAdminList()">教务老师列表</el-menu-item>
          <el-menu-item index="2-2" @click="onCcList()">课程顾问列表</el-menu-item>
          <el-menu-item index="2-3" @click="onSellerList()">地推人员列表</el-menu-item>
          <el-menu-item index="2-4" @click="onCustomerList()">客户列表</el-menu-item>
          <el-menu-item index="2-5" @click="onAssign()">分配课程顾问</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title">
          <i class="el-icon-circle-plus-outline"></i>
          <span>添加数据</span>
          </template>
          <el-menu-item-group>
          <el-menu-item index="3-1" @click="onThird()">导入第三方数据</el-menu-item>
          <el-menu-item index="3-2" @click="onAddCc()">添加课程顾问</el-menu-item>
          <el-menu-item index="3-3" @click="onAddSeller()">添加地推人员</el-menu-item>
          <el-menu-item index="3-4" @click="onAddEduAdmin()">添加教务老师</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-menu-item index="4" v-on:click="onLog()">
          <i class="el-icon-document"></i>
          <span slot="title">查看日志</span>
        </el-menu-item>
        <el-submenu index="5">
          <template slot="title">
          <i class="el-icon-news"></i>
          <span>查看业绩</span>
          </template>
          <el-menu-item-group>
          <el-menu-item index="5-1" @click="onSellerSales()">地推业绩</el-menu-item>
          <el-menu-item index="5-2" @click="onCcSales()">课程顾问业绩</el-menu-item>
          <el-menu-item index="5-3" @click="onTeacherSales()">试听课老师业绩</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="6">
          <template slot="title">
          <i class="el-icon-setting"></i>
          <span>设置</span>
          </template>
          <el-menu-item-group>
          <el-menu-item index="6-1" @click="onChangePass()">修改密码</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        </el-menu>
    </el-aside>
      <el-main>
        <transition name="el-zoom-in-center">
        <mainpage v-if="showindex === 1" :initial="initial"></mainpage>
        <changepass  v-if="showindex === 2" :name="name" :initial="initial"></changepass>
        <memList :usertype="user_type" v-if="showindex === 3" :initial="initial"></memList>
        <memList :usertype="user_type" v-if="showindex === 4" :initial="initial"></memList>
        <memList :usertype="user_type" v-if="showindex === 5" :initial="initial"></memList>
        <CustomerList v-if="showindex === 6" :initial="initial"></CustomerList>
        <AddThird :initUrl="url.importFileUrl" v-if="showindex === 7" :initial="initial">
        </AddThird>
        <AddCc v-if="showindex === 8" :initial="initial"></AddCc>
        <AddSeller v-if="showindex === 9" :initial="initial"></AddSeller>
        <AddEduAdmin v-if="showindex === 10" :initial="initial"></AddEduAdmin>
        <log  v-if="showindex === 11" :initial="initial"></log>
        <ccsales  v-if="showindex === 12" :initial="initial"></ccsales>
        <sellersales  v-if="showindex === 13" :initial="initial"></sellersales>
        <teachersales  v-if="showindex === 14" :initial="initial"></teachersales>
        <assigncc v-if="showindex=== 15" :initial="initial"></assigncc>
        </transition>
      </el-main>
    </el-container>
  </el-container>
</template>
<style scoped>
.el-card is-hover-shadow {
  margin: 20px;
}
.el-menu-vertical-demo {
  background-color: #909399;
}
.el-submenu__title {
  background-color: #48576a;
}
.el-header, .el-footer {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
}
.el-aside {
  background-color: #48576a;
  color: #333;
  text-align: left;
  line-height: 200px;
  min-height: 960px;
}
.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
}
body > .el-container {
  margin-bottom: 40px;
}
.el-submenu__title {
  color: #715b5b;
}
.el-menu-item {
    color: #715b5b;
}
.el-menu-item is-active{
  color: #daa103;
}
.el-menu {
  border-right: 0;
}
</style>
<script>
import changepass from '@/components/cc/changepass';
import DIC from '@/dictionary.json';
import headbar from '@/components/cc/headbar';
import log from './log';
import assigncc from './assigncc';
import memList from './memList';
import AddThird from './AddThird';
import AddCc from './AddCc';
import AddSeller from './AddSeller';
import AddEduAdmin from './AddEduAdmin';
import ccsales from './ccsales';
import sellersales from './sellersales';
import teachersales from './teachersales';
import CustomerList from './CustomerList';
import mainpage from './mainpage';

export default {
  components: {
    changepass,
    headbar,
    log,
    assigncc,
    memList,
    AddThird,
    AddCc,
    AddSeller,
    AddEduAdmin,
    ccsales,
    sellersales,
    CustomerList,
    mainpage,
    teachersales,
  },
  data() {
    return {
      initial: '0',
      showindex: 1,
      name: this.$route.params.user,
      user_type: 10,
      url: {
        importFileUrl: 'api/sup_import_customer',
      },
    };
  },
  methods: {
    onMain() {
      this.showindex = 1;
      this.initial = '1';
    },
    onEduAdminList() {
      this.showindex = 3;
      this.user_type = DIC.USER_TYPE.eduadmin;
      this.initial = '3';
    },
    onSellerList() {
      this.showindex = 5;
      this.user_type = DIC.USER_TYPE.seller;
      this.initial = '5';
    },
    onCustomerList() {
      this.showindex = 6;
      this.initial = '6';
    },
    onAssign() {
      this.showindex = 15;
      this.initial = '15';
    },
    onThird() {
      this.showindex = 7;
      this.initial = '7';
    },
    onAddCc() {
      this.showindex = 8;
      this.initial = '8';
    },
    onAddSeller() {
      this.showindex = 9;
      this.initial = '9';
    },
    onAddEduAdmin() {
      this.showindex = 10;
      this.initial = '10';
    },
    onSellerSales() {
      this.showindex = 13;
      this.initial = '13';
    },
    onCcSales() {
      this.showindex = 12;
      this.initial = '12';
    },
    onTeacherSales() {
      this.showindex = 14;
      this.initial = '14';
    },
    onCcList() {
      this.showindex = 4;
      this.initial = '4';
      this.user_type = DIC.USER_TYPE.consultant;
    },
    onLog() {
      this.showindex = 11;
      this.initial = '11';
    },
    onChangePass() {
      this.showindex = 2;
      this.initial = '2';
    },
  },
  beforeCreate() {
  },
  toggleSelection(rows) {
    if (rows) {
      rows.forEach((row) => {
        this.$refs.multipleTable.toggleRowSelection(row);
      });
    } else {
      this.$refs.multipleTable.clearSelection();
    }
  },
  handleSelectionChange(val) {
    this.multipleSelection = val;
  },
};
</script>
