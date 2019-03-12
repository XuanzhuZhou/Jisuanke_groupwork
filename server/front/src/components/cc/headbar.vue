<template>
<div class="icons">
  <el-button class="el-icon-edit" circle></el-button>
  <el-button class="el-icon-date" circle></el-button>
  <el-button class="el-icon-bell" circle></el-button>
  <el-dropdown @command="handleCommand">
    <span class="el-dropdown-link">
      {{this.$route.params.user}}
      <i class="el-icon-arrow-down el-icon--right"></i>
    </span>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item command='1'>
        <i class="el-icon-circle-close-outline"></i>
        退出登录
      </el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</div>
</template>
<style scoped>
.icons {
  margin-left: 75%;
  margin-top: 5px;
}
</style>
<script>
import DIC from '@/dictionary.json';
import { getCookie } from '@/utils/utils';

export default {
  data() {
    return {
      notifyNum: '1',
      picsrc: '/static/img/headpic.png',
    };
  },
  methods: {
    handleCommand(command) {
      if (command === '1') {
        this.axios({
          method: 'post',
          url: 'api/logout',
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).then((response) => {
          if (response.data.error === DIC.STATUS_CODE.Success) {
            this.$router.push({ name: 'Login' });
          }
        });
      }
    },
  },
};
</script>
