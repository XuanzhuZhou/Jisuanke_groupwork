<template>
  <div class="course-info">
    <el-from label-position="left" inline>
      <el-form-item label="课程老师">
        <el-input placeholder="course.teacher"></el-input>
      </el-form-item>
      <el-form-item label="开始时间">
        <el-input placeholder="course.time"></el-input>
      </el-form-item>
      <el-form-item label="课程价格">
        <el-input placeholder="course.price" :disabled="true"></el-input>
      </el-form-item>
    </el-from>
    <el-table :data="section">
      <el-table-column prop="count"
                       label="课节">
      </el-table-column>
      <el-table-column prop="name"
                       label="课节名">
      </el-table-column>
      <el-table-column prop="data"
                       label="上课日期">
      </el-table-column>
      <el-table-column prop="start_time"
                       label="开始时间">
      </el-table-column>
      <el-table-column prop="end_time"
                       label="结束时间">
      </el-table-column>
      <el-table-column prop="location"
                       label="上课地点">
      </el-table-column>
    </el-table>
  </div>
</template>


<script>
import DIC from '@/dictionary.json';
import { getCookie } from '@/utils/utils';

export default {
  props: {
    courseId: {
      type: Number,
      require: true,
    },
  },
  data() {
    return {
      id: this.courseId,
      course: {},
      section: [],
    };
  },
  updated() {
    this.axios({
      method: 'post',
      url: 'course/edu_courses_info',
      data: {
        id: this.id,
      },
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
    }).then((response) => {
      if (response.data.error !== DIC.STATUS_CODE.Success) {
        this.$message('出了一些问题');
      } else {
        this.section = response.data.section_info.list;
      }
    });
  },
};
</script>

<style scoped>
.course-info {
}
</style>

