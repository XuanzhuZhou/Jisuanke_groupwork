<template>
  <div :style="node" class="head">
    <div class="contain">
      <div class="headwords">
        <img :src="imgUrl" width="40%" height="50px">
      </div>
      <mt-button class="toggle" @click.native="show()">
        <span></span>
        <span></span>
        <span></span>
      </mt-button>
      <router-link to="/land" slot="right">
        <mt-button @click.native="quit()" class="exi">退出 ></mt-button>
      </router-link>
      <mt-popup class="nav" v-model="popupVisible" position="left">
        <ul class="ope"></ul>
        <ul>
          <li>
            <a class="child" @click="relation('1')">查看孩子信息</a>
          </li>
          <li>
            <a class="child" @click="relation('2')">查看课程信息</a>
          </li>
          <li>
            <a class="child" @click="relation('3')">申请退款</a>
          </li>
          <li>
            <a class="child" @click="relation('4')">修改密码</a>
          </li>
          <li>
            <a class="child" @click="relation('5')">课程付费</a>
          </li>
        </ul>
      </mt-popup>
    </div>
    <div class="content">
      <human :initial="initial" :username="username"></human>
      <courses :initial="initial" :username="username"></courses>
      <fund :initial="initial" :username="username"></fund>
      <password :initial="initial" :username="username"></password>
      <pay :initial="initial" :username="username"></pay>
    </div>
  </div>
</template>

<script>
/**
 * 手机端家长页面
 * @module adult
 */
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';
import human from './human';
import courses from './courses';
import fund from './fund';
import password from './password';
import pay from './pay';

const picture = require('../../../static/img/phone.png');

export default {
  data() {
    return {
      popupVisible: false,
      initial: '0',
      imgUrl: '/static/img/pic.png',
      username: this.$route.params.user,
      node: {
        backgroundImage: `url(${picture})`,
        backgroundSize: '100% 100%',
      },
    };
  },
  /**
   * Components 包含子组件
   * @prop {Component} human 查看孩子信息组件
   * @prop {Component} courses 查看孩子课程信息组件
   * @prop {Component} fund 申请退款组件
   * @prop {Component} password 修改按钮部分组件
   * @prop {Component} pay 家长支付课程组件
   */
  components: {
    human,
    courses,
    fund,
    password,
    pay,
  },
  methods: {
    /**
     * @function relation
     * @description 设置侧边栏状态是否可见
     */
    relation(value) {
      this.initial = value;
      this.popupVisible = !this.popupVisible;
    },
    /**
     * @function show
     * @description 设置侧边栏状态转换
     */
    show() {
      this.popupVisible = !this.popupVisible;
    },
    /**
     * @function quit
     * @description 用户退出登录时告诉后端用户已退出登录并转换到登录界面
     */
    quit() {
      this.axios({
        method: 'post',
        url: 'api/logout',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.$router.push({ name: 'land' });
        }
      });
    },
  },
};
</script>

<style scoped>
.head {
  height: 600px;
  width: 100%;
}
.toggle {
  display: block;
  background-color: #62696f;
  border-radius: 4px;
  border: 1px solid #fff;
  height: 35px;
  margin: -50px 0 15px;
  padding: 2px 6px;
  outline: none;
  width: 35px;
  z-index: 10;
}
span {
  display: block;
  width: 100%;
  height: 2px;
  margin: 4px auto;
  background-color: #fff;
}
.contain {
  box-sizing: border-box;
  display: block;
  position: fixed;
  padding-left: 10px;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #62696f;
  z-index: 10;
}
.headwords {
  text-align: center;
  color: white;
  display: block;
  font-size: 25px;
  margin: 17px 0 -26px -15px;
}
.nav {
  background-color: #f9fafb;
  color: #4c555a;
  font-size: 14px;
  min-height: 100%;
  width: 55%;
  padding: 42px 60px 42px 20px;
}
ul {
  color: #9da5b3;
  font-weight: 700;
  padding: 8px;
  display: block;
}
li {
  padding: 8px;
  display: block;
  text-decoration: none;
  color: inherit;
  transition: color .2s;
}
.child {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
  Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  font-size: 18px;
  color: #28292bd0;
}
.content {
  margin-top: 70px;
}
.ope {
  background-color: rgba(0, 0, 0, 0.925);
  color: whitesmoke;
  text-align: center;
  font-size: 20px;
  height: 150px;
  width: 130%;
  margin-left: -20px;
  margin-top: -15px;
}
.exi {
  background-color: #62696f;
  color: whitesmoke;
  border: 1px solid #62696f;
  float: right;
  margin-top: -53px;
}
</style>
