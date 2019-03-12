<template>
<div>
  <div class="navbar">
  <mt-header>
    <label>欢迎您！{{this.$route.params.user}}</label>
    <mt-button icon="more" slot="right" @click="popupVisible = true"></mt-button>
  </mt-header>
  </div>
  <mt-popup v-model="popupVisible" position="bottom">
    <div @click="showqrcode()" class ="bottomnavbar">查看二维码</div>
    <div @click="showcenter()" class ="bottomnavbar">个人中心</div>
  </mt-popup>
  <div class="qrcode" v-show ="showindex === 1">
    <qrcode></qrcode>
  </div>
  <div v-show ="showindex === 2" class="center">
    <el-card shadow="always">
      <img :src=pics>
      <div class="item2">姓名:{{this.$route.params.user}}</div>
      <div class="item2"><mt-button plain @click="changepass()">修改密码</mt-button></div>
      <div class="item2"><mt-button plain @click="logout()">退出登录</mt-button></div>
    </el-card>
  </div>
  <el-dialog :visible.sync="dialogFormVisible">
    <changepass></changepass>
  </el-dialog>
</div>
</template>
<script>
import DIC from '@/dictionary.json';
import { getCookie } from '@/utils/utils';
import changepass from '@/components/cc/changepass';
import qrcode from '@/components/sellers/qrcode';

export default {
  components: {
    changepass,
    qrcode,
  },
  data() {
    return {
      pics: '/static/img/go.png',
      name: this.$route.params.user,
      showindex: 2,
      shownavbar: true,
      popupVisible: false,
      dialogFormVisible: false,
    };
  },
  methods: {
    logout() {
      this.axios({
        method: 'post',
        url: 'api/logout',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.$router.push({ name: 'sellerlogin' });
        }
      });
    },
    changepass() {
      this.dialogFormVisible = true;
    },
    getQRcode() {
      this.axios({
        method: 'post',
        url: 'user/qrcode',
        data: {
          name: this.$route.params.user,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        this.picture = response.data.path;
      });
    },
    showqrcode() {
      this.showindex = 1;
      this.popupVisible = false;
    },
    showcenter() {
      this.showindex = 2;
      this.popupVisible = false;
    },
  },
  mounted() {
    this.axios({
      method: 'post',
      url: 'user/qrcode',
      data: {
        name: this.$route.params.user,
      },
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
    }).then((response) => {
      this.picture = response.data.path;
    });
  },
};
</script>
<style scoped>
.mint-popup, .mint-popup-bottom {
  width: 100%;
}
.bottomnavbar {
  width: 100%;
  text-align: center;
  height: 45px;
}
.mint-header {
  background-color: #23304a;
  height: 55px;
}
.navbar {
  margin-bottom: 5px;
}
.center {
  margin: 50px 10% 0 10%;
  height: 500px;
  width: 80%;
}
.item2 {
  margin: 50px 25% 50px 25%;
}
.el-dialog {
  width: 90%;
}
.demo-ruleForm {
  margin: 5% 5% 1% 5%;
}
</style>
