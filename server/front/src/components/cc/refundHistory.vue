<template>
<div>
  <el-card shadow="hover" class="mycard">
    <el-table :data="refundHistory">
      <el-table-column type="expand">
        <template slot-scope="props">
        <el-form label-position="left" inline class="demo-table-expand">
          <el-form-item label="退款编号"  prop="id">
          <span>{{ props.row.id }}</span>
          </el-form-item>
          <el-form-item prop="date" label="申请退款日期">
          <span>{{ props.row.date }}</span>
          </el-form-item>
          <el-form-item prop="date1" label="处理退款日期">
          <span>{{ props.row.date1 }}</span>
          </el-form-item>
          <el-form-item prop="stu_name" label="孩子姓名">
          <span>{{ props.row.stu_name }}</span>
          </el-form-item>
          <el-form-item prop="phone" label="家长的手机号">
          <span>{{ props.row.phone }}</span>
          </el-form-item>
          <el-form-item prop="course_id" label="课程编号">
          <span>{{ props.row.course_id }}</span>
          </el-form-item>
          <el-form-item prop="coursename" label="课程名称">
          <span>{{ props.row.coursename }}</span>
          </el-form-item>
          <el-form-item prop="cncl_num" label="已销课程数目">
          <span>{{ props.row.cncl_num }}</span>
          </el-form-item>
          <el-form-item prop="total_sec" label="总课时">
          <span>{{ props.row.total_sec }}</span>
          </el-form-item>
          <el-form-item prop="payment" label="课程价格">
          <span>{{ props.row.payment }}</span>
          </el-form-item>
          <el-form-item prop="refund" label="退款金额">
          <span>{{ props.row.refund }}</span>
          </el-form-item>
        </el-form>
        </template>
        </el-table-column>
        <el-table-column label="退款编号" prop="id"></el-table-column>
        <el-table-column prop="stu_name" label="孩子姓名"></el-table-column>
        <el-table-column prop="phone" label="家长的手机号"></el-table-column>
        <el-table-column
            prop="tag"
            label="标签"
            :filters="[{ text: '已经退费', value: '已经退费' },
            { text: '尚未退费', value: '尚未退费' }]"
            :filter-method="filterTag"
            filter-placement="bottom-end">
            <template slot-scope="scope">
                <el-tag
                :type="scope.row.tag === '已经退费' ? 'primary' : 'success'"
                disable-transitions>{{scope.row.tag}}</el-tag>
            </template>
      </el-table-column>
    </el-table>
  </el-card>
</div>
</template>

<style scoped>
.mycard {
  min-height: 800px;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
.demo-table-expand {
  font-size: 0;
}
.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}
.el-form-item__content {
  margin-bottom: 2%
}
.el-main {
  padding-top: 0;
}
.bread {
  margin: -20px -20px 10px -20px;
  height: 40px;
  border-left: 10px solid #48576a;
  background-color: white;
}
.el-breadcrumb {
  font-size: 16px;
  line-height: 3;
}
</style>

<script>
import { getCookie } from '@/utils/utils';

export default {
  props: {
    initial: {
      default: '0',
    },
    name: {
      type: String,
      require: true,
    },
  },
  data() {
    return {
      currValue: '0',
      username: '',
      refundHistory: [],
    };
  },
  watch: {
    name(nv) {
      this.username = nv;
    },
    initial(nv) {
      this.currValue = nv;
      if (nv === '1') {
        this.refresh();
      }
    },
  },
  methods: {
    filterTag(value, row) {
      return row.tag === value;
    },
    refresh() {
      this.axios({
        method: 'post',
        url: 'api/cc_check_refund',
        data: {
          username: this.$route.params.user,
          refund: true,
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.count === 0) {
          this.refundHistory = [];
          this.$message('暂无数据!');
        } else {
          this.refundHistory = [];
          for (let i = 0; i < response.data.list.length; i += 1) {
            const temp = {};
            temp.cncl_num = response.data.list[i].cncl_num;
            temp.course_id = response.data.list[i].course_id;
            temp.coursename = response.data.list[i].coursename;
            temp.date = response.data.list[i].date;
            temp.date1 = response.data.list[i].date1;
            temp.id = response.data.list[i].id;
            temp.payment = response.data.list[i].payment;
            temp.phone = response.data.list[i].phone;
            temp.refund = response.data.list[i].refund;
            temp.stu_name = response.data.list[i].stu_name;
            temp.total_sec = response.data.list[i].total_sec;
            if (response.data.list[i].is_paid === true) {
              temp.tag = '已经退费';
            } else {
              temp.tag = '尚未退费';
            }
            this.refundHistory.push(temp);
          }
          this.$message({
            message: '数据已更新！',
            type: 'success',
          });
        }
      });
    },
  },
};
</script>

