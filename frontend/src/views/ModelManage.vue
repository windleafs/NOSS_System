<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h4 class="card-title">模型管理</h4>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <label for="modelName" class="form-label">模型名称</label>
              <input type="text" class="form-control" id="modelName" v-model="modelName" placeholder="输入模型名称">
            </div>
            <div class="mb-3">
              <label for="modelFile" class="form-label">上传模型文件</label>
              <input type="file" class="form-control" id="modelFile" @change="uploadModel">
            </div>
            <div class="mb-3">
              <label for="modelType" class="form-label">设置模型用途</label>
              <select class="form-control" id="modelType" v-model="selectedModelType">
                <option value="image">图片隐写</option>
                <option value="video">视频隐写</option>
                <option value="iorv">图片视频通用</option>
              </select>
            </div>
            <div class="button-container">
              <button class="btn btn-primary" @click="saveModelSettings">确认上传</button>
            </div>
          </div>
        </div>
        <!-- New card for displaying models -->
        <div class="card mt-4">
          <div class="card-header">
            <h4 class="card-title">可用模型</h4>
          </div>
          <div class="card-body">
            <ul class="list-group">
              <li v-for="(model, index) in models" :key="model.id" class="list-group-item d-flex justify-content-between align-items-center">
                {{ model.name }} ({{ model.type }})
                <button class="btn btn-danger btn-sm" @click="deleteModel(index)">删除</button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

  
  
  
  
  
<script>
import baseURL from "@/config/config.js";
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  name: "ModelManage",
  data() {
    return {
      modelName: '',
      selectedModelType: 'image',
      modelFile: null,
      models: [],
      isLogin:false,
      username:'',
      userrole:'',
      usernoss:0,
      userid:0,
      toast:useToast(),
      isMember: false, 
      showModel: false,
      membershipExpiration:'',
    };
  },
  created() {
    this.fetchModels();  // 在组件创建时获取所有模型
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.isLogin = false;
      alert('您无权访问！');
      this.$router.push('/dashboard');
      return;
    }
    
    axios.get(baseURL+'/validate', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(response => {
      if (response.data && response.data.message === 'Token is valid!') {
        this.isLogin = true;
        this.userid = response.data.user_id;
        this.getUserInfo();
        
      } else {
        this.isLogin = false;
      }
    }).catch(error => {
      console.error('Authentication error:', error);
      this.isLogin = false;
    });
  },
  methods: {
    uploadModel(event) {
      const file = event.target.files[0];
      if (!file) return;
      const validExtensions = ['pth', 'pt'];
      const fileExtension = file.name.split('.').pop().toLowerCase();
      if (!validExtensions.includes(fileExtension)) {
        alert('文件类型不正确，请上传.pth或.pt后缀的文件');
        return;
      }
      this.modelFile = file;
    },
    saveModelSettings() {
      if (!this.modelFile || !this.modelName) {
        alert('请确保已填写模型名称并上传文件');
        return;
      }
      const formData = new FormData();
      formData.append('file', this.modelFile);
      formData.append('name', this.modelName);
      formData.append('type', this.selectedModelType);

      axios.post(`${baseURL}/upmodel`, formData)
        .then(response => {
          this.models.push({
            id: response.data.id,
            name: this.modelName,
            type: this.selectedModelType
          });
          useToast().success('模型已上传',{timeout:1000});
          this.modelName = '';  // 重置模型名称输入
        })
        .catch(error => {
          console.error('Error:', error);
          useToast().error('上传失败',{timeout:1000});
        });
    },
    deleteModel(index) {
      const modelId = this.models[index].id;
      axios.delete(`${baseURL}/deletemodel/${modelId}`)
        .then(() => {
          this.models.splice(index, 1);
          useToast().success('模型已删除',{timeout:1000});
        })
        .catch(error => {
          console.error('Delete Error:', error);
          useToast().error('删除失败',{timeout:1000});
        });
    },
    fetchModels() {
      axios.get(`${baseURL}/listmodels`)
        .then(response => {
          this.models = response.data;
        })
        .catch(error => {
          console.error('Error fetching models:', error);
          useToast().error('获取模型列表失败',{timeout:1000});
        });
    },
    getUserInfo(){
        axios.post(baseURL+'/getuinfo', { user_id: this.userid })
          .then(response => {
            if (response.data && response.data.user_info) {
              this.username= response.data.user_info.username;
              this.usernoss= response.data.user_info.noss_points;
              this.userrole= response.data.user_info.role;
              if(this.userrole!=='admin'){
                alert('您无权访问！');
                this.$router.push('/dashboard');
              }
            } else {
              alert('User not found');
            }
          })
          .catch(error => {
            console.error('Error fetching user info:', error);
            alert('Error fetching user info');
          });
      },
  } 
};
</script>



  
  
<style scoped>
.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 或根据需要调整间距 */
}
.list-group-item {
  display: flex;
  justify-content: space-between; /* Ensures content and button are spaced apart */
  align-items: center; /* Aligns items vertically at the center */
  padding: 0.75rem 1.25rem; /* Standard padding for list items */
  border-bottom: 1px solid #e0e0e0; /* Adds a subtle line between items for better visual separation */
}

.btn-danger {
  padding: 0.25rem 0.5rem; /* Smaller padding for a more compact button */
  font-size: 0.875rem; /* Smaller font size for a proportionate look to the list text */
}

.btn {
  white-space: nowrap; /* Prevents the button text from wrapping */
}

.card-body {
  overflow-x: hidden; /* Prevents horizontal scrolling caused by wide content */
  overflow-y: auto; /* Allows vertical scrolling if many items are present */
}

.card {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Light shadow for a subtle 3D effect */
  border: 1px solid #e0e0e0; /* Solid border to define the edges of the card */
}

.card-header {
  background-color: #f8f9fa; /* Light grey background for the header */
  border-bottom: 1px solid #e0e0e0; /* Light line to separate header from body */
}


.form-label {
  font-weight: bold; /* Bold labels for better readability */
}

.form-control {
  margin-bottom: 15px; /* Adds space between form elements */
  width: 100%; /* Ensures form controls take up the full width of their container */
  border-radius: 0.375rem; /* Rounded borders for text inputs and dropdowns */
  border: 1px solid #ced4da; /* Standard border for form controls */
}


.list-group {
  margin-bottom: 0; /* Removes bottom margin for lists */
}

.btn-danger {
  margin-left: 10px; /* Adds left margin to danger button for spacing */
}

.btn-primary, .btn-danger {
  border: none; /* Removes border from buttons for a cleaner look */
  color: white; /* Ensures text is white for readability */
  background-color: #007bff; /* Standard Bootstrap primary blue */
}


.btn-sm {
  padding: 0.25rem 0.5rem; /* Smaller padding for small buttons */
  font-size: 0.875rem; /* Smaller font size for small buttons */
  line-height: 1.5; /* Standard line height for alignment */
}

.input-group {
  margin-bottom: 15px; /* Adds space below input groups */
}

.input-group-text {
  background-color: #f8f9fa; /* Light grey background for input group addons */
  border-radius: 0.375rem; /* Rounded borders for aesthetic consistency */
}

.navbar-brand {
  font-weight: bolder; /* Bold font for brand in navbar for prominence */
}

@media (max-width: 768px) {
  .card {
    margin-top: 15px; /* Smaller top margin on smaller screens */
  }
}
</style>

  
  
  
  