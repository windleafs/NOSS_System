import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "@/views/Dashboard.vue";
import Profile from "@/views/Profile.vue";
import SignIn from "@/views/SignIn.vue";
import SignUp from "@/views/SignUp.vue";
import TextSteg from "@/views/TextSteg.vue";
import ImageSteg from "@/views/ImageSteg.vue";
import AudioSteg from "@/views/AudioSteg.vue";
import VideoSteg from "@/views/VideoSteg.vue";
import TextDecode from "@/views/TextDecode.vue";
import TextEnode from "@/views/TextEncode.vue";
import UserManage from "@/views/UserManage.vue";
import BatchStega from "../views/BatchStega.vue";
import ForgetPassword from '@/views/ForgetPassword.vue';
import ModelManage from '@/views/ModelManage.vue';

const routes = [
  {
    path: "/",
    name: "/",
    redirect: "/dashboard",
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/batchstega",
    name: "BatchStega",
    component: BatchStega,
  },
  {
    path: "/textsteg",
    name: "TextSteg",
    component: TextSteg,
  },
  {
    path: "/textsteg/encode",
    name: "TextEncode",
    component: TextEnode,
  },
  {
    path: "/textsteg/decode",
    name: "TextDecode",
    component: TextDecode,
  },
  {
    path: "/ImageSteg",
    name: "ImageSteg",
    component: ImageSteg,
  },
  {
    path: "/audiosteg",
    name: "AudioSteg",
    component: AudioSteg,
  },
  {
    path: "/videosteg",
    name: "VideoSteg",
    component: VideoSteg,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/usermanage",
    name: "UserManage",
    component: UserManage,
  },
  {
    path: "/sign-in",
    name: "Sign In",
    component: SignIn,
  },
  {
    path: "/sign-up",
    name: "Sign Up",
    component: SignUp,
  },
  {
    path: "/forgetpwd",
    name: "Forget Password",
    component: ForgetPassword,
  },
  {
    path: "/modelmanage",
    name: "ModelManage",
    component: ModelManage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});

export default router;
