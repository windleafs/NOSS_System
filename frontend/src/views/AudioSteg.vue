<template>
    <div class="container-fluid">
        <div class="row">
          <div class="col-md-4">
            <audio-edit title="上传隐写音频：" btntitle="上传音频" flag="音频"></audio-edit>
          </div>
          <div class="col-md-8">
            <audio-edit title="请输入要隐写的文本：" btntitle="清除" flag="文字"></audio-edit>
          </div>
        </div>
        <div class="row">
          <div class="col-md-4">
            <audio-edit title="隐写后的音频：" btntitle="获取" flag="音频"></audio-edit>
          </div>
          <div class="col-md-8">
            <audio-edit title="解码出的文本：" btntitle="获取" flag="文字"></audio-edit>
          </div>
        </div>
    </div>
</template>

<script>
import setTooltip from "@/assets/js/tooltip.js"
import AudioEdit from './components/AudioEdit.vue';


export default {
  name: "AudioSteg",
  components: {
    AudioEdit
    
  },
  mounted() {
    setTooltip();
  },
};
</script>
