<template>
  <div class="container-fluid">
    <div
      class="mt-4 page-header min-height-300 border-radius-xl"
      :style="{
        backgroundImage:
          'url(' + require('@/assets/img/curved-images/curved14.jpg') + ')',
        backgroundPositionY: '50%',
      }"
    >
      <span class="mask bg-gradient-success opacity-6"></span>
    </div>
    <div class="mx-4 overflow-hidden card card-body blur shadow-blur mt-n6">
      <div class="row gx-4">
        <div class="col-auto my-auto">
          <div class="h-100">
            <h5 class="mb-1">{{ username }}</h5>
            <p class="mb-0 text-sm font-weight-bold">
              {{ isLogin ? (userrole==='vip' ? '会员用户' : (userrole==='admin' ? '管理员' : '普通用户')) : '游客用户' }}
              
              <span v-if="isMember && membershipExpiration"> - 到期时间: {{ membershipExpiration }}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="py-4 container-fluid">
    <div class="mt-3 row">
      <div class="col-12 col-md-6 col-xl-8">
        <div class="card h-100">
          <div class="p-3 pb-0 card-header d-flex justify-content-between align-items-center">
            <h6 class="mb-0">会员权益</h6>
            <button class="btn btn-sm btn-primary transition-3d-hover" @click="handleShowModel">
              {{ isLogin ? (isMember ? '续费会员' : '成为会员') : '成为会员' }}
            </button>
          </div>
          <div class="p-3 card-body">
            <p class="text-muted">作为会员，您可以享受以下专属权益：</p>
            <ul class="list-unstyled">
              <li><i class="fas fa-check-circle text-success"></i> 独家折扣</li>
              <li><i class="fas fa-check-circle text-success"></i> 更强大的模型访问权限</li>
              <li><i class="fas fa-check-circle text-success"></i> 优先客户服务</li>
            </ul>
            <img src="@/assets/img/vip.jpg" alt="会员权益" class="img-fluid rounded mb-3">
          </div>
        </div>
      </div>
      <div class="mt-4 col-12 col-xl-4 mt-xl-0">
        <div class="card h-100">
          <div class="p-3 pb-0 card-header">
            <h6 class="mb-0">NOSS点</h6>
          </div>
          <div class="p-3 card-body">
            <div class="mb-4">
              <div class="fs-2 fw-bold text-center mb-3">{{ usernoss }}</div>
            </div>
            <div class="mb-3">
              <label for="rechargeAmount" class="form-label">输入充值金额（元）：</label>
              <input type="number" class="form-control" id="rechargeAmount" placeholder="请输入金额" @input="calculatePoints">
            </div>
            <div class="mb-4">
              <label for="nossPoints" class="form-label">您将获得的NOSS点：</label>
              <input type="text" class="form-control" id="nossPoints" placeholder="0" readonly>
            </div>
            <button class="btn btn-success w-100" @click="handleTopUp">立即充值</button>
          </div>
        </div>
      </div>
    </div>
    <member-model v-if="showModel" :member="isMember" :nossPoints="usernoss" @updatenoss="handleUpdate" @close="handleCloseModel" ></member-model>
  </div>
</template>

<script>
import SoftSwitch from "@/components/SoftSwitch.vue";
import ProfileInfoCard from "./components/ProfileInfoCard.vue";
import SoftAvatar from "@/components/SoftAvatar.vue";
import sophie from "@/assets/img/kal-visuals-square.jpg";
import marie from "@/assets/img/marie.jpg";
import ivana from "@/assets/img/ivana-square.jpg";
import peterson from "@/assets/img/team-4.jpg";
import nick from "@/assets/img/team-3.jpg";
import img1 from "@/assets/img/home-decor-1.jpg";
import img2 from "@/assets/img/home-decor-2.jpg";
import img3 from "@/assets/img/home-decor-3.jpg";
import team1 from "@/assets/img/team-1.jpg";
import team2 from "@/assets/img/team-2.jpg";
import team3 from "@/assets/img/team-3.jpg";
import team4 from "@/assets/img/team-4.jpg";
import {
  faFacebook,
  faTwitter,
  faInstagram,
} from "@fortawesome/free-brands-svg-icons";
import DefaultProjectCard from "./components/DefaultProjectCard.vue";
import PlaceHolderCard from "@/examples/Cards/PlaceHolderCard.vue";
import setNavPills from "@/assets/js/nav-pills.js";
import setTooltip from "@/assets/js/tooltip.js";
import baseURL from "@/config/config.js";
import axios from 'axios';
import { useToast } from "vue-toastification";
import MemberModel from './MemberModel.vue';
export default {
  name: "ProfileOverview",
  components: {
    SoftSwitch,
    ProfileInfoCard,
    SoftAvatar,
    DefaultProjectCard,
    PlaceHolderCard,
    MemberModel,
  },
  data() {
    return {
      showMenu: false,
      sophie,
      marie,
      ivana,
      peterson,
      nick,
      img1,
      team1,
      team2,
      team3,
      team4,
      img2,
      img3,
      faFacebook,
      faTwitter,
      faInstagram,
      isLogin:false,
      username:'',
      userrole:'',
      usernoss:0,
      userid:0,
      toast:useToast(),
      isMember: false, 
      showModel: false,
      membershipExpiration:'',
      isAdmin:false,
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
  mounted() {
    this.$store.state.isAbsolute = true;
    setNavPills();
    setTooltip(this.$store.state.bootstrap);
  },
  beforeUnmount() {
    this.$store.state.isAbsolute = false;
  },
  methods:{
    calculatePoints(event) {
      const amount = event.target.value;
      const points = amount * 100; // 假设每1元可兑换100个NOSS点
      document.getElementById('nossPoints').value = points;
    },
    getUserInfo(){
      axios.post(baseURL+'/getuinfo', { user_id: this.userid })
        .then(response => {
          if (response.data && response.data.user_info) {
            this.username= response.data.user_info.username;
            this.usernoss= response.data.user_info.noss_points;
            this.userrole= response.data.user_info.role;
            if(this.userrole==='vip'){
              this.isMember=true;
              this.membershipExpiration= response.data.user_info.membership_expiration;
            }
            if(this.userrole==='admin'){
              this.isAdmin=true;
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
    handleTopUp(){
      if(this.isLogin===false){
        alert('请先登录！');
        return;
      }
      
      if(this.isAdmin===true){
        alert('您已经是管理员！');
        return;
      }
      const pointsInput = document.getElementById('nossPoints');
      var pointsToAdd = parseInt(pointsInput.value, 10);
      if (isNaN(pointsToAdd) || pointsToAdd < 0) {
        alert('请输入一个合法的数字！');
        return;
      }

      var newPointsTotal = this.usernoss + pointsToAdd;;
      axios.post(baseURL + '/topup', {
        user_id: this.userid, 
        points: newPointsTotal
      })
      .then(response => {
        if (response.data && response.data.success) {
          this.usernoss = newPointsTotal;
          this.$store.commit("handleShowNoss",newPointsTotal);
          this.toast.success("充值成功！", {
            timeout: 1000
          });
        } else {
          this.toast.error("充值失败！", {
            timeout: 1000
          });
        }
      })
      .catch(error => {
        console.error('Error topping up points:', error);
        this.toast.error("充值失败！", {
            timeout: 1500
          });
      });
    },
    handleShowModel(){
      if(this.isLogin===false){
        alert('请先登录！');
        return;
      }
      if(this.isAdmin===true){
        alert('您已经是管理员！');
        return;
      }
      this.showModel=true;
    },
    handleCloseModel(){
      this.showModel=false;
    },
    handleUpdate(newpoints){
      var month = 0;
      if(this.usernoss-newpoints===3000){
        month=1;
      }
      else if(this.usernoss-newpoints===8000){
        month=3;
      }
      else{
        month=12;
      }
      axios.post(baseURL + '/topup/vip', {
        user_id: this.userid, 
        points: newpoints,
        expiration: month
      })
      .then(response => {
        if (response.data && response.data.success) {
          this.usernoss = newpoints;
          this.userrole = 'vip';
          this.isMember = true;
          this.membershipExpiration = response.data.membership_expiration;
          this.$store.commit("handleShowNoss",newpoints);
          this.toast.success("开通成功！", {
            timeout: 1000
          });
        } else {
          this.toast.error("开通失败！", {
            timeout: 1000
          });
        }
      })
      .catch(error => {
        console.error('Error:', error);
        this.toast.error("开通失败！", {
            timeout: 1500
          });
      });
      this.handleCloseModel();
    }
  }
};
</script>


<style scoped>
.fs-2 {
  font-size: 2rem; /* 大号字体 */
}

.fw-bold {
  font-weight: bold; /* 加粗 */
}

.form-label {
  font-size: 0.875rem;
  color: #6c757d;
}

.form-control {
  border-radius: 0.375rem;
  border: 1px solid #ced4da;
  padding: 0.375rem 0.75rem;
}

.btn {
  margin-top: 10px;
}
.img-fluid {
  width: 100%;
  height: 200px;
}

.transition-3d-hover {
  transition: all 0.3s ease-in-out;
}

.transition-3d-hover:hover {
  transform: translateY(-5px);
}

.fas {
  margin-right: 10px;
}

.text-muted {
  color: #6c757d;
}
</style>