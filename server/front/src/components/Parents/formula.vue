<template>
  <div v-if="currValue === '1'" class="dv">
    <el-tag class="tag">预览</el-tag>
    <el-card class="box-card">
      <div class="row" id="pdfDom"
      style="padding-top: 30px;background-color:#fff;">
        此处显示具体合同内容：
      </div>
    </el-card>
    <el-button class="but" @click="getPdf('弈学园电子合同')">导出PDF</el-button>
  </div>
</template>

<script>
/**
 * 预留功能：导出电子合同和电子发票pdf
 * @module formula
 */
export default {
  props: {
    initial: {
      default: '1',
    },
  },
  data() {
    return {
      currValue: '1',
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
.box-card {
  margin: 0 auto;
  text-align: center;
  width: 50%;
  margin-top: 1%;
}
.but {
  margin-top: 1%;
  background-color: cornflowerblue;
  color: whitesmoke;
}
.dv {
  text-align: center;
}
.tag {
  margin-top: 1%;
  color: blueviolet;
  font-size: 20px;
}
</style>
