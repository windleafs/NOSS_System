<template>
  <div class="container top-0 position-sticky z-index-sticky">
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
                    重置NOSS密码
                  </h3>
        
                </div>
                <div class="card-body">
                  <form role="form" class="text-start">
                    <label>用户名</label>
                    <div class="input-group mb-3">
                      <input type="text" class="form-control" v-model="username" placeholder="UserName" aria-label="Username" aria-describedby="username-addon">
                    </div>
                    <label>邮箱</label>
                    <div class="input-group mb-3">
                      <input type="email" class="form-control" v-model="email" placeholder="Email" aria-label="Email" aria-describedby="email-addon">
                    </div>
                    <label>验证码</label>
                    <div class="input-group mb-3 d-flex align-items-center">
                      <input type="text" class="form-control" v-model="captcha" placeholder="Verification Code" aria-label="Verification Code" aria-describedby="captcha-image" style="flex:1">
                      <img :src="captchaUrl" @click="refreshCaptcha" alt="captcha" id="captcha-image" style="height: calc(1.5em + .75rem + 2px); border: 2px solid #ccc; border-radius: 5px;"> <!-- 输入框的高度通常为calc(1.5em + .75rem + 2px)，也就是Bootstrap的默认值 -->
                    </div>
                    <label>新密码</label>
                    <div class="input-group mb-3">
                      <input type="password" class="form-control" v-model="newPassword" placeholder="New Password" aria-label="New Password">
                    </div>
                    <div class="text-center">
                      <button class="btn btn-success" @click="handleValidate" type="submit">重置密码</button>
                    </div>
                  </form>
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
import SoftButton from "@/components/SoftButton.vue";
const body = document.getElementsByTagName("body")[0];
import { mapMutations } from "vuex";
import { useToast } from "vue-toastification";
import baseURL from "@/config/config.js";

export default {
  name: "ResetPassword",
  components: {
    Navbar,
    AppFooter,
    SoftInput,
    SoftButton,
  },
  data() {
    return {
      username: '',
      email: '',
      captcha: '',
      newPassword: '',
      captchaUrl: baseURL + '/generate-captcha?' + new Date().getTime(),
      toast: useToast(),
      isvalid:false,
    };
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
    refreshCaptcha() {
      this.captchaUrl = baseURL + '/generate-captcha?' + new Date().getTime();
    },
    handleValidate(event) {
      event.preventDefault();
      const xhr = new XMLHttpRequest();
      const formdata = new FormData();
      formdata.append('captcha', this.captcha);
      xhr.open('POST', baseURL + '/verify-captcha');
      xhr.send(formdata);
      xhr.onreadystatechange = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          const response = JSON.parse(xhr.responseText);
          if (xhr.status === 200 && response.message === 'Captcha verified successfully') {
            this.isvalid=true;
            this.handleResetPassword();
          } else {
            this.toast.error("验证码错误！", { timeout: 1000 });
            this.refreshCaptcha();
          }
        }
      };
    },
    handleResetPassword() {
      // 重置密码逻辑
      const xhr = new XMLHttpRequest();
      const formdata = new FormData();
      console.log(this.username);
      console.log(this.email);
      formdata.append('username', this.username);
      formdata.append('email', this.email);
      formdata.append('newPassword', this.newPassword);
      xhr.open('POST', baseURL + '/reset-password');
      xhr.send(formdata);
      xhr.onreadystatechange = () => {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          if (response.message === 'Password reset successfully') {
            this.toast.success("密码重置成功！", {
              timeout: 1000
            });
            setTimeout(() => {
              this.$router.push('/sign-in'); 
            }, 1500);
          } else {
            this.toast.error("密码重置失败！", {
              timeout: 1000
            });
          }
        }
      };
    },
    handleSubValue(field, value) {
      this[field] = value;
    },
  },
};
</script>

<style scoped>
.input-group .form-control {
  flex: 1 1 auto; /* Flexbox property to allow the input to grow as needed */
}

.input-group .btn {
  margin-left: -1px; /* Removes the gap between the input and the button */
}

.input-group .form-control, .input-group .btn {
  height: 38px; /* Ensures consistent height between the button and input */
}
</style>