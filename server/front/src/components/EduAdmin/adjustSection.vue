<template>
<el-row>
  <el-col :span="17" :xs="24">
    <el-form class="adjust-section-form"
              size="small"
              @submit.native.prevent
              label-position="left"
              label-width="50px"
              max-height="100vh">
      <el-form-item label="课程" class="input-area">
        <el-input :placeholder="section.name"
                  v-bind="section.name">
        </el-input>
      </el-form-item>
      <el-form-item label="日期" class="input-area">
        <el-date-picker value-format="yyyy-MM-dd"
                        placeholder="选择日期"
                        v-model="section.date">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="时间" class="input-area">
        <el-row>
          <el-col :span="10">
            <el-form-item>
              <el-time-picker value-format="HH:mm:SS"
                              placeholder="开始时间"
                              v-model="section.start_time">
              </el-time-picker>
            </el-form-item>
          </el-col>
          <el-col class="line" :span="2">-</el-col>
          <el-col :span="10">
            <el-form-item>
              <el-time-picker value-format="HH:mm:SS"
                              placeholder="结束时间"
                              v-model="section.end_time">
              </el-time-picker>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form-item>
      <el-form-item>
        <el-button @click="submitAdd" size="medium">修改</el-button>
      </el-form-item>
    </el-form>
  </el-col>
</el-row>
</template>

<script>
export default {
  props: {
    item: {
      type: Object,
      require: true,
    },
  },
  data() {
    return {
      section: this.item,
    };
  },
  methods: {
    submitAdd() {
      if (this.section.start_time === null) {
        this.section.start_time = '';
      }
      if (this.section.end_time === null) {
        this.section.end_time = '';
      }
      if (this.section.date === null) {
        this.section.date = '';
      }
      this.$emit('submitAdd', this.section);
    },
  },
  watch: {
    item(nv) {
      if (nv) {
        this.section = nv;
      }
    },
  },
};
</script>

<style scoped>
.adjust-section-form {
  padding: 40px;
  padding-top: 20px;
}
.input-area {
  max-width: 600px;
  margin-bottom: 30px;
}
.input-area .el-input {
  max-width: 600px;
  width: 100%;
}
.line {
  text-align: center;
}
</style>
