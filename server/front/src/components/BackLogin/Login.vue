<template>
  <div :style="node" class="headpicture">
    <el-row :gutter="20" class="rows">
      <el-col :span="7.5" :offset="9">
        <img :src="imgUrl" height="150px" width="380px">
        <el-tabs v-model="activeName"
        :tab-position="tabPosition" class="formu">
          <el-tab-pane label="地推人员" name="5">
            <el-form :model="ruleForm2" status-icon
            :rules="rules2" ref="ruleForm2"
            label-width="50px" class="demo-ruleForm">
              <el-form-item label="用户名" prop="user" label-width="80px"
              class="input">
                <el-input style="width:250px;" v-model.number="ruleForm2.user"
                auto-complete="on" placeholder="请输入用户名"></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="pass" label-width="80px"
              class="input">
                <el-input style="width:250px;" type="password"
                v-model="ruleForm2.pass"
                auto-complete="off" placeholder="请输入密码">
                </el-input>
              </el-form-item>
              <el-row>
                <el-col :span="6" :offset="5"><el-checkbox>
                  记住我
                </el-checkbox></el-col>
                <el-col :span="8" :offset="4"><a href="">
                  忘记密码？
                </a></el-col>
              </el-row>
              <el-form-item class="item">
                <el-button type="success" @click="submitForm('ruleForm2')">
                  登录</el-button>
                <el-button @click="resetForm('ruleForm2')" id="reset">
                  重置</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="课程顾问" name="3">
            <el-form :model="ruleForm2" status-icon :rules="rules2"
            ref="ruleForm2" label-width="50px" class="demo-ruleForm">
              <el-form-item label="用户名" prop="user" label-width="80px"
              class="input">
                <el-input style="width:250px;" v-model.number="ruleForm2.user"
                auto-complete="on" placeholder="请输入用户名">
                </el-input>
              </el-form-item>
              <el-form-item label="密码" prop="pass" label-width="80px"
              class="input">
                <el-input style="width:250px;" type="password"
                v-model="ruleForm2.pass"
                auto-complete="off" placeholder="请输入密码">
                </el-input>
              </el-form-item>
              <el-row>
                <el-col :span="6" :offset="5"><el-checkbox>
                  记住我</el-checkbox></el-col>
                <el-col :span="8" :offset="4"><a href="">忘记密码？
                  </a></el-col>
              </el-row>
              <el-form-item class="item">
                <el-button type="success" @click="submitForm('ruleForm2')">
                  登录</el-button>
                <el-button @click="resetForm('ruleForm2')">重置</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="教务老师" name="4">
            <el-form :model="ruleForm2" status-icon :rules="rules2"
            ref="ruleForm2" label-width="50px" class="demo-ruleForm">
              <el-form-item label="用户名" prop="user" label-width="80px"
              class="input">
                <el-input style="width:250px;" v-model.number="ruleForm2.user"
                auto-complete="on" placeholder="请输入用户名">
                </el-input>
              </el-form-item>
              <el-form-item label="密码" prop="pass" label-width="80px"
              class="input">
                <el-input style="width:250px;" type="password"
                v-model="ruleForm2.pass"
                auto-complete="off" placeholder="请输入密码">
                </el-input>
              </el-form-item>
              <el-row>
                <el-col :span="6" :offset="5"><el-checkbox>
                  记住我</el-checkbox></el-col>
                <el-col :span="8" :offset="4"><a href="">
                  忘记密码？</a></el-col>
              </el-row>
              <el-form-item class="item">
                <el-button type="success" @click="submitForm('ruleForm2')">
                  登录</el-button>
                <el-button @click="resetForm('ruleForm2')">重置</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="超级管理员" name="2">
            <el-form :model="ruleForm2" status-icon :rules="rules2"
            ref="ruleForm2" label-width="50px" class="demo-ruleForm">
              <el-form-item label="用户名" prop="user" label-width="80px"
               class="input">
                <el-input style="width:250px;" v-model.number="ruleForm2.user"
                auto-complete="on" placeholder="请输入用户名">
                </el-input>
              </el-form-item>
              <el-form-item label="密码" prop="pass" label-width="80px"
               class="input">
                <el-input style="width:250px;" type="password"
                v-model="ruleForm2.pass"
                auto-complete="off" placeholder="请输入密码">
                </el-input>
              </el-form-item>
              <el-row>
                <el-col :span="6" :offset="5"><el-checkbox>
                  记住我</el-checkbox></el-col>
                <el-col :span="8" :offset="4"><a href="">
                  忘记密码？</a></el-col>
              </el-row>
              <el-form-item class="item">
                <el-button type="success" @click="submitForm('ruleForm2')">
                  登录</el-button>
                <el-button @click="resetForm('ruleForm2')">重置</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>

<script>
/**
 * 后台管理人员登录界面（地推人员、课程顾问、教务老师、超级管理员）
 * @module adult
 */
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';

const picture = require('../../../static/img/ground.jpg');

export default {
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else {
        callback();
      }
    };
    const validateUser = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入用户名'));
      } else {
        callback();
      }
    };
    /**
     * @prop {String} imgUrl 存放背景图片地址
     * @prop {String} tabPosition 设置标签页的位置
     * @prop {String} activeName 需要显示的组件名称
     * @prop {Object} ruleForm2 存放用户输入的用户名和密码
     * @prop {Object} rules2 存放
     * @prop {Object} node 存放背景图片的地址和大小
     */
    return {
      imgUrl: '/static/img/manage.png',
      tabPosition: 'top',
      activeName: '5',
      csrf: getCookie('csrftoken'),
      ruleForm2: {
        user: '',
        pass: '',
      },
      rules2: {
        pass: [
          { validator: validatePass, trigger: 'blur' },
        ],
        user: [
          { validator: validateUser, trigger: 'blur' },
        ],
      },
      node: {
        backgroundImage: `url(${picture})`,
        backgroundSize: '100% 100%',
      },
    };
  },
  methods: {
    /**
     * @function submitForm
     * @description 向后端发送用户填写的用户名密码的表单数据并给出提示
     */
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.axios({
            method: 'post',
            url: 'api/login',
            data: {
              type: this.activeName,
              user: this.ruleForm2.user,
              password: this.ruleForm2.pass,
            },
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
          }).then((response) => {
            if (response.data.error === DIC.STATUS_CODE['User Not Found']
                || response.data.error ===
                DIC.STATUS_CODE['Password Not Match']) {
              this.$alert('用户名或密码错误', '警告', {
                confirmButtonText: '确定',
                callback: () => {
                  this.$message({
                    type: 'info',
                    message: '注意修改用户名或密码哦！',
                  });
                },
              });
            } else if (response.data.error ===
            DIC.STATUS_CODE['Identity Error']) {
              this.$alert('身份信息不匹配', '警告', {
                confirmButtonText: '确定',
                callback: () => {
                  this.$message({
                    type: 'info',
                    message: '注意选择合适的身份信息哦！',
                  });
                },
              });
            } else if (this.activeName === '5') {
              this.$router.push({ name: 'Seller',
                params: { user: this.ruleForm2.user } });
            } else if (this.activeName === '4') {
              this.$router.push({ name: 'EduAdmin',
                params: { user: this.ruleForm2.user } });
            } else if (this.activeName === '3') {
              this.$router.push({ name: 'Cc',
                params: { user: this.ruleForm2.user } });
            } else {
              this.$router.push({ name: 'Superuser',
                params: { user: this.ruleForm2.user } });
            }
          });
        }
      });
    },
    /**
     * @function resetForm
     * @description 清空用户输入框的内容
     */
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>

<style scoped>
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
.rows {
  position: relative;
  top: 50%;
  width: 96%;
  transform: translateY(-50%);
}
.headpicture {
  width: 100%;
  height: 100%;
  position: fixed;
  z-index: -1;
}
h1, h3 {
  font-weight: normal;
  margin-left: 180px;
  margin-top: 150px;
  color: rgba(0, 110, 255, 0.973);
  font-family: "微软雅黑";
}
a {
  color: #42b983;
}
.home {
  background-color: rgba(0, 110, 255, 0.973);
  color: white;
}
.formu {
  width: 100%;
  background-color: white;
  border-width: 1px;
  border-color: rgba(128, 128, 128, 0.3);
  border-style: solid;
  padding-left: 20px;
  padding-right: 10px;
  padding-top: 20px;
  padding-bottom: 20px;
  border-radius: 5px;
}
.el-form-item__label {
  float: left;
  font-size: 14px;
  color: #606266;
  line-height: 40px;
  padding: 0 12px 0 0;
  box-sizing: border-box;
}
.tabs {
  position: relative;
  left: 55%;
  top: 150px;
  width: 390px;
}
.el-input__inner {
  margin-left: -30px;
  -webkit-appearance: none;
  background-color: #fff;
  background-image: none;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  box-sizing: border-box;
  color: #606266;
  display: inline-block;
  font-size: inherit;
  height: 40px;
  line-height: 40px;
  outline: 0;
  padding: 0 15px;
  transition: border-color .2s cubic-bezier(.645,.045,.355,1);
  width: 100%;
}
.el-form-item__label {
  margin-left: -50px;
  float: left;
  font-size: 14px;
  color: #606266;
  line-height: 40px;
  padding: 0 12px 0 0;
  box-sizing: border-box;
}
.el-form-item {
  margin-left: 0;
}
.item {
  padding-left: 30px;
}
.el-row {
  padding-top: 12px;
  padding-bottom: 30px;
}
.input {
  padding-top: 15px;
}
</style>
