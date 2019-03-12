<template>
  <el-container>
    <el-header class="search-bar">
      <el-row :gutter="10">
        <el-col :span="2" :xs="24" class="refresh-button">
          <el-button @click="resetData"
                      size="small"
                      icon="el-icon-refresh">
          </el-button>
        </el-col>
        <el-col :span="4" :xs="24">
          <el-input class="input-area"
                    size="small"
                    placeholder="请输入注册电话"
                    suffix-icon="el-icon-phone"
                    v-model="selectConditions.tel">
          </el-input>
        </el-col>
        <el-col :span="4" :xs="24">
          <el-input class="input-area"
                    size="small"
                    placeholder="请输入孩子姓名"
                    v-model="selectConditions.childname">
          </el-input>
        </el-col>
        <el-col :span="4" :xs="24">
          <el-input class="input-area"
                    size="small"
                    placeholder="请输入老师姓名"
                    v-model="selectConditions.teacher">
          </el-input>
        </el-col>
        <el-col :span="4" :xs="24">
          <el-select class="input-area"
                      size="small"
                      @change="changeDay"
                      placeholder="上课星期">
            <el-option label="星期一" :value="days.Monday"></el-option>
            <el-option label="星期二" :value="days.Tuesday"></el-option>
            <el-option label="星期三" :value="days.Wednesday"></el-option>
            <el-option label="星期四" :value="days.Thursday"></el-option>
            <el-option label="星期五" :value="days.Friday"></el-option>
            <el-option label="星期六" :value="days.Saturday"></el-option>
            <el-option label="星期日" :value="days.Sunday"></el-option>
          </el-select>
        </el-col>
        <el-col :span="4" :xs="24">
          <el-time-picker v-model="selectConditions.time"
                          size="small"
                          class="input-area"
                          value-format="HH:mm:SS"
                          :picker-options="{
                            selectableRange: '6:00:00 - 22:00:00'
                          }">
          </el-time-picker>
        </el-col>
        <el-col :span="2" :xs="24">
          <el-button size="small"
                      icon="el-icon-search"
                      @click="updateData"
                      class="search-button">
          </el-button>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-table :data="courses" :header-cell-style="setOutHeaderColor">
        <el-table-column type="expand" align="center">
          <template slot-scope="props">
            <el-table :data="props.row.sections"
                      class="section-content"
                      :header-cell-style="setHeaderColor">
              <el-table-column prop="name"
                               label="课节名"
                               align="center">
              </el-table-column>
              <el-table-column prop="date"
                               label="日期"
                               align="center">
              </el-table-column>
              <el-table-column prop="start_time"
                               label="开始时间"
                               align="center">
              </el-table-column>
              <el-table-column prop="end_time"
                               label="结束时间"
                               align="center">
              </el-table-column>
              <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                  <el-button @click="showDialogToChangeSection(scope.row)"
                             type="text"
                             size="small"
                             :disabled="is_cancel">
                    {{ is_cancel ? "已销课" : "修改此课程" }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-table-column>
        <el-table-column prop="name"
                         label="课程"
                         align="center">
        </el-table-column>
        <el-table-column prop="cur_sec"
                         label="已上课节"
                         align="center">
        </el-table-column>
        <el-table-column prop="teacher"
                         label="教师"
                         align="center">
        </el-table-column>
        <el-table-column prop="date"
                         label="星期"
                         align="center">
        </el-table-column>
        <el-table-column prop="time"
                         label="开始时间"
                         align="center">
        </el-table-column>
        <el-table-column prop="total_sec"
                         label="总课时"
                         align="center">
        </el-table-column>
        <el-table-column prop="num"
                         label="人数"
                         align="center">
        </el-table-column>
        <el-table-column label="添加学生"
                         align="center">
          <template slot-scope="scope">
            <el-button @click="addingStudent(scope.row)"
                       type="text"
                       size="small">
              安排学生
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="修改课程"
                         align="center">
          <template slot-scope="scope">
            <el-button @click="showDialogToChangeCourse(scope.row)"
                       type="text"
                       size="small">
              修改课程
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
    <el-dialog title="添加学生"
               :visible.sync="dialogFormVisible">
      <search-item :item="classId"
                   @submitSearch="addStudent">
      </search-item>
    </el-dialog>
    <el-dialog :visible.sync="dialogChangeSectionVisible">
      <adjust-section :item="sectionToChange"
                      @submitAdd="changeSection">
      </adjust-section>
    </el-dialog>
    <el-dialog :visible.sync="dialogChangeCourseVisible">
      <adjust-course :item="courseToChange"
                     @submitAdd="changeCourse">
      </adjust-course>
    </el-dialog>
  </el-container>
</template>

<style scoped>
.input-area {
  max-width: 10vw;
}
.section-content {
  padding-left: 0;
  padding-right: 0;
}
.section-content thead {
  background-color: #dddddd;
}
.search-bar {
  background-color: white;
}
.search-bar > div {
  margin-top: 4px;
  margin-bottom: 4px;
}
.el-table thead {
  color: #606266;
}
</style>

<script>
import DIC from '@/dictionary.json';
import { getCookie } from '@/utils/utils';
import searchItem from './searchItem';
import adjustCourse from './adjustCourse';
import adjustSection from './adjustSection';

export default {
  components: {
    'search-item': searchItem,
    'adjust-course': adjustCourse,
    'adjust-section': adjustSection,
  },
  data() {
    return {
      days: DIC.DATE_CODE,
      day: DIC.DATE_CODE.Monday,
      dialogFormVisible: false,
      dialogChangeSectionVisible: false,
      dialogChangeCourseVisible: false,
      selectConditions: {
        tel: '',
        childname: '',
        day: '',
        time: '',
        teacher: '',
      },
      courses: [{
        name: 'cb',
        date: '20180102',
        time: '12:12:12',
        time_length: '120',
        teacher: 'jdb',
        total_sec: '10086',
        sections: [{
          name: 'Math',
          date: '2018-02-30',
          start_time: '2019-03-03',
          end_time: '2019-03-05',
        }],
      }],
      classId: 0,
      sectionToChange: null,
      courseToChange: null,
      csrfHeaders: { 'X-CSRFToken': getCookie('csrftoken') },
    };
  },
  methods: {
    setHeaderColor() {
      return {
        'background-color': '#dddddd',
        color: '#606266',
      };
    },
    setOutHeaderColor() {
      return {
        'background-color': '#dddddd',
        color: '#606266',
      };
    },
    addingStudent(row) {
      this.classId = row.id;
      this.dialogFormVisible = true;
    },
    addStudent(key) {
      const requestData = key;
      requestData.id = this.classId;
      this.axios({
        method: 'post',
        url: 'api/eduadmin_arrange_course',
        data: requestData,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === 0) {
          this.$message('添加成功');
        } else {
          this.$message('添加失败');
        }
        this.updateData();
      }).catch(() => {
        this.$message('好像有些不对劲');
      });
    },
    changeDay(key) {
      this.selectConditions.day = key;
    },
    updateData() {
      if (this.selectConditions.time === null) {
        this.selectConditions.time = '';
      }
      if ((this.tel === '' && this.name === '') ||
          (this.tel !== '' && this.name !== '')) {
        this.axios({
          method: 'post',
          url: 'api/eduadmin_get_courses',
          data: this.selectConditions,
          headers: this.csrfHeaders,
        }).then((response) => {
          if (response.data.error === 0) {
            this.courses = response.data.list;
          } else {
            this.$message('什么都没有找到');
          }
        });
      } else {
        this.$message('请同时填入孩子姓名和电话号码');
      }
    },
    changeCourse() {
      const requestData = this.courseToChange;
      requestData.teacher_name = this.courseToChange.teacher;
      this.axios({
        method: 'post',
        url: 'course/change_course_info',
        data: requestData,
        headers: this.csrfHeaders,
      }).then((response) => {
        this.changeSuccess(response.data);
      });
    },
    showDialogToChangeSection(key) {
      this.sectionToChange = key;
      this.dialogChangeSectionVisible = true;
    },
    changeSuccess(data) {
      if (data.error === DIC.STATUS_CODE.Success) {
        this.$message('修改成功');
      } else {
        this.$message('修改失败');
      }
      this.resetData();
    },
    changeSection(newSection) {
      const reqeustData = newSection;
      reqeustData.section_id = newSection.id;
      reqeustData.section_name = newSection.name;
      this.axios({
        method: 'post',
        url: 'course/change_section_info',
        data: reqeustData,
        headers: this.csrfHeaders,
      }).then((response) => {
        this.changeSuccess(response.data);
      });
    },
    showDialogToChangeCourse(key) {
      this.dialogChangeCourseVisible = true;
      this.courseToChange = key;
    },
    resetData() {
      this.axios({
        method: 'post',
        url: 'api/eduadmin_get_courses',
        data: {
          tel: '',
          childname: '',
          day: '',
          time: '',
          teacher: '',
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.error === DIC.STATUS_CODE.Success) {
          this.courses = response.data.list;
        } else {
          this.$message('什么都没有找到');
        }
      });
    },
  },
  beforeCreate() {
    this.axios({
      method: 'post',
      url: 'api/eduadmin_get_courses',
      data: {
        tel: '',
        childname: '',
        day: '',
        time: '',
        teacher: '',
      },
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
    }).then((response) => {
      if (response.data.error === DIC.STATUS_CODE.Success) {
        this.courses = response.data.list;
      } else {
        this.$message('什么都没有找到');
      }
    });
  },
};
</script>
