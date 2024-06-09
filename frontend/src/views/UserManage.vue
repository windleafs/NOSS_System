<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0 d-flex justify-content-between align-items-center">
            <div>
              <button class="btn btn-primary mb-3" @click="showAddUserModal = true">添加用户</button>
            </div>
            <div class="search-container">
              <input type="text" class="form-control" placeholder="搜索用户名..." v-model="searchQuery">
            </div>
          </div>
          <div class="card-body">
            <table class="table text-center">
              <thead>
                <tr>
                  <th>用户ID</th>
                  <th>用户名</th>
                  <th>邮箱</th>
                  <th>noss点数</th>
                  <th>身份</th>
                  <th>会员到期时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.nossPoints }}</td>
                  <td>{{ user.role }}</td>
                  <td>{{ user.membershipExpiration }}</td> 
                  <td>
                    <button class="btn btn-info btn-sm" @click="editUser(user)">编辑</button>
                    <button class="btn btn-danger btn-sm" @click="deleteUser(user.id)">删除</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <user-model v-if="showAddUserModal || editMode" :edit-mode="editMode" :user-data="currentUser" @close="closeModal" @save="saveUser"></user-model>
  </div>
</template>




<script>
import UserModel from './UserModel.vue'; 
import baseURL from "@/config/config.js";
import axios from 'axios';
import { useToast } from "vue-toastification";

export default {
  name: "UserManage",
  components: {
    UserModel
  },
  data() {
    return {
      users: [],
      showAddUserModal: false,
      editMode: false,
      currentUser: null,
      searchQuery: '',
      isLogin:false,
      username:'',
      userrole:'',
      usernoss:0,
      userid:0,
      toast:useToast(),
      isMember: false, 
      showModel: false,
      membershipExpiration:'',
    };
  },
  created() {
    this.fetchUsers(); 
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.isLogin = false;
      alert('您无权访问！');
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
        this.getUserInfo();
        
      } else {
        this.isLogin = false;
      }
    }).catch(error => {
      console.error('Authentication error:', error);
      this.isLogin = false;
    });
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user =>
        user.username.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
      addUser() {
          this.currentUser = { id: null, username: '', email: '', nossPoints: 0, role: '', membershipExpiration: ''};
          this.editMode = false;
          this.showAddUserModal = true;
      },
      editUser(user) {
          this.currentUser = { ...user };
          this.editMode = true;
          this.showAddUserModal = true;
      },
      deleteUser(userId) {
          if(confirm('确定要删除此用户吗？')) {
              axios.delete(`${baseURL}/deleteuser/${userId}`)
              .then(() => {
                  this.users = this.users.filter(user => user.id !== userId);
                  useToast().success('用户已成功删除',{timeout: 1000});
              })
              .catch(error => {
                  console.error('Error deleting user:', error);
                  useToast().error('删除用户失败',{timeout: 1000});
              });
          }
      },
      closeModal() {
          this.showAddUserModal = false;
          this.editMode = false;
      },
      saveUser(userData) {
          const url = this.editMode ? `${baseURL}/updateuser` : `${baseURL}/setuser`;
          axios.post(url, userData)
          .then(response => {
              if(this.editMode) {
                  this.users = this.users.map(user => user.id === userData.id ? {...user, ...userData} : user);
              } else {
                  this.fetchUsers(); // 重新获取所有用户信息以更新列表
              }
              useToast().success(this.editMode ? '用户信息已更新' : '用户已添加',{timeout: 1000});
              this.closeModal();
          })
          .catch(error => {
              console.error('Error saving user:', error);
              useToast().error(this.editMode ? '更新用户信息失败' : '添加用户失败',{timeout: 1000});
          });
      },
      fetchUsers() {
          axios.get(`${baseURL}/getuser`)
          .then(response => {
              this.users = response.data.users;
          })
          .catch(error => {
              console.error('Error fetching users:', error);
          });
      },
      getUserInfo(){
        axios.post(baseURL+'/getuinfo', { user_id: this.userid })
          .then(response => {
            if (response.data && response.data.user_info) {
              this.username= response.data.user_info.username;
              this.usernoss= response.data.user_info.noss_points;
              this.userrole= response.data.user_info.role;
              if(this.userrole!=='admin'){
                alert('您无权访问！');
                this.$router.push('/dashboard');
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
  }
};
</script>


<style scoped>
.search-container {
  width: 250px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th, .table td {
  text-align: center;
  vertical-align: middle;
}

.btn {
  margin-right: 5px;
}

.user-modal {
  display: block;
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  z-index: 1000;
}
</style>




