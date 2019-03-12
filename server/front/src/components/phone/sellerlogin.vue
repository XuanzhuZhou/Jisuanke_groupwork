<template>
<div>
  <el-card class="card">
  <div class="whitebar"></div>
  <button class="circle"></button>
  <div class="loginform">
    <el-form :model="form" status-icon :rules="rules" ref="form" class="demo-ruleForm">
      <el-form-item label="用户名" prop="username">
      <el-input v-model.number="form.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
      <el-input type="password" v-model="form.password" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item>
      <el-button type="primary" @click="submitForm('form')">提交</el-button>
      <el-button @click="resetForm('form')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
  <div class="blackbar"></div>
  </el-card>
</div>
</template>
<script>
import DIC from '@/dictionary.json';
import { getCookie } from '@/utils/utils';

export default {
  data() {
    const validatePassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else {
        callback();
      }
    };
    const validateUsername = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入用户名'));
      } else {
        callback();
      }
    };
    return {
      form: {
        username: null,
        password: null,
      },
      rules: {
        password: [
          { validator: validatePassword, trigger: 'blur' },
        ],
        username: [
          { validator: validateUsername, trigger: 'blur' },
        ],
      },
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.axios({
            method: 'post',
            url: 'api/login',
            data: {
              type: DIC.USER_TYPE.seller,
              user: this.form.username,
              password: this.form.password,
            },
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
          }).then((response) => {
            if (response.data.error === DIC.STATUS_CODE['User Not Found']
              || response.data.error === DIC.STATUS_CODE['Password Not Match']) {
              this.$alert('用户名或密码错误', '警告', {
                confirmButtonText: '确定',
                callback: () => {
                  this.$message({
                    type: 'info',
                    message: '注意修改用户名或密码哦！',
                  });
                },
              });
            } else {
              this.$router.push({ name: 'sellerpage', params: { user: this.form.username } });
            }
          });
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>
<style scoped>
.img {
    width: 100%;
    height: 100%;
}
.loginform {
    position: absolute;
    z-index: 2;
    margin: 80px 40px 0 40px;
    text-align: center;
}
.whitebar {
    position: relative;
    z-index: 1;
    background-color: white;
    margin: 0;
    height: 150px;
    width: 100%;
}
.blackbar {
    position: relative;
    z-index: 1;
    background-color: #4d4f53;
    margin: 0;
    min-height: 650px;
    width: 100%;
}
.card {
    border-style: solid;
    border-width: 5px;
}
.el-card__body {
    padding: 0;
}
.circle {
    z-index: 2;
    position: absolute;
    width: 100px;
    height: 100px;
    background-color: skyblue;
    -moz-border-radius: 50px;
    -webkit-border-radius: 50px;
    border-radius: 50px;
    margin-top: -50px;
}
</style>
