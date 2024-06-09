<template>
  <div
    class="w-auto h-auto collapse navbar-collapse max-height-vh-100 h-100"
    id="sidenav-collapse-main"
  >
    <ul class="navbar-nav">
      <li class="nav-item">
        <sidenav-collapse navText="欢迎页" :to="{ name: 'Dashboard' }">
          <template #icon>
            <shop />
          </template>
        </sidenav-collapse>
      </li>
      <!-- <li class="nav-item">
        <sidenav-collapse navText="信息表" :to="{ name: 'Tables' }">
          <template #icon>
            <office />
          </template>
        </sidenav-collapse>
      </li> -->
      <li class="nav-item">
        <sidenav-collapse navText="文字隐写" :to="{ name: 'TextSteg' }">
          <template #icon>
            <document />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse navText="图像隐写" :to="{ name: 'ImageSteg' }">
          <template #icon>
            <basket />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse navText="音频隐写" :to="{ name: 'AudioSteg' }">
          <template #icon>
            <spaceship />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse navText="视频隐写" :to="{ name: 'VideoSteg' }">
          <template #icon>
            <credit-card />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse navText="批量隐写" :to="{ name: 'BatchStega' }">
          <template #icon>
            <office />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item" v-show="showManage">
        <sidenav-collapse navText="用户管理" :to="{ name: 'UserManage' }">
          <template #icon>
            <office />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item" v-show="showManage">
        <sidenav-collapse navText="模型管理" :to="{ name: 'ModelManage' }">
          <template #icon>
            <office />
          </template>
        </sidenav-collapse>
      </li>
      <li class="mt-3 nav-item">
        <h6
          class="text-xs ps-4 text-uppercase font-weight-bolder opacity-6"
          :class="this.$store.state.isRTL ? 'me-4' : 'ms-2'"
        >
          PAGES
        </h6>
      </li>
      <li class="nav-item">
        <sidenav-collapse navText="个人中心" :to="{ name: 'Profile' }">
          <template #icon>
            <customer-support />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse navText="登录" :to="{ name: 'Sign In' }">
          <template #icon>
            <document />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse navText="注册" :to="{ name: 'Sign Up' }">
          <template #icon>
            <spaceship />
          </template>
        </sidenav-collapse>
      </li>
    </ul>
  </div>
</template>
<script>
import SidenavCollapse from "./SidenavCollapse.vue";
import Shop from "../../components/Icon/Shop.vue";
import Office from "../../components/Icon/Office.vue";
import CreditCard from "../../components/Icon/CreditCard.vue";
import CustomerSupport from "../../components/Icon/CustomerSupport.vue";
import Document from "../../components/Icon/Document.vue";
import Spaceship from "../../components/Icon/Spaceship.vue";
import Basket from '../../components/Icon/Basket.vue';
import baseURL from "@/config/config.js";
import axios from 'axios';

export default {
  name: "SidenavList",
  props: {
    cardBg: String,
  },
  data() {
    return {
      title: "Soft UI Dashboard PRO",
      controls: "dashboardsExamples",
      isActive: "active",
      isLogin:false,
      username:'',
      userrole:'',
      usernoss:0,
      userid:0,
      isMember: false, 
      showModel: false,
      membershipExpiration:'',
      showManage:false,
    };
  },
  created(){
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.isLogin = false;
      this.$store.commit("handleShowNoss",0);
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
        this.$store.commit("handleShowNoss",0);
      }
    }).catch(error => {
      console.error('Authentication error:', error);
      this.isLogin = false;
      this.$store.commit("handleShowNoss",0);
    });
  },
  components: {
    SidenavCollapse,
    Shop,
    Office,
    CreditCard,
    CustomerSupport,
    Document,
    Spaceship,
    Basket
  },
  methods: {
    getRoute() {
      const routeArr = this.$route.path.split("/");
      return routeArr[1];
    },
    getUserInfo(){
        axios.post(baseURL+'/getuinfo', { user_id: this.userid })
          .then(response => {
            if (response.data && response.data.user_info) {
              this.username= response.data.user_info.username;
              this.usernoss= response.data.user_info.noss_points;
              this.userrole= response.data.user_info.role;
              this.$store.commit("handleShowNoss",this.usernoss);
              if(this.userrole==='admin'){
                this.showManage = true;
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
  },
};
</script>
