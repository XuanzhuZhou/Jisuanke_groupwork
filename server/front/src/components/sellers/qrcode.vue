<template>
<div>
    <img :src="picture">
</div>
</template>
<style scoped>
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

export default {
  props: {
    initial: {
      default: '0',
    },
  },
  data() {
    return {
      currValue: '0',
      name: this.$route.params.user,
      picture: '',
    };
  },
  watch: {
    initial(nv) {
      this.currValue = nv;
      if (nv === '1') {
        this.getQRcode();
      }
    },
  },
  created() {
    this.getQRcode();
  },
  methods: {
    getQRcode() {
      this.axios({
        method: 'post',
        url: 'user/qrcode',
        data: {
          name: this.$route.params.user,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        this.picture = response.data.path;
      });
    },

  },
};
</script>
