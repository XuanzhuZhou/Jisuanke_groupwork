<template>
<el-row :gutter="10" class="erow">
  <el-col :xs="8" :sm="80" :md="80" :lg="52" :xl="85" :span="8" :offset="8">
    <div class="op">
    <el-form v-if="currValue === '6'" :model="ruleForm" status-icon
            :rules="rules" ref="ruleForm" class="demos"><br>
      <el-form-item label="旧密码" prop="oldpass">
        <el-input type="password" v-model="ruleForm.oldpass"
        auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="newpass">
        <el-input type="password" v-model="ruleForm.newpass"
        auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认新密码" prop="checkpass">
        <el-input type="password" v-model="ruleForm.checkpass"
        auto-complete="off"></el-input>
      </el-form-item>
      <br>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">
          提交</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
      <br>
    </el-form>
    </div>
  </el-col>
</el-row>
</template>

<script>
/**
 * 家长更改密码模块
 * @module changePass
 */
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';

export default {
  props: {
    initial: {
      default: '0',
    },
    username: {
      default: '',
    },
  },
  data() {
    const validatenewPass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入新密码'));
      } else {
        callback();
      }
    };
    const validatenewPass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入新密码'));
      } else if (value !== this.ruleForm.newpass) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    /**
     * @prop {String} currValue 更改页面状态
     * @prop {Object} ruleForm 存入更改前后的密码
     * @prop {Object} rules 密码输入检查规则
     */
    return {
      currValue: '0',
      ruleForm: {
        oldpass: '',
        newpass: '',
        checkpass: '',
      },
      rules: {
        newpass: [{ validator: validatenewPass, trigger: 'blur' }],
        checkpass: [{ validator: validatenewPass2, trigger: 'blur' }],
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
     * @description 向后端发送更改密码请求并获取是否成功更改密码
     */
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.axios({
            method: 'post',
            url: 'api/change_password',
            data: {
              username: this.username,
              old_psw: this.ruleForm.oldpass,
              new_psw: this.ruleForm.newpass,
            },
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
          }).then((response) => {
            if (response.data.error === DIC.STATUS_CODE.Success) {
              this.$alert('密码修改成功！', '恭喜', {
                confirmButtonText: '确定',
                callback: () => {
                  this.$message({
                    type: 'info',
                    message: '快去用新密码登录吧！',
                  });
                },
              });
              this.resetForm(this.ruleForm);
            } else {
              this.$alert('密码修改失败！', '警告', {
                confirmButtonText: '确定',
                callback: () => {
                  this.$message({
                    type: 'info',
                    message: '注意密码大小写哦！',
                  });
                },
              });
              this.resetForm(this.ruleForm);
            }
          });
        }
      });
    },
    /**
     * @function resetForm
     * @description 清空输入框中内容
     */
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>

<style scoped>
.demos {
  margin: 0 auto;
}
.erow {
  margin-top: 40px;
}
.op {
  background-color: rgba(145, 145, 145, 0.153);
}
.el-form-item {
  width: 80%;
  padding-left: 10%;
}
</style>
