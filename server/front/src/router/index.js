import Vue from 'vue';
import Router from 'vue-router';
import Heading from '@/components/Landing/heading';
import Login from '@/components/BackLogin/Login';
import Seller from '@/components/sellers/Seller';
import parent from '@/components/Parents/parent';
import Cc from '@/components/cc/Cc';
import EduAdmin from '@/components/EduAdmin/EduAdmin';
import Superuser from '@/components/superuser/Superuser';
import sellerpage from '@/components/phone/sellerpage';
import sellerlogin from '@/components/phone/sellerlogin';
import land from '@/components/PhoneLogin/land';
import adult from '@/components/PhoneParent/adult';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Heading',
      component: Heading,
      meta: {
        requireLoginCheck: false,
      },
    },
    {
      path: '/parent/:user',
      name: 'parent',
      component: parent,
      meta: {
        requireLoginCheck: true,
        // 设为 false 即可对该 url 不进行登录检查
      },
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login,
      meta: {
        requireLoginCheck: false,
      },
    },
    {
      path: '/sellerlogin',
      name: 'sellerlogin',
      component: sellerlogin,
      meta: {
        requireLoginCheck: false,
      },
    },
    {
      path: '/Seller/:user',
      name: 'Seller',
      component: Seller,
      meta: {
        requireLoginCheck: true,
      },
    },
    {
      path: '/Cc/:user',
      name: 'Cc',
      component: Cc,
      meta: {
        requireLoginCheck: true,
      },
    },
    {
      path: '/EduAdmin/:user',
      name: 'EduAdmin',
      component: EduAdmin,
      meta: {
        requireLoginCheck: true,
      },
    },
    {
      path: '/Superuser/:user',
      name: 'Superuser',
      component: Superuser,
      meta: {
        requireLoginCheck: true,
      },
    },
    {
      path: '/sellerpage/:user',
      name: 'sellerpage',
      component: sellerpage,
      meta: {
        requireLoginCheck: true,
      },
    },
    {
      path: '/land',
      name: 'land',
      component: land,
      meta: {
        requireLoginCheck: false,
      },
    },
    {
      path: '/adult',
      name: 'adult',
      component: adult,
      meta: {
        requireLoginCheck: false,
      },
    },
  ],
});
