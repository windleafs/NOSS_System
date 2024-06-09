<template>
    <div class="container-fluid">
      
        <div class="row">
          <div class="col-md-6">
            <video-edit title="上传隐写视频：" btntitle="上传视频" flag="视频"></video-edit>
          </div>
          <div class="col-md-6">
            <video-edit title="隐写后的视频：" btntitle="获取" flag="视频"></video-edit>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <video-edit title="请输入要隐写的文本：" btntitle="清除" flag="文字"></video-edit>
          </div>
          <div class="col-md-6">
            <video-edit title="解码出的文本：" btntitle="获取" flag="文字"></video-edit>
          </div>
        </div>
    </div>
</template>

<script>
import setTooltip from "@/assets/js/tooltip.js"
import VideoEdit from './components/VideoEdit.vue';
import baseURL from "@/config/config.js";
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  name: "VideoSteg",
  components: {
    VideoEdit
    
  },
  data(){
    return {
      selectedModel:'model1',
      isLogin:false,
      username:'',
      userrole:'',
      usernoss:0,
      userid:0,
      toast:useToast(),
      isMember: false, 
      showModel: false,
      membershipExpiration:'',
    }
  },
  created() {
    this.fetchUsers(); 
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.isLogin = false;
      alert('请注册以体验此功能！');
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
      
      } else {
        this.isLogin = false;
        alert('请注册以体验此功能！');
        this.$router.push('/dashboard');
        return;
      }
    }).catch(error => {
      console.error('Authentication error:', error);
      this.isLogin = false;
      alert('请注册以体验此功能！');
      this.$router.push('/dashboard');
      return;
    });
  },
  mounted() {
    setTooltip();
  },
  methods:{
    fetchUsers() {
        axios.get(`${baseURL}/getuser`)
        .then(response => {
            this.users = response.data.users;
        })
        .catch(error => {
            console.error('Error fetching users:', error);
        });
    },
  }
};
</script>


<style scoped>
.card {
    margin-bottom: 20px; /* Ensure space between this card and the next row */
}

.form-control {
    margin-top: 10px; /* Spacing for better form layout */
}

.card-header {
    background-color: #eeeeee; /* A light background for the card header */
}
</style>