<template>
    <div class="modal-background">
      <div class="modal-content">
        <h5 class="modal-title">{{ editMode ? '编辑用户' : '添加用户' }}</h5>
        <form @submit.prevent="submit">
          <div class="form-group">
            <label for="username">用户名:</label>
            <input type="text" id="username" v-model="localUser.username" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="password">密码:</label>
            <input type="password" id="password" v-model="localUser.password" class="form-control">
          </div>
          <div class="form-group">
            <label for="email">邮箱:</label>
            <input type="email" id="email" v-model="localUser.email" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="nossPoints">noss点数:</label>
            <input type="number" id="nossPoints" v-model="localUser.nossPoints" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="role">身份:</label>
            <select id="role" v-model="localUser.role" class="form-control">
              <option value="admin">管理员</option>
              <option value="user">普通用户</option>
              <option value="vip">会员用户</option>
            </select>
          </div>
          <div class="form-group">
            <label for="membershipExpiration">会员到期时间:</label>
            <input type="date" id="membershipExpiration" v-model="localUser.membershipExpiration" class="form-control">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="$emit('close')">取消</button>
            <button type="submit" class="btn btn-primary">{{ editMode ? '更新' : '添加' }}</button>
          </div>
        </form>
      </div>
    </div>
</template>

<script>
import baseURL from "@/config/config.js";
import axios from 'axios';
import { useToast } from "vue-toastification";

export default {
  name:'UserModel',
  props: {
    userData: {
      type: Object,
      default: () => ({ id: null, username: '', password: '', email: '', nossPoints: 0, role: 'user' ,membershipExpiration:''})
    },
    editMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localUser: { ...this.userData},
      toast:useToast(),
    };
  },
  methods: {
    formatDate(dateStr) {
      return dateStr.split('-').join('/');
    },
    submit() {
      if (this.localUser.membershipExpiration) {
        this.localUser.membershipExpiration = this.formatDate(this.localUser.membershipExpiration);
      }
      else{
        this.localUser.membershipExpiration='1970/01/01';
      }
      this.$emit('save', this.localUser);
      // axios.post(baseURL+'/setuser', this.localUser, {
      //   headers: {
      //     'Content-Type': 'application/json'
      //   }
      // })
      // .then(response => {
      //   console.log('Submission successful', response.data);
      //   if(response.data.success===true){
      //     this.$emit('save', this.localUser);
      //     this.toast.success("添加成功！", {
      //       timeout: 1000
      //     });
      //   }
      //   else{
      //     this.toast.error("添加失败！", {
      //       timeout: 1000
      //     });
      //   }
      //   this.$emit('close');
      // })
      // .catch(error => {
      //   console.error('Error submitting form', error);
      //   this.toast.error("添加失败！", {
      //     timeout: 1000
      //   });
      // });
    }
  },
  watch: {
    userData: {
      handler(newVal) {
        this.localUser = { ...newVal };
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 90%;
  max-width: 500px;
}

.modal-title {
  margin-bottom: 15px;
}

.form-group {
  margin-bottom: 10px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
