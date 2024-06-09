<template>
  <navbar btn-background="bg-gradient-primary" />
  <div
    class="pt-5 m-3 page-header align-items-start min-vh-50 pb-11 border-radius-lg"
    :style="{
      backgroundImage:
        'url(' + require('@/assets/img/curved-images/curved6.jpg') + ')',
    }"
  >
    <span class="mask bg-gradient-dark opacity-6"></span>
    <div class="container">
      <div class="row justify-content-center">
        <div class="mx-auto text-center col-lg-5">
          <h1 class="mt-5 mb-2 text-white">注 册</h1>
          <p class="text-white text-lead">
            注册NOSS账号，体验完整服务！
          </p>
        </div>
      </div>
    </div>
  </div>
  <div class="container">
    <div class="row mt-lg-n10 mt-md-n11 mt-n10 justify-content-center">
      <div class="mx-auto col-xl-4 col-lg-5 col-md-7">
        <div class="card z-index-0">
  
          <div class="card-body">
            <form role="form">
              <div class="mb-3">
                <soft-input
                  v-on:getsubvalue="handleSubValue('username',$event)"
                  :value="username"
                  id="name"
                  type="text"
                  placeholder="用户名"
                  aria-label="Name"
                />
              </div>
              <div class="mb-3">
                <soft-input
                  v-on:getsubvalue="handleSubValue('email',$event)"
                  :value="email"
                  id="email"
                  type="email"
                  placeholder="邮箱"
                  aria-label="Email"
                />
              </div>
              <div class="mb-3">
                <soft-input
                  v-on:getsubvalue="handleSubValue('password',$event)"
                  :value="password"
                  id="password"
                  type="password"
                  placeholder="密码"
                  aria-label="Password"
                />
              </div>
              <soft-checkbox
                id="flexCheckDefault"
                name="flexCheckDefault"
                class="font-weight-light"
                checked
              >
                我同意
                <a href="javascript:;" class="text-dark font-weight-bolder"
                  >NOSS隐写系统用户注册协议</a
                >
              </soft-checkbox>

              <div class="text-center">
                <soft-button
                  color="dark"
                  full-width
                  variant="gradient"
                  class="my-4 mb-2"
                  @click="handleSignUp"
                  >注 册</soft-button
                >
              </div>
              <p class="text-sm mt-3 mb-0">
                已有NOSS账号？
                <router-link
                  :to="{ name: 'Sign In' }"
                  class="text-dark font-weight-bolder"
                >
                  点我登录
                </router-link>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  <app-footer />
</template>

<script>
import Navbar from "@/examples/PageLayout/Navbar.vue";
import AppFooter from "@/examples/PageLayout/Footer.vue";
import SoftInput from "@/components/SoftInput.vue";
import SoftCheckbox from "@/components/SoftCheckbox.vue";
import SoftButton from "@/components/SoftButton.vue";
import baseURL from "@/config/config.js";
import { mapMutations } from "vuex";
import { useToast } from "vue-toastification";
export default {
  name: "SignupBasic",
  data(){
    return{
      username:'',
      email:'',
      password:'',
      toast:useToast(),
    }
  },
  components: {
    Navbar,
    AppFooter,
    SoftInput,
    SoftCheckbox,
    SoftButton,
  },
  created() {
    this.toggleEveryDisplay();
    this.toggleHideConfig();
  },
  beforeUnmount() {
    this.toggleEveryDisplay();
    this.toggleHideConfig();
  },
  methods: {
    ...mapMutations(["toggleEveryDisplay", "toggleHideConfig"]),
    handleSignUp(event){
      event.preventDefault();
      var regex = /[^a-zA-Z0-9]/;
      if(regex.test(this.username)===true){
        this.toast.error("用户名非法！", {
            timeout: 1000
          });
        return;
      }
      if(this.username===''||this.email===''||this.password===''){
        this.toast.error("信息填写不完整！", {
            timeout: 1000
          });
        return;
      }
      const xhr = new XMLHttpRequest();
      const formdata = new FormData();
      formdata.append('username',this.username);
      formdata.append('email',this.email);
      formdata.append('password',this.password);
      xhr.open('POST', baseURL+'/register');
      xhr.send(formdata);
      xhr.onreadystatechange = ()=> {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        const tres=JSON.parse(xhr.responseText);
        console.log(tres);
        this.username='';
        this.email='';
        this.password='';
        if(tres.message!=='Fail to register!'){
          this.toast.success("注册成功！", {
            timeout: 1000
          });
        }
        else{
          this.toast.error("注册失败！", {
            timeout: 1000
          });
        }
      }};
    },
    handleSubValue(field, value) {
      this[field] = value;
    },
  },
};
</script>
