<template>
  <nav
    class="shadow-none navbar navbar-main navbar-expand-lg border-radius-xl"
    v-bind="$attrs"
    id="navbarBlur"
    data-scroll="true"
  >
    <div class="px-3 py-1 container-fluid">
      <breadcrumbs :currentPage="currentRouteName" :textWhite="textWhite" />
      <div
        class="mt-2 collapse navbar-collapse mt-sm-0 me-md-0 me-sm-4"
        :class="this.$store.state.isRTL ? 'px-0' : 'me-sm-4'"
        id="navbar"
      >
        <div
          class="pe-md-3 d-flex align-items-center"
          :class="this.$store.state.isRTL ? 'me-md-auto' : 'ms-md-auto'"
        >
          
        </div>
        <ul class="navbar-nav justify-content-end">
          <li class="nav-item d-flex align-items-center">
            <span class="d-sm-inline d-none fw-bold text-info">NOSS点：{{ this.$store.state.showNoss }}&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <router-link
              :to="{ name: 'Sign In' }"
              class="px-0 nav-link font-weight-bold"
              :class="textWhite ? textWhite : 'text-body'"
              @click="handleBar"
            >
            
              <i
                class="fa fa-user"
                :class="this.$store.state.isRTL ? 'ms-sm-2' : 'me-sm-1'"
              ></i>
              <span v-if="this.$store.state.isRTL" class="d-sm-inline d-none"
                >يسجل دخول</span
              >
              <span v-else class="d-sm-inline d-none">{{ barText }}</span>
            </router-link>
          </li>
          <li class="nav-item d-xl-none ps-3 d-flex align-items-center">
            <a
              href="#"
              @click="toggleSidebar"
              class="p-0 nav-link text-body"
              id="iconNavbarSidenav"
            >
              <div class="sidenav-toggler-inner">
                <i class="sidenav-toggler-line"></i>
                <i class="sidenav-toggler-line"></i>
                <i class="sidenav-toggler-line"></i>
              </div>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
import Breadcrumbs from "../Breadcrumbs.vue";
import { mapMutations, mapActions } from "vuex";
import axios from 'axios';
import baseURL from "@/config/config.js";
export default {
  name: "navbar",
  data() {
    return {
      showMenu: false,
      barText: '登录',
      isLogin:false,
      username:'',
      userrole:'',
      usernoss:0,
      userid:0,
      isMember: false, 
      showModel: false,
      membershipExpiration:'',
    };
  },
  mounted(){
    
  },
  props: ["minNav", "textWhite"],
  created() {
    this.minNav;
    this.checkAuthentication();
  },
  methods: {
    ...mapMutations(["navbarMinimize", "toggleConfigurator"]),
    ...mapActions(["toggleSidebarColor"]),

    toggleSidebar() {
      this.toggleSidebarColor("bg-white");
      this.navbarMinimize();
    },
    checkAuthentication() {
      const token = localStorage.getItem('jwtToken');
      if (!token) {
        this.isAuthenticated = false;
        this.barText = "登录";
        return;
      }
      
      axios.get(baseURL+'/validate', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }).then(response => {
        if (response.data && response.data.message === 'Token is valid!') {
          this.isAuthenticated = true;
          this.userid = response.data.user_id;
          this.barText = "退出登录";
          //this.getUserInfo();
        } else {
          this.isAuthenticated = false;
          this.barText = "登录";
        }
      }).catch(error => {
        console.error('Authentication error:', error);
        this.isAuthenticated = false;
        this.barText = "登录";
      });
    },
    getUserInfo(){
        axios.post(baseURL+'/getuinfo', { user_id: this.userid })
          .then(response => {
            if (response.data && response.data.user_info) {
              this.username= response.data.user_info.username;
              this.usernoss= response.data.user_info.noss_points;
              this.userrole= response.data.user_info.role;
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
    handleBar(){
      if(this.barText==='退出登录'){
        localStorage.setItem('jwtToken','');
      }
    }
  },
  components: {
    Breadcrumbs,
  },
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
  },
  updated() {
    const navbar = document.getElementById("navbarBlur");
    window.addEventListener("scroll", () => {
      if (window.scrollY > 10 && this.$store.state.isNavFixed) {
        // navbar.classList.add("blur");
        // navbar.classList.add("position-sticky");
        // navbar.classList.add("shadow-blur");
      } else {
        // navbar.classList.remove("blur");
        // navbar.classList.remove("position-sticky");
        // navbar.classList.remove("shadow-blur");
      }
    });
  },
};
</script>
