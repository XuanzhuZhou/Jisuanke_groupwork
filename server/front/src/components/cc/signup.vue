<template>
  <div>
    <el-card shadow="hover" class="mycard">
    <el-form :model="form" status-icon :rules="rules2" ref="form"
      label-width="100px"
      style="width: 90%; margin-top: 15px;">
    <el-form-item label="家长手机号" class="signform" prop="tel">
      <el-input v-model="form.tel" auto-complete="off"></el-input>
    </el-form-item>
    <el-form-item label="孩子姓名" class="signform" prop="child_name">
      <el-input v-model="form.child_name"></el-input>
    </el-form-item>
    <el-form-item label="家长姓名" class="signform" prop="parent_name">
      <el-input v-model="form.parent_name"></el-input>
    </el-form-item>
    <el-form-item label="classin账号ID" class="signform" prop="classin_id">
      <el-input v-model="form.classin_id"></el-input>
    </el-form-item>
    <el-form-item label="classin账号名称" class="signform" prop="classin_name">
      <el-input v-model="form.classin_name"></el-input>
    </el-form-item>
    <el-form-item label="孩子生日" class="signform" prop="birthday">
      <el-date-picker type="date" placeholder="选择日期" v-model="form.birthday"
      value-format="yyyy-MM-dd"></el-date-picker>
    </el-form-item>
    <el-form-item label="推荐客户" class="signform" prop="old_user">
      <el-input v-model="form.old_user"></el-input>
    </el-form-item>
     <el-form-item label="课程价格" class="signform" prop="price">
      <el-input v-model="form.price"></el-input>
    </el-form-item>
    <el-form-item label="时间选择：Ⅰ" class="signform">
      <el-col :span="9" prop="day1">
        <el-select v-model="form.day1" placeholder="上课星期">
          <el-option label="星期一" value="星期一"></el-option>
          <el-option label="星期二" value="星期二"></el-option>
          <el-option label="星期三" value="星期三"></el-option>
          <el-option label="星期四" value="星期四"></el-option>
          <el-option label="星期五" value="星期五"></el-option>
          <el-option label="星期六" value="星期六"></el-option>
          <el-option label="星期日" value="星期日"></el-option>
        </el-select>
      </el-col>
      <el-col :span="9" prop="time1">
        <el-time-picker type="fixed-time" placeholder="上课时间"
          v-model="form.time1">
        </el-time-picker>
      </el-col>
    </el-form-item>
    <el-form-item label="时间选择：Ⅱ" class="signform">
      <el-col :span="9" prop="day2">
        <el-select v-model="form.day2" placeholder="上课星期">
          <el-option label="星期一" value="星期一"></el-option>
          <el-option label="星期二" value="星期二"></el-option>
          <el-option label="星期三" value="星期三"></el-option>
          <el-option label="星期四" value="星期四"></el-option>
          <el-option label="星期五" value="星期五"></el-option>
          <el-option label="星期六" value="星期六"></el-option>
          <el-option label="星期日" value="星期日"></el-option>
        </el-select>
      </el-col>
      <el-col :span="9" prop="time2">
        <el-time-picker type="fixed-time" placeholder="上课时间"
          v-model="form.time2">
        </el-time-picker>
      </el-col>
    </el-form-item>
    <el-form-item label="时间选择：Ⅲ" class="signform">
      <el-col :span="9" prop="day3">
        <el-select v-model="form.day3" placeholder="上课星期">
          <el-option label="星期一" value="星期一"></el-option>
          <el-option label="星期二" value="星期二"></el-option>
          <el-option label="星期三" value="星期三"></el-option>
          <el-option label="星期四" value="星期四"></el-option>
          <el-option label="星期五" value="星期五"></el-option>
          <el-option label="星期六" value="星期六"></el-option>
          <el-option label="星期日" value="星期日"></el-option>
        </el-select>
      </el-col>
      <el-col :span="9" prop="time3">
        <el-time-picker type="fixed-time" placeholder="上课时间"
            v-model="form.time3">
        </el-time-picker>
      </el-col>
    </el-form-item>
    <el-form-item label="课程要求" class="signform" prop="demand">
      <el-input type="textarea" v-model="form.demand"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="signUp('form')">立即创建</el-button>
      <el-button @click="resetForm('form')">重置</el-button>
    </el-form-item>
  </el-form>
  </el-card>
</div>
</template>

<style scoped>
.mycard {
  min-height: 800px;
}
.signform {
  width: 70%;
  margin: 0 18% 3% 18%;
}
.el-input__inner {
  margin-left: 0;
  padding-top: 0;
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
  props: {
    initial: {
      default: '0',
    },
  },
  data() {
    const validateTel = (rule2, value, callback) => {
      if (value === '') {
        callback(new Error('请输入家长手机号'));
      } else {
        callback();
      }
    };
    const validateChildName = (rule2, value, callback) => {
      if (value === '') {
        callback(new Error('请输入孩子姓名'));
      } else {
        callback();
      }
    };
    const validateParentName = (rule2, value, callback) => {
      if (value === '') {
        callback(new Error('请输入家长姓名'));
      } else {
        callback();
      }
    };
    const validateBirthday = (rule2, value, callback) => {
      if (value === '') {
        callback(new Error('请输入孩子生日'));
      } else {
        callback();
      }
    };
    const validateDemand = (rule2, value, callback) => {
      if (value === '') {
        callback(new Error('请输入课程要求'));
      } else {
        callback();
      }
    };
    return {
      currValue: '0',
      form: {
        tel: '',
        child_name: '',
        parent_name: '',
        classin_id: '',
        classin_name: '',
        birthday: '',
        old_user: '',
        day1: '',
        time1: '',
        day2: '',
        time2: '',
        day3: '',
        time3: '',
        demand: '',
        price: '',
      },
      rules2: {
        tel: [{ validator: validateTel, trigger: 'blur' },
          { required: true, message: '请填写家长信息！', trigger: 'blur' },
          { min: 11, max: 11, message: '长度为 11 个字符', trigger: 'blur' }],
        child_name: [{ validator: validateChildName, trigger: 'blur' },
          { required: true, message: '请填写孩子姓名！', trigger: 'blur' },
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }],
        parent_name: [{ validator: validateParentName, trigger: 'blur' },
          { required: true, message: '请填写家长姓名！', trigger: 'blur' }],
        birthday: [{ validator: validateBirthday, trigger: 'blur' },
          { required: true, message: '请填写孩子生日！', trigger: 'blur' }],
        demand: [{ validator: validateDemand, trigger: 'blur' },
          { required: true, message: '请填写课程要求！', trigger: 'blur' }],
      },
    };
  },
  watch: {
    initial(nv) {
      this.currValue = nv;
    },
  },
  methods: {
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    signUp(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.axios({
            method: 'post',
            url: 'api/cc_signup_info',
            data: {
              tel: this.form.tel,
              child_name: this.form.child_name,
              parent_name: this.form.parent_name,
              classin_id: this.form.classin_id,
              classin_name: this.form.classin_name,
              birthday: this.form.birthday,
              old_user: this.form.old_user,
              day1: this.form.day1,
              time1: this.form.time1,
              day2: this.form.day2,
              time2: this.form.time2,
              day3: this.form.day3,
              time3: this.form.time3,
              demand: this.form.demand,
              money: parseFloat(this.form.price),
            },
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
          }).then((response) => {
            if (response.data.error === DIC.STATUS_CODE.Success) {
              this.$message({
                message: '报名成功！',
                type: 'success',
              });
            }
            if (response.data.error === DIC.STATUS_CODE['User Not Found']) {
              this.$message({
                message: '该用户不存在！请检查信息是否正确！',
                type: 'warning',
              });
            }
            if (response.data.error === DIC.STATUS_CODE['Child Not Found']) {
              this.$message({
                message: '信息不匹配!请检查孩子姓名！',
                type: 'warning',
              });
            }
            if (response.data.error === DIC.STATUS_CODE['Old Not Found']) {
              this.$message({
                message: '老客户信息不匹配！请检查信息是否正确！',
                type: 'warning',
              });
            }
            if (response.data.error === DIC.STATUS_CODE['Course Not Paid']) {
              this.$message({
                message: '存在待支付的课程,请支付后再报名',
                type: 'warning',
              });
            }
          });
        }
        return false;
      });
    },
  },
};
</script>

