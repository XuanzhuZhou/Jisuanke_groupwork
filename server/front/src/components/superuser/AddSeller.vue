<template>
  <div>
    <el-card shadow="hover" class="mycard">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="addsellerform">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="ruleForm.username" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="newpass">
          <el-input type="password" v-model="ruleForm.newpass" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="请再次输入密码" prop="checkpass">
          <el-input type="password" v-model="ruleForm.checkpass" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮件地址" prop="email">
          <el-input v-model="ruleForm.email" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="城市" prop="city">
          <el-input v-model="ruleForm.city" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input v-model="ruleForm.price" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="ruleForm.gender" placeholder="请选择性别">
            <el-option label="男" value="man"></el-option>
            <el-option label="女" value="woman"></el-option>
           </el-select>
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
.addsellerform {
  width: 60%;
  margin: 0 15% 0 15%;
}
.el-main {
  text-align: center;
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
      ruleForm: {
        newpass: '',
        checkpass: '',
        username: '',
        email: '',
        gender: '',
        city: '',
        price: '',
      },
      rules: {
        newpass: [
          { validator: validatenewPass, trigger: 'blur' },
          { min: 1, max: 16, message: '长度在 1 到 16 个字符', trigger: 'blur' },
        ],
        checkpass: [
          { validator: validatenewPass2, trigger: 'blur' },
          { min: 1, max: 16, message: '长度在 1 到 16 个字符', trigger: 'blur' },
        ],
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' },
        ],
        city: [
          { required: true, message: '请输入城市', trigger: 'blur' },
        ],
        price: [
          { required: true, message: '请输入价格', trigger: 'blur' },
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] },
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' },
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
            url: 'api/superuser_register',
            data: {
              username: this.ruleForm.username,
              password: this.ruleForm.newpass,
              email: this.ruleForm.email,
              gender: this.ruleForm.gender,
              city: this.ruleForm.city,
              price: this.ruleForm.price,
              user_type: '5',
            },
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
          }).then((response) => {
            if (response.data.error === DIC.STATUS_CODE.Success) {
              this.$message({
                message: '创建用户成功！',
                type: 'success',
              });
            } else {
              this.$message.error('用户名已存在！');
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
