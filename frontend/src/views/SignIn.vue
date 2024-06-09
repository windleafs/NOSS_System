<template>
  <div class="container top-0 position-sticky z-index-sticky">
    <div class="row">
      <div class="col-12">
        <navbar
          is-blur="blur blur-rounded my-3 py-2 start-0 end-0 mx-4 shadow"
          btn-background="bg-gradient-success"
          :dark-mode="true"
        />
      </div>
    </div>
  </div>
  <main class="mt-0 main-content main-content-bg">
    <section>
      <div class="page-header min-vh-75">
        <div class="container">
          <div class="row">
            <div class="mx-auto col-xl-4 col-lg-5 col-md-6 d-flex flex-column">
              <div class="mt-8 card card-plain">
                <div class="pb-0 card-header text-start">
                  <h3 class="font-weight-bolder text-success text-gradient">
                    NOSS 隐写系统
                  </h3>
                  <p class="mb-0">登录您的NOSS账号</p>
                </div>
                <div class="card-body">
                  <form role="form" class="text-start">
                    <label>用户名</label>
                    <soft-input
                      v-on:getsubvalue="handleSubValue('username',$event)"
                      :value="username"
                      id="email"
                      type="email"
                      placeholder="UserName"
                      name="email"
                    />
                    <label>密码</label>
                    <soft-input
                      v-on:getsubvalue="handleSubValue('password',$event)"
                      :value="password"
                      id="password"
                      type="password"
                      placeholder="Password"
                      name="password"
                    />
                    <soft-switch id="rememberMe" name="rememberMe" @click="handleRemember">
                      记住密码
                    </soft-switch>
                    <div class="text-center">
                      <soft-button
                        class="my-4 mb-2"
                        variant="gradient"
                        color="success"
                        full-width
                        @click="handleLogin"
                        >登&nbsp;&nbsp;录
                      </soft-button>
                    </div>
                  </form>
                </div>
                <div class="px-1 pt-0 text-center card-footer px-lg-2">
                  <p class="mx-auto mb-4 text-sm">
                    登录遇到问题?
                    <router-link
                      :to="{ name: 'Sign Up' }"
                      class="text-success text-gradient font-weight-bold"
                      >点我注册</router-link
                    >
                    <router-link
                      :to="{ name: 'Forget Password' }"
                      class="ms-2 text-success text-gradient font-weight-bold"
                      >忘记密码</router-link
                    >
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div
                class="top-0 oblique position-absolute h-100 d-md-block d-none me-n8"
              >
                <div
                  class="bg-cover oblique-image position-absolute fixed-top ms-auto h-100 z-index-0 ms-n6"
                  :style="{
                    backgroundImage:
                      'url(' +
                      require('@/assets/img/curved-images/curved9.jpg') +
                      ')',
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
  <app-footer />
</template>

<script>
import Navbar from "@/examples/PageLayout/Navbar.vue";
import AppFooter from "@/examples/PageLayout/Footer.vue";
import SoftInput from "@/components/SoftInput.vue";
import SoftSwitch from "@/components/SoftSwitch.vue";
import SoftButton from "@/components/SoftButton.vue";
const body = document.getElementsByTagName("body")[0];
import { mapMutations } from "vuex";
import { useToast } from "vue-toastification";
import baseURL from "@/config/config.js";

export default {
  name: "SignIn",
  components: {
    Navbar,
    AppFooter,
    SoftInput,
    SoftSwitch,
    SoftButton,
  },
  data(){
    return {
      username:'',
      password:'',
      toast:useToast(),
      rememberMe: false,
    }
  },
  mounted() {
    this.loadCredentials();
  },
  created() {
    this.toggleEveryDisplay();
    this.toggleHideConfig();
    body.classList.remove("bg-gray-100");
  },
  beforeUnmount() {
    this.toggleEveryDisplay();
    this.toggleHideConfig();
    body.classList.add("bg-gray-100");
  },
  methods: {
    ...mapMutations(["toggleEveryDisplay", "toggleHideConfig"]),
    handleRemember(){
      this.rememberMe=!this.rememberMe;
    },
    handleLogin(event){
      event.preventDefault();
      console.log(this.rememberMe);
      if (this.rememberMe) {
        localStorage.setItem('username', this.username);
        localStorage.setItem('password', this.password); 
      } else {
        localStorage.removeItem('username');
        localStorage.removeItem('password');
        localStorage.removeItem('rememberstate');
      }
      const xhr = new XMLHttpRequest();
      const formdata = new FormData();
      formdata.append('username',this.username);
      formdata.append('password',this.password);
      xhr.open('POST', baseURL+'/login');
      xhr.send(formdata);
      xhr.onreadystatechange = ()=> {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        const tres=JSON.parse(xhr.responseText);
        console.log(tres);
        if(tres.message!=='Fail to login!'){
          localStorage.setItem('jwtToken', tres.token);
          this.toast.success("登录成功！", {
            timeout: 1500
          });
          setTimeout(() => {
            this.$router.push('/'); 
          }, 1500);
        }
        else{
          this.toast.error("登录失败！", {
            timeout: 2000
          });
        }
      }};
    },
    handleSubValue(field, value) {
      this[field] = value;
    },
    loadCredentials() {
      this.username = localStorage.getItem('username') || '';
      this.password = localStorage.getItem('password') || '';
      this.rememberMe = !!this.username;
      if(this.rememberMe===true){
        document.getElementById("rememberMe").click();
        this.rememberMe=!this.rememberMe;
      }
    }
  },
};
</script>
