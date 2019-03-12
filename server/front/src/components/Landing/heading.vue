<template>
  <div>
    <div class="dem">
      <el-menu class="el-menu-demo" mode="horizontal"
      :default-active="activeIndex"
      text-color="#000000" active-text-color="#8EC63D">
        <el-menu-item index="10"><img :src="imgUrl" id="image"
        height="50px"></el-menu-item>
        <el-menu-item index="0" @click="show('0')">首页</el-menu-item>
        <el-menu-item index="1" @click="show('1')">关于我们</el-menu-item>
        <el-button size="medium" class="reg" index="5" @click="show('5')">
          登录</el-button>
        <el-button size="medium" class="reg" index="6" @click="show('6')">
          注册</el-button>
      </el-menu>
    </div>
    <page :initial="initial" :username="username"></page>
    <about :initial="initial" :username="username"></about>
    <register :initial="initial" :username="username"></register>
    <log :initial="initial" :username="username"></log>
    <div class="foot" v-if="this.initial === '0' || this.initial === '1'">
      <p>
        <br>全国免费课程咨询预约热线：4006062001&nbsp;&nbsp;&nbsp;&nbsp;
          工作时间：9：00-17:00&nbsp;&nbsp;&nbsp;&nbsp;</p>
      <div class="footers">
        <p>
          Copyright © 2001-2017
          陕ICP备13008117号-1 版权所有:西安东亚西文培训中心
        <br>
          全国统一咨询热线：4006062001  地址：西安市含光门外环城南路含光商务大厦6层
        <br>
        </p>
        <br>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * 落地页面头部导航条组件
 * @module heading
 */
import page from './page.vue';
import register from './register.vue';
import log from './login.vue';
import about from './aboutUs.vue';

export default {
  /**
   * @prop {Component} page 落地页主要页面
   * @prop {Component} register 家长注册页面组件
   * @prop {Component} log 家长登录界面组件
   * @prop {Componen} about 落地页关于我们企业介绍部分
   */
  components: {
    page,
    register,
    log,
    about,
  },
  data() {
    return {
      activeIndex: '0',
      initial: '0',
      imgUrl: '/static/img/logohead.png',
      username: 'bay',
    };
  },
  methods: {
    /**
     * @function show
     * @description 修改所要显示的组件
     */
    show(value) {
      this.initial = value;
    },
  },
};
</script>

<style scoped>
.el-menu-demo {
  margin: 0 auto;
  transition: linear;
  padding-left: 70px;
  padding-right: 75px;
}
.reg {
  float: right;
  margin: 13px;
}
.foot {
  background: #001829;
  color: white;
  margin-top: -15px;
}
p {
  text-align: center;
}
.dem {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
}
.footers {
  font-size: 12px;
}
.el-menu--horizontal {
  border-right: none;
  border-bottom: none;
}
</style>
