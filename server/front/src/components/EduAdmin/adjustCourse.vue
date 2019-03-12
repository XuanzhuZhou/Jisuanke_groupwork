<template>
<el-row>
  <el-col :span="17" :xs="24">
    <div>
      <el-form class="adjust-course-form"
              @submit.native.prevent
              label-position="right"
              label-width="80px">
        <el-form-item label="课程名称" class="input-area">
          <el-input :placeholder="course.name">
          </el-input>
        </el-form-item>
        <el-form-item label="上课日期" class="input-area">
          <el-date-picker value-format="yyyy-MM-dd"
                          placeholder="选择日期"
                          v-model="course.data">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="上课时间" class="input-area">
          <el-time-picker placeholder="选择时间"
                          value-format="HH:mm:SS"
                          v-model="course.time">
          </el-time-picker>
        </el-form-item>
        <el-form-item label="课程时长" class="input-area">
          <el-input :placeholder="course.time_length">
          </el-input>
        </el-form-item>
        <el-form-item label="课程教师" class="input-area">
          <el-input r="course.teacher">
          </el-input>
        </el-form-item>
        <el-form-item label="课程节次" class="input-area">
          <el-input :placeholder="course.total_sec">
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="submitAdd">修改</el-button>
        </el-form-item>
      </el-form>
    </div>
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
      course: this.item,
    };
  },
  methods: {
    submitAdd() {
      if (this.course.time === null) {
        this.course.time = '';
      }
      if (this.course.date === null) {
        this.course.date = '';
      }
      this.$emit('submitAdd', this.course);
    },
  },
  watch: {
    item(nv) {
      this.course = nv;
    },
  },
};
</script>

<style scoped>
.adjust-course-form {
  padding: 40px;
  padding-top: 20px;
  padding-bottom: 20px;
}
.input-area {
  max-width: 600px;
  margin-bottom: 30px;
}
.input-area .el-input {
  max-width: 600px;
  width: 100%;
}
</style>
