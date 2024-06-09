<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <h6>发布任务</h6>
          </div>
          <div class="card-body">
            <form @submit.prevent="addTask">
              <div class="mb-3">
                <label for="file" class="form-label">上传文件:</label>
                <input type="file" class="form-control" ref="fileInput" id="file" @change="handleFileUpload" multiple required>
              </div>
              <div class="mb-3">
                <label for="stegaContent" class="form-label">隐写内容</label>
                <textarea type="text" class="form-control" id="stegaContent" v-model="newTask.content" placeholder="输入隐写内容" rows="8"></textarea>
              </div>
              <div class="mb-3">
                <label for="taskType" class="form-label">任务类型:</label>
                <select class="form-control" id="taskType" v-model="taskType">
                  <option value="encrypt">隐写任务</option>
                  <option value="decode">解码任务</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="steganographyType" class="form-label">隐写类型:</label>
                <select class="form-control" id="steganographyType" v-model="newTask.type" @change="handleChangeType">
                  <option value="text">文本隐写</option>
                  <option value="image">图片隐写</option>
                  <option value="audio">音频隐写</option>
                  <option value="video">视频隐写</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="modelSelection" class="form-label">模型选择:</label>
                <select class="form-control" id="modelSelection" v-model="newTask.model">
                  <option v-for="model in models" :key="model" :value="model">{{ model }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="cost" class="form-label">费用 (NOSS点):</label>
                <input type="number" class="form-control" id="cost" v-model="newTask.cost" readonly>
              </div>
              <div class="button-container">
                <button type="submit" class="btn btn-primary">提交任务</button>
              </div>
            </form>
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <h6>任务列表</h6>
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <table class="table align-items-center mb-0 text-center">
              <thead>
                <tr>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">任务ID</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">任务名</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">任务类型</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">任务状态</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(task, index) in tasks" :key="task.id">
                  <td>{{ task.id }}</td>
                  <td>{{ task.taskname }}</td>
                  <td>{{ task.type }}</td>
                  <td v-if="task.status === '可下载'">
                    <a :href="task.downloadUrl" target="_blank">{{ task.status }}</a>
                  </td>
                  <td v-else>
                    {{ task.status }}
                  </td>
                </tr>
              </tbody>
            </table>
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
  name: "BatchStega",
  data() {
    return {
      tasks: [],
      taskType: 'encrypt',
      taskIdCounter: 1, 
      newTask: {
        files: [], 
        type: "text",
        cost: 0,
        model:'',
        content:'',
      },
      costRates: {
        text: 5,
        image: 50,
        audio: 10,
        video: 100
      },
      isLogin:false,
      userid:0,
      username:'',
      userrole:'',
      isMember:false,
      usernoss:0,
      models: [], 
    };
  },
  created(){
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.isLogin = false;
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
    handleFileUpload(event) {
      this.newTask.files = Array.from(event.target.files); // 保存文件数组
      this.updateCost(); // 文件上传后立即更新费用
    },
    updateCost(){
      var discount = 1;
      if(this.isMember===true){
        discount = 0.8;
      }
      const baseCost = this.costRates[this.newTask.type]*discount;
      const fileCount = this.newTask.files.length;
      this.newTask.cost = baseCost * fileCount; // 每个文件的费用乘以文件数量
    },
    handleChangeType() {
      this.fetchmodel();
      this.updateCost();
    },
    getUserInfo(){
      axios.post(baseURL+'/getuinfo', { user_id: this.userid })
        .then(response => {
          if (response.data && response.data.user_info) {
            this.username= response.data.user_info.username;
            this.usernoss= response.data.user_info.noss_points;
            this.userrole= response.data.user_info.role;
            if(this.userrole==='admin'){
              this.isMember=true;
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
    handlePayCost(newPoints){
      axios.post(baseURL + '/topup', {
        user_id: this.userid, 
        points: newPoints
      })
      .then(response => {
        if (response.data && response.data.success) {
          this.usernoss = newPoints;
          this.$store.commit("handleShowNoss",newPoints);
        } else {
          useToast().error("支付失败！", {
            timeout: 1000
          });
        }
      })
      .catch(error => {
        console.error('Error topping up points:', error);
        useToast().error("支付失败！", {
            timeout: 1500
          });
      });
    },
    resetFileInput() {
      const fileInput = this.$refs.fileInput;
      fileInput.type = 'text';
      fileInput.type = 'file';
    },
    addTask() {
      // this.newTask.files.forEach(file => {
      //   const task = {
      //     id: this.taskIdCounter++,  // 分配并更新任务ID
      //     filename: file.name,
      //     type: this.newTask.type,
      //     cost: this.newTask.cost,
      //     status: "待处理"
      //   };
      //   this.tasks.push(task);
      // });
      // this.newTask = { files: [], type: "text", cost: 1 }; // 重置表单

      if(this.usernoss<this.newTask.cost){
        alert('NOSS点不足，请先充值！');
        return;
      }

      this.usernoss=this.usernoss-this.newTask.cost;
      this.handlePayCost(this.usernoss);

      var endpointMap = {};

      if(this.taskType==='encrypt'){
        endpointMap = {
        'text': '/batch/text/steg',
        'image': '/batch/img/steg',
        'audio': '/batch/audio/steg',
        'video': '/batch/video/steg'
        };
      }
      else{
        endpointMap = {
        'text': '/batch/text/decode',
        'image': '/batch/img/decode',
        'audio': '/batch/audio/decode',
        'video': '/batch/video/decode'
        };
      }

      const endpoint = endpointMap[this.newTask.type];

      let formData = new FormData();

      this.newTask.files.forEach(file => {
        formData.append('files', file); 
      });

      // 添加其他数据到 formData
      formData.append('type', this.newTask.type);
      formData.append('cost', this.newTask.cost);
      formData.append('model', this.newTask.model);
      formData.append('content', this.newTask.content);
      formData.append('userid',this.userid);

      const task = {
        id: this.taskIdCounter++,  // 分配并更新任务ID
        taskname: this.newTask.files.length===1?this.newTask.files[0].name:this.newTask.files[0].name+'等文件',
        type: this.newTask.type+"/"+this.taskType,
        cost: this.newTask.cost,
        status: "待处理",
      };
      this.tasks.push(task);

      // 发送 formData 到服务器
      axios.post(baseURL + endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data' 
        }
      })
      .then(response => {
        if(response.data.message==='Task Finished Success!'){
          useToast().success('任务提交成功！', {timeout: 1000});
          const downloadUrl = baseURL+response.data.download_url;  
          let tasklen = this.tasks.length;
          this.tasks[tasklen-1].status='可下载';
          this.tasks[tasklen-1].downloadUrl=downloadUrl;
          this.newTask = { files: [], type: "text", cost: 0 }; // 重置表单
          this.resetFileInput();
        }
        else{
          useToast().error('任务提交失败！', {timeout: 1000});
        }
      })
      .catch(error => {
        console.error("Error submitting the batch request: ", error);
        useToast().error('任务提交失败！', {timeout: 1000});
      });

    },
    fetchmodel(){
      this.models=[];
      axios.post(baseURL+'/gettypemodel', {type: this.newTask.type}).then(response => {
        if (response.data && response.data.message === 'Available models received!') {
          this.models=response.data.models;
          if (this.models.length > 0) {
            this.newTask.model = this.models[0]; // 设置下拉框自动选中第一个模型
          }
        } else {
          console.log('No models found:', response.data.message);
        }
      }).catch(error => {
        console.error('Model Receive error:', error);
        
      });
      if (this.newTask.type==='image' || this.newTask.type==='video'){
        axios.post(baseURL+'/gettypemodel', {type: 'iorv'}).then(response => {
        if (response.data && response.data.message === 'Available models received!') {
            for(let i=0;i<response.data.models.length;i++){
              this.models.push(response.data.models[i]);
            }
            if (this.models.length > 0) {
              this.newTask.model = this.models[0]; // 设置下拉框自动选中第一个模型
            }
          } else {
            console.log('No models found:', response.data.message);
          }
        }).catch(error => {
          console.error('Model Receive error:', error);
          
        });
      }
    }
  },
  watch: {
    'newTask.type': function(newType) {
      this.updateCost();
    }
  }
};
</script>



<style scoped>
.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 或根据需要调整间距 */
}

.form-label {
  font-weight: bold;
}

.form-control {
  border-radius: 0.25rem;
  border: 1px solid #ced4da;
  padding: 0.375rem 0.75rem;
}

.table {
  width: 100%;
  margin-bottom: 1rem;
  color: #212529;
}

th, td {
  padding: 0.75rem;
  text-align: center; /* 将表格的头部和单元格文本居中 */
  vertical-align: middle;
}

.btn-primary {
  color: #fff;
  background-color: #007bff;
  border-color: #007bff;
}

/* 按钮鼠标悬停效果 */
.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}
</style>

