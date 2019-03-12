<template>
  <div class="bac" v-if="currValue === '0'">
    <el-carousel :interval="4000" indicator-position="outside" height="500px" class="cards">
      <el-carousel-item v-for="(item, i) in items" :key="i">
        <img :src="item.imge" height="500px" width="1200px">
      </el-carousel-item>
    </el-carousel>
    <div class="lists">
      <span><strong>●&nbsp;&nbsp;&nbsp;<span id="styles">弈学园
      </span>风采&nbsp;&nbsp;&nbsp;●</strong></span>
    </div>
    <div class="bot">
      <el-row>
        <el-col :span="5" v-for="(item, index) in imgUrl" :key="index"
        :offset="index > 0 && index % 4 !== 0 ? 1 : 0">
          <div v-if="index > 3">
            <br>
          </div>
          <el-card :body-style="{ padding: '0px' }">
            <img :src="item.im" class="image">
            <div style="padding: 14px;">
              <span>{{ item.letter }}</span>
              <div class="bottom clearfix">
                <el-button type="text" class="button">弈学园</el-button>
              </div>
            </div>
          </el-card>
          <br>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
/**
 * 落地页主页面显示，包含走马灯和弈学园风采简介
 * @module page
 */
export default {
  props: {
    initial: {
      default: '0',
    },
  },
  /**
   * @prop {Array} items 存放页面显示的图片
   * @prop {Array} imgUrl 存放弈学园风采展示的卡片图片和文字
   * @prop {String} currValue 当前要显示的页面元素和组件
   */
  data() {
    return {
      items: [
        { imge: '/static/img/card1.jpg' },
        { imge: '/static/img/picture.png' },
        { imge: '/static/img/card3.png' },
      ],
      imgUrl: [{
        im: '/static/img/bd1.png',
        letter: '围棋特色',
      },
      {
        im: '/static/img/bd2.png',
        letter: '线上课程',
      },
      {
        im: '/static/img/bd4.png',
        letter: '师资保障',
      },
      {
        im: '/static/img/bd3.png',
        letter: '校区分布',
      },
      {
        im: '/static/img/bd5.png',
        letter: '家长分享',
      },
      {
        im: '/static/img/bd6.png',
        letter: '所获荣誉',
      },
      {
        im: '/static/img/bd7.png',
        letter: '媒体报道',
      },
      {
        im: '/static/img/bd8.png',
        letter: '联系我们',
      }],
      currValue: '0',
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
  width: 100%;
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
  margin: 50px auto auto auto;
  padding-top: 2%;
  max-width: 1170px;
}
.title {
  max-width: 1170px;
  margin: 0 auto;
  height: 70px;
  background: #d4d4d4;
  border-left: 10px solid rgb(57, 57, 58);
  padding-left: 40px;
  box-sizing: border-box;
  margin-bottom: 30px;
}
.title p {
  color: #7b7b7b;
  font-size: 28px;
  font-weight: bold;
  line-height: 66px;
}
.title span {
  color: rgb(8, 17, 48);
  font-size: 28px;
  font-weight: bold;
  line-height: 66px;
}
.bot {
  padding-left: 52px;
  max-width: 1220px;
  margin: 0 auto;
}
.lists {
  color: #8EC63D;
  text-align: center;
  font-size: 30px;
  margin: 20px auto 35px auto;
}
#styles {
  color: rgb(24, 23, 23);
}
</style>
