<template>
    <div class="container-fluid">
        
        <div class="row">
            <div class="col-md-6">
                <image-edit title="请上传要隐写的图片：" flag="图片" btntitle="上传图片"></image-edit>
            </div>
            <div class="col-md-6">
                <image-edit title="隐写后的图片：" flag="图片" btntitle="获取"></image-edit>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <image-edit title="请输入要隐写的文字：" flag="文字" btntitle="清除"></image-edit>
            </div>
            <div class="col-md-6">
                <image-edit title="解码出的文字：" flag="文字" btntitle="获取"></image-edit>
            </div>
        </div>
    </div>
</template>

<script>
import setTooltip from "@/assets/js/tooltip.js"
import ImageEdit from "./components/ImageEdit.vue"


export default {
  name: "ImageSteg",
  components: {
    ImageEdit,
  },
  data() {
    return {
      selectedModel: 'model1', // Default selected model
    };
  }, 
  mounted() {
    setTooltip();
  },
};
</script>


<style scoped>
.card {
    margin-bottom: 20px; /* Ensure space between this card and the next row */
}

.form-control {
    margin-top: 10px; /* Spacing for better form layout */
}

.card-header {
    background-color: #eeeeee; /* A light background for the card header */
}
</style>
