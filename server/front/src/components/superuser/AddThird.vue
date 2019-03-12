<template>
<el-card>
  <div shadow="hover">
      <el-upload
        class="upload-form"
        ref="upload"
        drag
        multiple
        :action="submitFile"
        :limit="3"
        :before-upload="beforeUpload"
        :on-remove="removeFile"
        :on-exceed="handleExceed"
        :file-list="fileList"
        :auto-upload="false"
        accept=".xlsx,.xls,.csv">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <div class="el-upload__tip" slot="tip">
          只能上传xls/xlsx/csv文件，且不超过500kb
        </div>
      </el-upload>
      <div class="buttons">
        <el-button size="small"  type="primary" @click="submitFile">
          提交
        </el-button>
        <el-button size="small" type="info" @click="clear">
          清空
        </el-button>
      </div>
  </div>
</el-card>
</template>
<style scoped>
.upload-form {
  width: 300px;
  margin: 0 auto;
}
.buttons {
  display: flex;
  align-items: center;
  flex-flow: row nowrap;
  width: 100px;
  margin: 10px auto;
}
.bread {
  height: 50px;
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
import DIC from '@/dictionary.json';

export default {
  props: {
    initUrl: {
      type: String,
      require: true,
    },
  },
  data() {
    return {
      url: this.initUrl,
      fileList: [],
    };
  },
  methods: {
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 
          ${files.length + fileList.length} 个文件`,
      );
    },
    beforeUpload(file) {
      const fileData = new FormData();
      fileData.append('file', file);
      this.axios({
        method: 'post',
        url: this.url,
        data: fileData,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).then((response) => {
        if (response.data.msg === DIC.STATUS_CODE.Success) {
          this.$notify.success({
            title: '提示',
            message: `成功导入${file.name}`,
          });
          this.fileList.push(file);
        } else {
          this.$notify.error({
            title: '失败',
            message: `${file.name}无法导入，请检查格式`,
          });
        }
      });
      return false;
    },
    submitFile() {
      this.$refs.upload.submit();
    },
    clear() {
      this.$refs.upload.clearFiles();
      this.fileList = [];
    },
    removeFile(file) {
      const index = this.fileList.indexOf(file);
      if (index > -1) {
        this.fileList.splice(index, 1);
      }
    },
  },
};
</script>
