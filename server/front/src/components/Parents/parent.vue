<template>
  <div class="til">
    <el-row :gutter="10" class="rows">
      <el-col :xs="1" :sm="2" :md="2" :lg="2" :xl="4">
        <img :src="imgUrl" height="60px" width="320px" class="image">
      </el-col>
      <el--col>
        <el-button class="el-icon-circle-close" id="lab" @click="quit()"
        round>退出登录</el-button>
        <h4>欢迎您，{{ this.$route.params.user }}用户！</h4>
      </el--col>
    </el-row>
    <el-row :gutter="10">
      <el-col :xs="40" :sm="27" :md="28" :lg="29" :xl="21">
        <el-menu :default-active="activeIndex2" class="el-menu-demo"
        mode="horizontal" background-color="#545c64"
        text-color="#fff" active-text-color="#F7D02E">
          <el-menu-item index="2" @click="board('2')" class="childmsg">
            查看孩子信息</el-menu-item>
          <el-menu-item index="3" @click="board('3')" class="childmsg">
            查看课程信息</el-menu-item>
          <el-menu-item index="5" @click="board('5')" class="childmsg">
            申请退款</el-menu-item>
          <el-menu-item index="6" @click="board('6')" class="childmsg">
            修改密码</el-menu-item>
          <el-menu-item index="7" @click="board('7')" class="childmsg">
            付费</el-menu-item>
          <el-menu-item index="1" @click="board('1')" class="childmsg">
            电子合同与发票</el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
    <div class="contents">
      <el-row :gutter="10">
        <el-col :xs="40" :sm="27" :md="28" :lg="29" :xl="21">
          <formula :initial="initial" :username="username"></formula>
          <childInformation :initial="initial" :username="username">
          </childInformation>
          <syllabus :initial="initial" :username="username"></syllabus>
          <refund :initial="initial" :username="username"></refund>
          <changePass :initial="initial" :username="username"></changePass>
          <payFee :initial="initial" :username="username"></payFee>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
/**
 * 家长页面的基础界面
 * @module parent
 */
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';
import formula from './formula';
import childInformation from './childInformation';
import syllabus from './syllabus';
import refund from './refund';
import changePass from './changePass';
import payFee from './payFee';

export default {
  /**
   * @prop {String} imgUrl 图片地址信息
   * @prop {Boolean} username 从家长登录页获取的用户名（电话号码）
   * @prop {String} activeIndex 需要显示的页面
   */
  data() {
    return {
      imgUrl: '/static/img/headpic.png',
      isCollapse: true,
      username: this.$route.params.user,
      activeIndex: '1',
      activeIndex2: '1',
      initial: '1',
    };
  },
  /**
   * Components 包含子组件
   * @prop {Component} formula 查看电子合同和电子发票
   * @prop {Component} childInformation 查看孩子信息
   * @prop {Component} syllabus 查看课程和课节信息
   * @prop {Component} refund 获取退款信息并申请退款
   * @prop {Component} changePass 更改密码功能
   * @prop {Component} payFee 家长支付课程
   */
  components: {
    formula,
    childInformation,
    syllabus,
    refund,
    changePass,
    payFee,
  },
  methods: {
    /**
     * @function board
     * @description 更改需要显示的页面
     */
    board(value) {
      this.initial = value;
    },
    /**
     * @function quit
     * @description 家长登出页面并给后端发送请求
     */
    quit() {
      this.axios({
        method: 'post',
        url: 'api/logout',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.$router.push({ name: 'Heading' });
        }
      });
    },
  },
};
</script>

<style scoped>
.til {
  position: relative;
}
h4 {
  float: right;
  margin-top: 20px;
  margin-right: 4%;
}
#lab {
  float: right;
  margin-top: 13px;
  margin-right: 4%;
 }
.rows {
  width: 1300px;
}
.image {
  margin-left: 80px;
}
.el-menu-demo {
  padding-left: 75px;
}
.contents {
  background-color: #f0f0f0;
  width: 100%;
  height: 100%;
  position: fixed;
  z-index: -1;
}
.childmsg {
  font-size: 17px;
  font-family: "微软雅黑";
}
</style>
