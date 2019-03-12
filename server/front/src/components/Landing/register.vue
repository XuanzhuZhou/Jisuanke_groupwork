<template>
  <div v-if="currValue === '6'" class="di">
    <el-row>
      <img :src="img" class="headpicture">
      <el-col :span="4" :offset="10">
        <img :src="imgUrl2" height="80px" width="220px">
      </el-col>
      <div class="blocks">
        <el-form :model="ruleForm2" status-icon :rules="rules2" ref="ruleForm2"
        label-width="80px" class="form">
          <el-form-item label="孩子姓名" prop="name">
            <el-input v-model.number="ruleForm2.name"
            placeholder="请输入孩子姓名"></el-input>
          </el-form-item>
          <el-form-item label="电话号码" prop="tel">
            <el-input v-model="ruleForm2.tel" auto-complete="off"
            placeholder="请输入手机号码"></el-input>
          </el-form-item>
          <el-form-item label="验证码" prop="confirm">
            <el-col :span="14">
            <el-input v-model="ruleForm2.confirm" placeholder="请输入验证码"
            auto-complete="off" class="next"></el-input>
            </el-col>
            <el-col :span="6">
            <el-button id="changeshow" @click="sendMsg()" v-show="show"
            :disabled="!show">
              发送验证码
            </el-button>
            <el-button v-show="!show" class="count" :disabled="!show">
              重新发送 ({{ count }}s)
            </el-button>
            </el-col>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="submitForm('ruleForm2')">
              注册</el-button>
            <el-button @click="resetForm('ruleForm2')">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-row>
  </div>
</template>

<script>
/**
 * 家长注册页面
 * @module register
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
    const checkName = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入孩子姓名'));
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
     * @prop {String} img 页面图片路径
     * @prop {String} imgUrl 页面图片路径
     * @prop {String} imgUrl2 页面图片路径
     * @prop {String} currValue 页面需要显示的组件
     * @prop {Boolean} show 发送验证码按钮的状态显示
     * @prop {String} count 发送验证码后的等待时间
     * @prop {String} time 发送验证码后倒计时的时间
     * @prop {Boolean} isSpace  判断是否应该停止验证码倒计时
     * @prop {Boolean} isSuccess 根据后端传送的信息判断是否注册成功
     * @prop {Object} ruleForm2 存放家长注册时填入的电话、姓名和验证码
     * @prop {Object} rules2 给输入框加上判断条件
     */
    return {
      img: '/static/img/ground.jpg',
      imgUrl: '/static/img/regis.png',
      imgUrl2: '/static/img/manage.png',
      currValue: '0',
      show: true,
      count: '',
      time: null,
      isSpace: true,
      isSuccess: true,
      ruleForm2: {
        tel: '',
        name: '',
        confirm: '',
      },
      rules2: {
        tel: [
          { validator: checkTel, trigger: 'blur' },
        ],
        name: [
          { validator: checkName, trigger: 'blur' },
        ],
        confirm: [
          { validator: checkCon, trigger: 'blur' },
        ],
      },
    };
  },
  watch: {
    initial(nv) {
      this.currValue = nv;
      this.isSuccess = true;
    },
  },
  methods: {
    /**
     * @function getParams
     * @description 获取url中的地推人员ID情况
     */
    getParams() {
      const url = window.location.href;
      if (url.indexOf('?') !== -1) {
        return url.split('=')[1];
      }
      return '-1';
    },
    /**
     * @function submitPay
     * @description 向后端发送用户注册成功并提出支付请求
     */
    submitPay(that) {
      const msg = {};
      msg.tel = that.ruleForm2.tel;
      msg.child_name = that.ruleForm2.name;
      msg.seller_id = that.$options.methods.getParams();
      that.axios({
        method: 'post',
        url: 'api/payviews',
        data: msg,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        window.open(response.data.url);
        that.$confirm('支付情况', '提示', {
          confirmButtonText: '支付成功',
          cancelButtonText: '支付遇到问题',
          type: 'success',
        }).then(() => {
          that.$message({
            type: 'success',
            message: '快去享受试听盛宴吧!',
          });
          that.axios({
            method: 'post',
            url: 'customer/register_success',
            data: {
              username: that.ruleForm2.tel,
              child_name: that.ruleForm2.name,
            },
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
          });
        }).catch(() => {
          that.$message({
            type: 'info',
            message: '注意查看您的支付账户哦！',
          });
        });
      });
    },
    /**
     * @function submitForm
     * @description 将用户填入的数据发送给后端并验证用户能够正常注册成功
     */
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
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
              this.$alert('注册成功，您的初始密码为手机号后六位', '恭喜您', {
                confirmButtonText: '确定',
                callback: () => {
                  this.$message({
                    type: 'info',
                    message: '快去登录吧！',
                  });
                },
              });
              this.$options.methods.submitPay(this);
              this.isSuccess = false;
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
        }
      });
    },
    /**
     * @function resetForm
     * @description 清空用户输入框中的内容
     */
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    /**
     * @function sendMsg
     * @description 给后端发送手机号并发送给家长手机验证码
     */
    sendMsg() {
      if (!this.time && !this.isSpace) {
        this.count = 60;
        this.show = false;
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
.count {
  max-width: 135px;
}
.el-form-item {
  margin-top: 20px;
  margin-bottom: 40px;
}
.form {
  padding: 15px;
}
.headpicture {
  width: 100%;
  height: 100%;
  position: fixed;
  z-index: -1;
  margin-top: -38px;
}
.blocks {
  background-color: white;
  width: 380px;
  margin: 80px auto auto auto;
  position: relative;
  border-radius: 5px;
}
.di {
  margin-top: 100px;
  height: 500px;
}
.spice {
  width: 0;
  border: 1px solid rgba(128, 128, 128, 0.208);
  position: relative;
  left: 45%;
  height: 400px;
}
.demos {
  margin-left: 40%;
  margin-top: -350px;
  width: 45%;
}
h2 {
  position: relative;
  margin-left: 90px;
}
p {
  margin-left: 40px;
  margin-right: -30px;
}
.next {
  width: 88%;
}
.count {
  margin-left: -23px;
}
.bt {
  position: relative;
  left: 337px;
  top: -62px;
}
.message {
  margin-top: -350px;
}
</style>
