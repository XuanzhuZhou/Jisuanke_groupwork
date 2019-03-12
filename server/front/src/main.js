// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import { getCookie } from '@/utils/utils';
import echarts from 'echarts';
import Mint from 'mint-ui';
import toPdf from '@/utils/toPdf';
import axios from 'axios';
import VueAxios from 'vue-axios';
import 'element-ui/lib/theme-chalk/index.css';
import ElementUI from 'element-ui';
import 'mint-ui/lib/style.css';
import Vue from 'vue';
import App from './App';
import router from './router';
import DIC from './dictionary.json';

Vue.prototype.$echarts = echarts;

Vue.use(ElementUI);
Vue.use(VueAxios, axios);
Vue.use(toPdf);
Vue.use(Mint);

Vue.config.productionTip = false;
router.beforeEach((to, from, next) => {
  axios({
    method: 'post',
    url: 'api/check_login',
    headers: { 'X-CSRFToken': getCookie('csrftoken') },
  }).then((response) => {
    if (response.data.error === 1 && to.name !== 'Login'
    && to.meta.requireLoginCheck) {
      next({ path: '/Login' });
    } else if (response.data.user_type === DIC.USER_TYPE.customer) {
      if (to.name === 'Login' || to.name === 'parent' || to.name === 'Heading'
      || to.name === 'land' || to.name === 'adult') {
        next();
      } else {
        next(false);
      }
    } else if (response.data.user_type === DIC.USER_TYPE.superuser) {
      if (to.name === 'Login' || to.name === 'Superuser'
      || to.name === 'Heading' || to.name === 'land') {
        next();
      } else {
        next(false);
      }
    } else if (response.data.user_type === DIC.USER_TYPE.consultant) {
      if (to.name === 'Login' || to.name === 'Cc'
      || to.name === 'Heading' || to.name === 'land') {
        next();
      } else {
        next(false);
      }
    } else if (response.data.user_type === DIC.USER_TYPE.eduadmin) {
      if (to.name === 'Login' || to.name === 'EduAdmin'
      || to.name === 'Heading' || to.name === 'land') {
        next();
      } else {
        next(false);
      }
    } else if (response.data.user_type === DIC.USER_TYPE.seller) {
      if (to.name === 'Login' || to.name === 'Seller'
      || to.name === 'Heading' || to.name === 'land'
      || to.name === 'sellerpage' || to.name === 'sellerlogin') {
        next();
      } else {
        next(false);
      }
    } else {
      next();
    }
  });
});


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
