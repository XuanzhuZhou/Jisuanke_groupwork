<template>
  <div>
    <el-card shadow="hover" class="mycard">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="passform">
        <el-form-item label="旧密码" prop="oldpass">
          <el-input type="password"
            v-model="ruleForm.oldpass"
            auto-complete="off">
          </el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newpass">
          <el-input type="password"
            v-model="ruleForm.newpass"
            auto-complete="off">
          </el-input>
        </el-form-item>
        <el-form-item label="确认新密码" prop="checkpass">
          <el-input type="password"
            v-model="ruleForm.checkpass"
            auto-complete="off">
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">
              提交
           </el-button>
           <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.mycard {
  min-height: 800px;
}
.passform {
  width: 60%;
  margin: 0 15% 3% 15%;
}
.el-main {
  text-align: center;
  padding-top: 0;
}
.bread {
  margin: -20px -20px 10px -20px;
  height: 40px;
  border-left: 10px solid #48576a;
  background-color: white;
}
.el-breadcrumb {
  font-size: 16px;
  line-height: 3;
}
</style>

<script>
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';

export default {
  props: {
    initial: {
      default: '0',
    },
    name: {
      type: String,
      require: true,
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
    return {
      currValue: '0',
      username: '',
      ruleForm: {
        newpass: '',
        checkpass: '',
      },
      rules: {
        newpass: [{ validator: validatenewPass, trigger: 'blur' },
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, max: 18, message: '长度在 6 到 18 个字符', trigger: 'blur' }],
        checkpass: [{ validator: validatenewPass2, trigger: 'blur' },
          { required: true, message: '请再次输入新密码', trigger: 'blur' },
          { min: 6, max: 18, message: '长度在 6 到 18 个字符', trigger: 'blur' }],
      },
    };
  },
  watch: {
    name(nv) {
      this.username = nv;
    },
    initial(nv) {
      this.currValue = nv;
    },
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.axios({
            method: 'post',
            url: 'api/change_password',
            data: {
              old_psw: this.ruleForm.oldpass,
              new_psw: this.ruleForm.newpass,
              username: this.$route.params.user,
            },
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
          }).then((response) => {
            if (response.data.error === DIC.STATUS_CODE['Password Not Match']) {
              this.$refs[this.formName].resetFields();
              this.$message.error('旧密码错误!');
            } else {
              this.$message({
                message: '密码修改成功！',
                type: 'success',
              });
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

