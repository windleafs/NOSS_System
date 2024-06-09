<template>
  <div class="nav-wrapper position-relative end-0">
    <ul class="nav nav-pills nav-fill p-1" role="tablist">
      <li class="nav-item">
        <router-link
          class="nav-link mb-0 px-0 py-1 active active"
          to="/textsteg/encode"
          role="tab"
          aria-selected="true"
          >隐写模块</router-link
        >
      </li>
      <li class="nav-item">
        <router-link
          class="nav-link mb-0 px-0 py-1"
          to="/textsteg/decode"
          role="tab"
          aria-selected="false"
          >解码模块</router-link
        >
      </li>
    </ul>
  </div>
</template>

<script>
import setNavPills from "@/assets/js/nav-pills.js";

export default {
  name: "nav-pill",
  mounted() {
    setNavPills();
  },
  data(){
    return{

    }
  }
};
</script>
