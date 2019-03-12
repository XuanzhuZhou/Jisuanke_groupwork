<template>
  <div>
    <el-card class="class-card">
      <el-row>
        <el-col :span="18">
        <el-form @submit.native.prevent
                label-position="right"
                label-width="80px">
          <el-form-item label="课程名称" class="input-area">
            <el-input placeholder="课程名称"
                      v-model="requestData.name">
            </el-input>
          </el-form-item>
          <el-form-item label="老师姓名" class="input-area">
            <el-input placeholder="老师姓名"
                      v-model="requestData.teacher_name">
            </el-input>
          </el-form-item>
          <el-form-item label="上课星期" class="input-area">
            <el-input placeholder="上课星期"
                      v-model="requestData.date">
            </el-input>
          </el-form-item>
          <el-form-item label="上课时间" class="input-area">
            <el-time-picker type="fixed-time"
                      value-format="HH:mm:SS"
                      v-model="requestData.time">
            </el-time-picker>
          </el-form-item>
          <el-form-item label="课程时长" class="input-area">
            <el-input placeholder="课程时长"
                      v-model="requestData.time_length">
            </el-input>
          </el-form-item>
          <el-form-item label="开始日期" class="input-area">
            <el-date-picker placeholder="开始日期"
                            value-format="yyyy-MM-dd"
                            v-model="requestData.start_date">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="课程价格" class="input-area">
            <el-input placeholder="课程价格"
                      v-model="requestData.price">
            </el-input>
          </el-form-item>
          <el-form-item label="总课节数" class="input-area">
            <el-input placeholder="总课节数"
                      v-model="requestData.total_sec">
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button @click="addClass">修改</el-button>
          </el-form-item>
        </el-form>
        </el-col>
      </el-row>
    </el-card>
    <add-third :initUrl="url.importFileUrl"></add-third>
  </div>
</template>


<style scoped>
.class-card {
  margin-bottom: 16px;
}
.input-area {
  max-width: 800px;
  width: 100%;
  margin-top: 20px;
}
.input-area .el-input {
  max-width: 800px;
  width: 100%;
}
</style>

<script>
import { getCookie } from '@/utils/utils';
import DIC from '@/dictionary.json';
import AddThird from '@/components/superuser/AddThird';

export default {
  components: {
    'add-third': AddThird,
  },
  data() {
    return {
      url: {
        importFileUrl: 'data/import_courses',
      },
      time: '',
      date: '',
      requestData: {
        teacher_name: '',
        name: '',
        time: '',
        date: '',
        time_length: '',
        total_sec: '',
        price: '',
        start_date: '',
      },
    };
  },
  methods: {
    addClass() {
      if (this.requestData.time === null) {
        this.requestData.time = '';
      }
      this.axios({
        url: 'course/add_new_course',
        method: 'post',
        data: this.requestData,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.$message('添加成功');
        } else {
          this.$message('添加失败');
        }
      });
    },
  },
};
</script>
