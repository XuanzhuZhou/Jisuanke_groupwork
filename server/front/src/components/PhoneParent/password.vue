<template>
  <div v-if="currValue === '4'">
    <mt-field label="旧密码" placeholder="请输入旧密码" type="password"
    v-model="ruleForm.oldpass"></mt-field>
    <mt-field label="新密码" placeholder="请输入新密码" type="password"
    v-model="ruleForm.newpass"></mt-field>
    <mt-field label="确认新密码" placeholder="请再次输入新密码" type="password"
    v-model="ruleForm.checkpass"></mt-field>
    <mt-button class="btn" @click.native="pass()">提交</mt-button>
  </div>
</template>

<script>
/**
 * 家长修改密码功能
 * @module password
 */
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';

export default {
  props: {
    initial: {
      default: '0',
    },
  },
  /**
   * @prop {String} currValue 判断需要切换的页面
   * @prop {Object} ruleForm 存入用户修改的解密码和新密码
   */
  data() {
    return {
      currValue: '0',
      ruleForm: {
        oldpass: '',
        newpass: '',
        checkpass: '',
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
     * @function pass
     * @description 用户通过手机端更改密码
     */
    pass() {
      if (this.ruleForm.newpass !== this.ruleForm.checkpass) {
        this.$toast({
          message: '两次密码不一致',
          iconClass: 'mint-toast-icon mintui mintui-field-error',
        });
        return;
      } else if (this.ruleForm.oldpass === '' || this.ruleForm.newpass === ''
        || this.ruleForm.oldpass === '') {
        this.$toast({
          message: '用户名密码不能为空',
          iconClass: 'mint-toast-icon mintui mintui-field-error',
        });
        return;
      }
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
        }
      });
    },
  },
};
</script>

<style scoped>
.btn {
  width: 100%;
  background-color: rgba(97, 96, 96, 0.644);
  color: white;
}
</style>
