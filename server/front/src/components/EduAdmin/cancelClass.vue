<template>
  <div>
    <el-table :data="courses" stripe>
      <el-table-column prop="name"
                       label="课节名"
                       align="center">
      </el-table-column>
      <el-table-column prop="date" label="日期" align="center">
      </el-table-column>
      <el-table-column prop="start_time"
                       label="开始时间"
                       align="center">
      </el-table-column>
      <el-table-column prop="end_time"
                       label="结束时间"
                       align="center">
      </el-table-column>
      <el-table-column prop="location"
                       label="上课地点"
                       align="center">
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
            <el-button @click="cancel(scope.row)"
                       type="text"
                       size="small"
                       :disabled="scope.row.is_cancel">
              {{ scope.row.is_cancel ? '已销' : '销课' }}
            </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getCookie } from '@/utils/utils';

export default {
  data() {
    return {
      courses: [],
    };
  },
  methods: {
    cancel(key) {
      this.axios({
        method: 'post',
        url: 'api/eduadmin_ensure_cancell',
        data: {
          id: key.id,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.seccess) {
          this.$message('销课成功');
          this.updateData();
        } else {
          this.$message('销课失败');
        }
      });
    },
    updateData() {
      this.axios({
        method: 'post',
        url: 'api/eduadmin_cancell_courses',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.count !== 0) {
          this.courses = response.data.list;
        }
      });
    },
  },
  beforeCreate() {
    this.axios({
      method: 'post',
      url: 'api/eduadmin_cancell_courses',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
    }).then((response) => {
      if (response.data.count !== 0) {
        this.courses = response.data.list;
      }
    });
  },
};
</script>

