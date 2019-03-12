<template>
  <div>
    <img :src="url" class="head">
    <mt-swipe :auto="4000" class="swip">
      <mt-swipe-item v-for="img in imgaes" :key="img.id">
        <img :src="img.url" class="swip">
      </mt-swipe-item>
    </mt-swipe>
    <mt-navbar v-model="active">
      <mt-tab-item id="1">用户注册</mt-tab-item>
      <mt-tab-item id="2">手机验证码登录</mt-tab-item>
      <mt-tab-item id="3">手机号密码登录</mt-tab-item>
    </mt-navbar>
    <mt-tab-container v-model="active">
      <mt-tab-container-item id="1">
        <mt-field label="孩子姓名" placeholder="请输入孩子姓名"
        v-model="ruleForm2.name"></mt-field>
        <mt-field label="手机号" placeholder="请输入手机号"
        v-model="ruleForm2.tel"></mt-field>
        <mt-field label="验证码" placeholder="请输入验证码"
        v-model="ruleForm2.confirm">
          <mt-button type="default" v-show="showx"
            :disabled="!showx" @click.native="sendcodes('1')">
            发送验证码</mt-button>
          <mt-button v-show="!showx" :disabled="!showx">
            重新发送 ({{ count }}s)
          </mt-button>
        </mt-field>
        <mt-button type="primary" size="large" plain
          @click.native="register()">注册</mt-button>
      </mt-tab-container-item>
      <mt-tab-container-item id="2">
        <mt-field label="手机号" placeholder="请输入手机号"
        v-model="ruleForm.tel"></mt-field>
        <mt-field label="验证码" placeholder="请输入验证码"
        v-model="ruleForm.con">
          <mt-button type="default" v-show="show"
            :disabled="!show" @click.native="sendcodes('2')">
            发送验证码</mt-button>
          <mt-button v-show="!show" :disabled="!show">
            重新发送 ({{ count }}s)
          </mt-button>
        </mt-field>
        <mt-button type="primary" size="large" plain
        @click.native="logphone()">登录</mt-button>
      </mt-tab-container-item>
      <mt-tab-container-item id="3">
        <mt-field label="手机号" placeholder="请输入手机号"
        v-model="ruleForm3.tel"></mt-field>
        <mt-field label="密码" placeholder="请输入密码" type="password"
        v-model="ruleForm3.pass"></mt-field>
        <mt-button type="primary" size="large" plain
        @click.native="logpass()">登录</mt-button>
      </mt-tab-container-item>
    </mt-tab-container>
    <div class="foot">
      <div>
        <p>
          <br>
          Copyright © 2001-2017
          <br><br>
          全国统一咨询热线：4006062001  地址：西安市含光门外环城南路含光商务大厦6层
        <br>
        </p>
        <br>
      </div>
    </div>
  </div>
</template>
<script>
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';

export default {
  name: 'HelloWorld',
  data() {
    return {
      url: '/static/img/total.png',
      active: '1',
      show: true,
      showx: true,
      count: '',
      time: null,
      ruleForm2: {
        tel: '',
        name: '',
        confirm: '',
      },
      ruleForm: {
        con: '',
        tel: '',
      },
      ruleForm3: {
        tel: '',
        pass: '',
      },
      imgaes: [
        {
          url: '/static/img/card1.jpg',
          id: 1,
        },
        {
          url: '/static/img/picture.png',
          id: 2,
        },
        {
          url: '/static/img/card3.png',
          id: 3,
        },
      ],
    };
  },
  methods: {
    sendcodes(type) {
      if (!this.time) {
        this.count = 60;
        if (type === '1') {
          this.showx = false;
        } else {
          this.show = false;
        }
        this.axios({
          method: 'post',
          url: 'api/sendmsg',
          data: {
            tel: this.ruleForm2.tel,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then((response) => {
          if (response.data.msg === DIC.STATUS_CODE.Success) {
            this.$message({
              type: 'info',
              message: '发送成功！',
            });
          } else {
            this.$message({
              type: 'info',
              message: '发送失败！',
            });
          }
        });
        this.time = setInterval(() => {
          if (this.count > 0 && this.count <= 60) {
            this.count -= 1;
          } else {
            if (type === '1') {
              this.showx = true;
            } else {
              this.show = true;
            }
            clearInterval(this.time);
            this.time = null;
          }
        }, 1000);
      }
    },
    register() {
      if (this.ruleForm2.tel === '' || this.ruleForm2.name === ''
        || this.ruleForm2.confirm === '') {
        this.$toast({
          message: '输入不能为空',
          iconClass: 'mint-toast-icon mintui mintui-field-error',
        });
        return;
      }
      this.axios({
        method: 'post',
        url: 'customer/register',
        data: {
          username: this.ruleForm2.tel,
          child_name: this.ruleForm2.name,
          code: this.ruleForm2.confirm,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.$options.methods.submitPay(this);
        } else if (response.data.msg === DIC.STATUS_CODE['Verify Code Error']) {
          this.$alert('验证码错误', '警告', {
            confirmButtonText: '确定',
            callback: () => {
              this.$message({
                type: 'info',
                message: '注意输入正确的验证码哦！',
              });
            },
          });
        } else {
          this.$alert('客户已存在', '警告', {
            confirmButtonText: '确定',
            callback: () => {
              this.$message({
                type: 'info',
                message: '注意输入正确的孩子姓名和手机号哦！',
              });
            },
          });
        }
      });
    },
    logphone() {
      if (this.ruleForm.tel === '' || this.ruleForm.con === '') {
        this.$toast({
          message: '输入不能为空',
          iconClass: 'mint-toast-icon mintui mintui-field-error',
        });
        return;
      }
      this.axios({
        method: 'post',
        url: 'customer/login_code',
        data: {
          username: this.ruleForm.tel,
          code: this.ruleForm.con,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.$router.push({ name: 'adult',
            params: { user: this.ruleForm.tel } });
        } else if (response.data.msg === DIC.STATUS_CODE['Verify Code Error']) {
          this.$alert('验证码错误', '警告', {
            confirmButtonText: '确定',
            callback: () => {
              this.$message({
                type: 'info',
                message: '注意输入正确的验证码哦！',
              });
            },
          });
        } else if (response.data.msg === DIC.STATUS_CODE['User Not Found']) {
          this.$alert('未找到用户', '警告', {
            confirmButtonText: '确定',
            callback: () => {
              this.$message({
                type: 'info',
                message: '注意输入正确的用户名哦！',
              });
            },
          });
        } else {
          this.$alert('身份错误', '警告', {
            confirmButtonText: '确定',
            callback: () => {
              this.$message({
                type: 'info',
                message: '注意选择正确的身份哦！',
              });
            },
          });
        }
      });
    },
    logpass() {
      if (this.ruleForm3.tel === '' || this.ruleForm3.pass === '') {
        this.$toast({
          message: '输入不能为空',
          iconClass: 'mint-toast-icon mintui mintui-field-error',
        });
        return;
      }
      this.axios({
        method: 'post',
        url: 'customer/login_password',
        data: {
          username: this.ruleForm3.tel,
          password: this.ruleForm3.pass,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.$router.push({ name: 'adult',
            params: { user: this.ruleForm3.tel } });
        } else if (response.data.msg ===
        DIC.STATUS_CODE['Password Not Match']) {
          this.$alert('密码错误', '警告', {
            confirmButtonText: '确定',
            callback: () => {
              this.$message({
                type: 'info',
                message: '注意输入正确的密码哦！',
              });
            },
          });
        } else if (response.data.msg === DIC.STATUS_CODE['User Not Found']) {
          this.$alert('未找到用户', '警告', {
            confirmButtonText: '确定',
            callback: () => {
              this.$message({
                type: 'info',
                message: '注意输入正确的用户名哦！',
              });
            },
          });
        } else {
          this.$alert('身份错误', '警告', {
            confirmButtonText: '确定',
            callback: () => {
              this.$message({
                type: 'info',
                message: '注意选择正确的身份哦！',
              });
            },
          });
        }
      });
    },
  },
};
</script>
<style scoped>
.head {
  background-color: rgba(0, 153, 255, 0.945);
  width: 70%;
  height: 90px;
  margin-bottom: -40px;
}
.swip {
  margin-top: 5%;
  height: 250px;
  width: 100%;
}
.foot {
  background: #001829;
  color: #666;
  text-align: center;
}
</style>
