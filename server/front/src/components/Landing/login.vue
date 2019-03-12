<template>
  <div v-if="currValue === '5'" class="di">
    <img :src="img" class="headpicture">
      <center><img :src="imgUrl2" height="80px" width="220px" class="pos">
      </center>
      <div class="blocks">
      <el-tabs v-model="activeName" type="border-card" class="demos">
        <el-tab-pane label="手机号验证码登录" name="first" class="tabpage">
          <el-form :model="ruleForm" status-icon :rules="rules"
          ref="ruleForm" label-width="80px" class="form">
            <el-form-item label="手机号码" prop="tele">
              <el-input v-model="ruleForm.tele" auto-complete="off"
              placeholder="请输入手机号码"></el-input>
            </el-form-item>
            <el-form-item label="验证码" prop="con">
              <el-col :span="13">
              <el-input v-model="ruleForm.con" auto-complete="off"
              placeholder="请输入验证码" class="next"></el-input>
              </el-col>
              <el-col :span="1">
              <el-button @click="sendMsg()" v-show="show" :disabled="!show"
              class="bt" id="change">
                发送验证码
              </el-button>
              </el-col>
              <el-button v-show="!show" class="count bt" :disabled="!show">
                重新发送 ({{ count }}s)
              </el-button>
            </el-form-item>
            <el-form-item class="pos">
              <el-button type="success" @click="submitForm('ruleForm')">
                登录</el-button>
              <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="手机号密码登录" name="second" class="tabpages">
          <el-form :model="ruleForm2" status-icon :rules="rules2"
          ref="ruleForm2" label-width="80px" class="form">
            <el-form-item label="手机号码" prop="tel">
              <el-input v-model="ruleForm2.tel" auto-complete="off"
              placeholder="请输入手机号码"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="pass">
              <el-input type="password" v-model="ruleForm2.pass"
              auto-complete="off" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item class="pos">
              <el-button type="success" @click="submitForm2('ruleForm2')">
                登录</el-button>
              <el-button @click="resetForm('ruleForm2')">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
/**
 * 家长登录界面
 * @module log
 */
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';

export default {
  props: {
    initial: {
      default: '0',
    },
  },
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('密码不能为空'));
      } else {
        callback();
      }
    };
    const checkTel = (rule, value, callback) => {
      setTimeout(() => {
        if (!value) {
          callback(new Error('电话号码不能为空'));
        } else if (isNaN(value)) {
          callback(new Error('请输入数字值'));
        } else if (value.length > 18) {
          callback(new Error('手机号过长，请重新输入！'));
        } else {
          this.isSpace = false;
          callback();
        }
      }, 1);
    };
    const checkCon = (rule, value, callback) => {
      if (!value) {
        callback(new Error('验证码不能为空'));
      }
      setTimeout(() => {
        if (isNaN(value)) {
          callback(new Error('请输入数字值'));
        } else if (value.length !== 4) {
          callback(new Error('请输入正确的4位验证码！'));
        } else {
          callback();
        }
      }, 1000);
    };
    /**
     * @prop {String} img 网页图片
     * @prop {String} imgUrl 网页图片
     * @prop {String} imgUrl2 背景图片
     * @prop {String} currValue 判断显示在屏幕中央的组件
     * @prop {Boolean} show 发送验证码的按钮当前处于那种状态
     * @prop {String} count 给定验证码点击后禁止点击的时间
     * @prop {String} time 验证码点击后进入倒计时的时间变化值
     * @prop {Boolean} isSpace 判断是否应该停止验证码倒计时
     * @prop {String} activeName 判断用户选择的登录方式
     * @prop {Object} ruleForm 存放用户输入的手机号和验证码
     * @prop {Object} ruleForm2 存放用户输入的手机号和密码
     * @prop {Object} rules 手机号验证码判断规则
     * @prop {Object} rules2 手机号密码判断规则
     */
    return {
      img: '/static/img/ground.jpg',
      imgUrl: '/static/img/log.png',
      imgUrl2: '/static/img/manage.png',
      currValue: '0',
      show: true,
      count: '',
      time: null,
      isSpace: true,
      activeName: 'first',
      ruleForm: {
        con: '',
        tele: '',
      },
      ruleForm2: {
        tel: '',
        pass: '',
      },
      rules: {
        tele: [
          { validator: checkTel, trigger: 'blur' },
        ],
        con: [
          { validator: checkCon, trigger: 'blur' },
        ],
      },
      rules2: {
        tel: [
          { validator: checkTel, trigger: 'blur' },
        ],
        pass: [
          { validator: validatePass, trigger: 'blur' },
        ],
      },
    };
  },
  watch: {
    initial(nv) {
      this.currValue = nv;
    },
  },
  methods: {
    /**
     * @function submitForm
     * @description 将用户填写的电话和验证码发送给后端进行检验并给出用户能否登录成功
     * 的提示信息
     */
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$refs[formName].validate(() => {
            this.axios({
              method: 'post',
              url: 'customer/login_code',
              data: {
                username: this.ruleForm.tele,
                code: this.ruleForm.con,
              },
              headers: { 'X-CSRFToken': getCookie('csrftoken') },
            }).then((response) => {
              if (response.data.msg === DIC.STATUS_CODE.Success) {
                this.$router.push({ name: 'parent',
                  params: { user: this.ruleForm.tel } });
              } else if (response.data.msg ===
              DIC.STATUS_CODE['Verify Code Error']) {
                this.$alert('验证码错误', '警告', {
                  confirmButtonText: '确定',
                  callback: () => {
                    this.$message({
                      type: 'info',
                      message: '注意输入正确的验证码哦！',
                    });
                  },
                });
              } else if (response.data.msg ===
              DIC.STATUS_CODE['User Not Found']) {
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
          });
        }
      });
    },
    /**
     * @function submitForm2
     * @description 将用户填写的电话和密码发送给后端进行检验并给出用户能否登录成功
     * 的提示信息
     */
    submitForm2(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$refs[formName].validate(() => {
            this.axios({
              method: 'post',
              url: 'customer/login_password',
              data: {
                username: this.ruleForm2.tel,
                password: this.ruleForm2.pass,
              },
              headers: { 'X-CSRFToken': getCookie('csrftoken') },
            }).then((response) => {
              if (response.data.msg === DIC.STATUS_CODE.Success) {
                this.$router.push({ name: 'parent',
                  params: { user: this.ruleForm2.tel } });
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
              } else if (response.data.msg ===
              DIC.STATUS_CODE['User Not Found']) {
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
          });
        }
      });
    },
    /**
     * @function resetForm
     * @description 清空输入框的内容
     */
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    /**
     * @function sendMsg
     * @description 用于向后端传送用户输入的手机号并发送手机验证码
     */
    sendMsg() {
      if (!this.time && !this.isSpace) {
        this.count = 60;
        this.show = false;
        this.axios({
          method: 'post',
          url: 'api/sendmsg',
          data: {
            tel: this.ruleForm.tele,
          },
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then((response) => {
          if (response.data.error === DIC.STATUS_CODE.Success) {
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
            this.show = true;
            clearInterval(this.time);
            this.time = null;
            this.isSpace = true;
          }
        }, 1000);
      }
    },
  },
};
</script>

<style scoped>
.pos {
  margin: 90px 0 auto 0;
}
el-form-item {
  margin-top: 20px;
  margin-bottom: 40px;
}
.headpicture {
  width: 100%;
  height: 100%;
  position: fixed;
  z-index: -1;
}
.blocks {
  background-color: white;
  width: 380px;
  margin: 0 auto;
  margin: 80px auto auto auto;
  position: relative;
  transform: translateY(-20%);
  border-radius: 5px;
}
.form {
  padding: 15px;
}
.next {
  width: 90%;
}
.el-form-item {
  margin-top: 20px;
  margin-bottom: 40px;
}
.el-tabs__item {
  padding: 20px;
  height: 80px;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  display: inline-block;
  list-style: none;
  font-size: 20px;
  font-weight: 500;
  color: #303133;
  position: relative;
}
.count {
  max-width: 107px;
}
.el-tabs__item.is-active {
  color: #67c23a;
}
.el-tabs__active-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  background-color: #67c23a;
}
.el-tabs__item:hover {
  color: #67c23a;
  cursor: pointer;
}
.el-tabs__item.is-active {
  color: #67c23a;
}
.el-checkbox__input.is-checked+.el-checkbox__label {
  color: #67c23a;
}
.el-checkbox__input.is-checked .el-checkbox__inner,
.el-checkbox__input.is-indeterminate .el-checkbox__inner {
  background-color: #67c23a;
  border-color: #67c23a;
}
.el-checkbox__inner:hover {
  border-color: #67c23a;
}
.el-tabs--border-card>.el-tabs__header .el-tabs__item.is-active {
  color: #67c23a;
  background-color: #fff;
  border-right-color: #dcdfe6;
  border-left-color: #dcdfe6;
}
.el-tabs__item {
  padding: 0 20px;
  width: 70%;
  height: 40px;
  box-sizing: border-box;
  line-height: 40px;
  display: inline-block;
  list-style: none;
  font-size: 14px;
  font-weight: 500;
  position: relative;
}
</style>
