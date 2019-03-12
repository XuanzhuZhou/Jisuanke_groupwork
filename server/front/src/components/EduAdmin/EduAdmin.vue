<template>
  <el-container>
    <el-header class="header-bar">
      <head-bar></head-bar>
    </el-header>
    <el-container>
      <el-aside class="aside">
        <el-menu class="el-menu-vertical-demo content"
                 background-color="#48576a"
                 text-color="#bfcbd9"
                 active-text-color="#66b1ff">
          <el-menu-item index="1" class="aside-menu-item">
            <i class="el-icon-document"></i>
            <span slot="title" @click="selectHandle('1')">
              首页
            </span>
          </el-menu-item>
          <el-submenu index="2" class="aside-menu-item">
            <template slot="title">
              <i class="el-icon-mobile-phone"></i>
              <span>课程管理</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="2-1"
                            @click="selectHandle('0')"
                            class="aside-menu-item">
                销课
              </el-menu-item>
              <el-menu-item index="2-2"
                            @click="selectHandle('3')"
                            class="aside-menu-item">
                添加课程
              </el-menu-item>
              <el-menu-item index="2-3"
                            @click="selectHandle('1')"
                            class="aside-menu-item">
                修改课程
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="3" class="aside-menu-item">
            <template slot="title">
              <i class="el-icon-mobile-phone"></i>
              <span>退款管理</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="3-1"
                            @click="selectHandle('2')"
                            class="aside-menu-item">
                确认退款
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="4" class="aside-menu-item">
            <template slot="title">
              <i class="el-icon-mobile-phone"></i>
              <span>设置</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="4-1"
                            @click="selectHandle('4')"
                            class="aside-menu-item">
                修改密码
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main class="eduadmin-main">
        <el-card class="my-card">
          <div :is="currentTab"
               keep-alive>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>
<style scoped>
.aside {
  position: relative;
  max-width: 200px;
  min-height: 100vh;
  width: 200px;
}
.aside > ul {
  position: absolute;
  max-width: 200px;
  width: 100%;
  height: 100%;
}
.header-bar {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
  padding-top: 5px;
}
.my-card {
  padding: 20px;
}
</style>

<script>
import changepass from '@/components/cc/changepass';
import headbar from '@/components/cc/headbar';
import cancelClass from './cancelClass';
import searchClass from './searchClass';
import checkRefund from './checkRefund';
import addClass from './addClass';

export default {
  components: {
    'head-bar': headbar,
    'cancel-class': cancelClass,
    'search-class': searchClass,
    'check-refund': checkRefund,
    'change-password': changepass,
    'add-class': addClass,
  },
  data() {
    return {
      currentTab: 'cancel-class',
    };
  },
  methods: {
    selectHandle(handle) {
      switch (handle) {
        case '0':
          this.currentTab = 'cancel-class';
          break;
        case '1':
          this.currentTab = 'search-class';
          break;
        case '2':
          this.currentTab = 'check-refund';
          break;
        case '3':
          this.currentTab = 'add-class';
          break;
        case '4':
          this.currentTab = 'change-password';
          break;
        default:
          this.currentTab = 'cancel-class';
          break;
      }
    },
  },
};
</script>
