<template>
  <div v-if="currValue === '1'" class="di">
    <div class="lists">
      <span><strong>●&nbsp;&nbsp;&nbsp;<span id="styles">弈学园 ———
      </span>国内唯一连锁培训机构&nbsp;&nbsp;&nbsp;●</strong></span>
    </div>
    <div class="image">
      <img :src="img4" height="470px">
    </div>
    <div class="lists">
      <span><strong>●&nbsp;&nbsp;&nbsp;<span id="styles">弈学园
      </span>连锁化经营模式&nbsp;&nbsp;&nbsp;●</strong></span>
    </div>
    <div class="image">
      <img :src="img" height="500px">
    </div>
    <div class="lists">
      <span><strong>●&nbsp;&nbsp;&nbsp;<span id="styles">弈学园
      </span>专注少儿素质教育&nbsp;&nbsp;&nbsp;●</strong></span>
    </div>
    <div class="image">
      <img :src="img5" height="700px" width="1050px">
    </div>
    <div class="lists">
      <span><strong>●&nbsp;&nbsp;&nbsp;<span id="styles">弈学园
      </span>线上线下辅助教育&nbsp;&nbsp;&nbsp;●</strong></span>
    </div>
    <div class="image">
      <img :src="img3" height="430px">
    </div>
    <div class="lists">
      <span><strong>●&nbsp;&nbsp;&nbsp;<span id="styles">弈学园
      </span>校区分布与收入情况&nbsp;&nbsp;&nbsp;●</strong></span>
    </div>
    <div class="image botto">
      <img :src="img2" height="530px">
    </div>
  </div>
</template>

<script>
/**
 * 落地页关于我们模块，主要包含公司企业的简介部分
 * @module aboutUs
 */
export default {
  props: {
    initial: {
      default: '0',
    },
  },
  /**
   * @prop {String} currValue 子组件显示判断
   * @prop {String} imgUrl 页面图片
   * @prop {String} imgUrl2 页面图片
   * @prop {String} img 页面图片
   * @prop {String} img2 页面图片
   * @prop {String} img3 页面图片
   * @prop {String} img4 页面图片
   * @prop {String} img5 页面图片
   */
  data() {
    return {
      currValue: '0',
      imgUrl: '/static/img/total.png',
      imgUrl2: '/static/img/words.png',
      img: '/static/img/course1.png',
      img2: '/static/img/course2.png',
      img3: '/static/img/course3.png',
      img4: '/static/img/course4.png',
      img5: '/static/img/course5.png',
    };
  },
  watch: {
    initial(nv) {
      this.currValue = nv;
    },
  },
};
</script>

<style scoped>
.di {
  margin: 6.5% auto auto auto;
  max-width: 1170px;
}
.bac {
  background-color: #F3F3F3;
}
.time {
  font-size: 13px;
  color: #999;
}
.bottom {
  margin-top: 13px;
  line-height: 22px;
}
.button {
  padding: 0;
  float: right;
}
.image {
  margin: 0 auto;
  display: block;
}
.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both;
}
.cards {
  margin-top: 50px;
  padding-top: 2%;
}
.title {
  margin: 0 auto;
  height: 70px;
  background: #d4d4d4;
  border-left: 10px solid #998f03;
  padding-left: 40px;
  box-sizing: border-box;
  margin-top: 30px;
  margin-bottom: 30px;
}
.title p {
  color: #7b7b7b;
  font-size: 28px;
  font-weight: bold;
  line-height: 66px;
}
.title span {
  color: #998f03;
  font-size: 28px;
  font-weight: bold;
  line-height: 66px;
}
.bot {
  padding-left: 58px;
}
.image {
  text-align: center;
}
.botto {
  margin-bottom: 20px;
}
#word {
  margin-left: 15%;
  margin-bottom: 9px;
}
.lists {
  color: #8EC63D;
  text-align: center;
  font-size: 30px;
  margin: 20px;
  margin: 25px auto 30px auto;
}
#styles {
  color: rgb(24, 23, 23);
}
</style>
