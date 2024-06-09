<template>
    <div class="modal-background" @click="handleBackgroundClick">
      <div class="modal-content">
        <h5 class="modal-title">{{ member ? '续费会员' : '成为会员' }}</h5>
        <div class="options-container">
          <div class="membership-option" v-for="option in membershipOptions" :key="option.type">
            <div class="membership-type">{{ option.name }}</div>
            <div class="membership-price">{{ option.price }} NOSS点</div>
            <button type="button" class="btn btn-primary buy-button" @click="handlePurchase(option.type)">
              {{ member ? '续费' : '购买' }}
            </button>
          </div>
        </div>
      </div>
    </div>
</template>


<script>
export default {
  name:'MemberModel',
  props: {
    member: {
      type: Boolean,
      default: false
    },
    nossPoints: {
      type: String,
      default: false
    },
  },
  data() {
    return {
      membershipOptions: [
        { name: '月卡会员', price: 3000, type: 'monthly' },
        { name: '季卡会员', price: 8000, type: 'quarterly' },
        { name: '年卡会员', price: 19999, type: 'yearly' }
      ]
    };
  },
  methods: {
    handleBackgroundClick(event) {
      if (event.target === event.currentTarget) {
        this.$emit('close')
      }
    },
    handlePurchase(type) {
      var curnoss = parseInt(this.nossPoints);
      var cost = 3000;
      if(type==='quarterly'){
        cost = 8000;
      }
      else if(type==='yearly'){
        cost = 19999;
      }
      else{
        cost = 3000;
      }
      if(curnoss<cost){
        alert('NOSS点不足，请先充值！');
      }
      else{
        var newpoints = curnoss-cost;
        this.$emit('updatenoss',newpoints);
      }
    },
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
  background-color: rgba(0, 0, 0, 0.6); /* 更深的背景色提高对比 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background: white;
  padding: 30px; /* 增加内边距 */
  border-radius: 8px; /* 更圆滑的边框 */
  width: 80%; /* 调整宽度 */
  max-width: 600px; /* 增加最大宽度 */
}

.modal-title {
  font-size: 1.5rem; /* 更大的标题字体 */
  color: #333; /* 深色字体 */
  margin-bottom: 20px;
  text-align: center;
}

.options-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 栅格布局，平均分配空间 */
  gap: 20px; /* 栅格间距 */
}

.membership-option {
  background: #f9f9f9; /* 更浅的背景色 */
  border: 2px solid #ccc; /* 边框更显著 */
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between; /* 内容平均分布 */
}

.membership-type {
  font-size: 1.2rem; /* 类型字体放大 */
  font-weight: bold;
  color: #0056b3; /* 使用主题颜色 */
  margin-bottom: 10px;
}

.membership-price {
  font-size: 1.1rem; /* 价格字体大小 */
  color: #555; /* 更深的字体颜色 */
  font-weight: bold;
  margin-bottom: 15px;
}

.buy-button {
  width: 100%;
  padding: 10px 0; /* 增加按钮的填充 */
  font-size: 1rem; /* 按钮字体大小 */
}
</style>


