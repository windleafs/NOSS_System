<template>
 <div class="card mt-4">
    <div class="card-header pb-0 p-3">
      <div class="row">
        <div class="col-6 d-flex align-items-center">
          <h6 class="mb-0">{{ title }}</h6>
        </div>
        <div class="col-6 text-end">
          <input type="file" ref="upload2" @change="viewAudio2" style="display:none;"/>
          <soft-button ref="leftbtn" :style="'visibility:'+(title==='隐写后的音频：'?'visible':'hidden')" @click="uploadImg2" color="dark" variant="gradient">
            上传
          </soft-button>
        </div>
      </div>
    </div>
    <div class="card-body p-3">
      <div class="row">
        <div class="container duiqi">
            <div class="form-group">
                <audio :src="audioURL" ref="audWin" v-show="flag==='文字'?false:true" controls></audio>
                <textarea v-show="flag==='文字'?true:false" @change="keepHideText" class="form-control" v-model="srctext" id="FormControlTextarea1" rows="2"></textarea>
            </div>
        </div>
        <div class="col-12 duiqi">
            <input type="file" ref="upload" @change="viewAudio" style="display:none;"/>
            <soft-button @click="handlebtn" color="dark" variant="gradient">
            {{ btntitle }}
            </soft-button>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>
import SoftButton from "@/components/SoftButton.vue";
import baseURL from "@/config/config.js";


export default {
    name:'AudioEdit',
    components:{
        SoftButton,
    },
    props:{
        title:String,
        flag:String,
        btntitle:String,
    },
    data(){
        return{
            audioURL:'',
            srctext:'',
            audioFile:null,
            audioEnText:'',
            audioDeText:'',
        }
    },
    methods:{
        uploadImg(){
            this.$refs.upload.click();
        },
        uploadImg2(){
            this.$refs.upload2.click();
        },
        clrText(){
            this.srctext='';
        },
        viewAudio(e){
            const file = e.target.files[0];
            this.audioFile=file
            const reader = new FileReader();
            reader.onload = (e) => {
                this.audioURL = e.target.result; 
            };
            reader.readAsDataURL(file);
            if(this.title==='上传隐写音频：'){
                this.$store.commit('handelAudFile',this.audioFile);
            }
        },
        viewAudio2(e){
            const file = e.target.files[0];
            this.audioFile=file;
            const reader = new FileReader();
            reader.onload = (e) => {
                this.audioURL = e.target.result; 
            };
            reader.readAsDataURL(file);
            this.$store.commit('handleAudURL',this.audioURL);
            if(this.title==="隐写后的音频："){
                this.$store.commit('handelAudDeFile',this.audioFile);
            }
        },
        keepHideText(){
            if(this.title==="请输入要隐写的文本："){
                this.$store.commit('handleAuEnText',this.srctext);
            }
        },
        encodeAud(){
            const xhr = new XMLHttpRequest();
            const formdata = new FormData();
            const aud = this.$refs.audWin;
            formdata.append('audio',this.$store.state.audioEnFile);
            formdata.append('text',this.$store.state.audioText);
            console.log(this.$store.state.audioText);
            xhr.open('POST', baseURL+'/eaudio');
            xhr.send(formdata);
            xhr.onreadystatechange = ()=> {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                const tres=JSON.parse(xhr.responseText);
                console.log(tres);
                var tbase = tres.audio.substring(2, tres.audio.length - 1);
                aud.src="data:audio/mp3;base64,"+tbase;
                var byteString = atob(tbase);
                var mimeString = "audio/mp3"; 
                var ab = new ArrayBuffer(byteString.length);
                var ia = new Uint8Array(ab);
                for (var i = 0; i < byteString.length; i++) {
                    ia[i] = byteString.charCodeAt(i);
                }
                var blob = new Blob([ab], { type: mimeString });
                var file = new File([blob], 'audio.mp3', {
                    type: 'audio/mp3',
                });
                this.$store.commit('handelAudDeFile',file);
            }};
            aud.onload=()=>{
                this.$store.commit('handelAudDeFile',aud.src);
            }
        },
        decodeAud(){
            const xhr = new XMLHttpRequest();
            const formdata = new FormData();
            formdata.append('audio',this.$store.state.audioDeFile);
            console.log(this.$store.state.audioEnFile);
            xhr.open('POST', baseURL+'/deaudio');
            xhr.send(formdata);
            xhr.onreadystatechange = ()=> {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                const cb = JSON.parse(xhr.responseText);
                this.srctext=cb.text;
            }}; 
        }
    },
    computed:{
        handlebtn(){
            if(this.btntitle==='上传音频'){
                return this.uploadImg;
            }
            else if(this.btntitle==='清除'){
                return this.clrText;
            }
            else if(this.title==='解码出的文本：'){
                return this.decodeAud;
            }
            return this.encodeAud;
        }
    }
}
</script>

<style scoped>
.duiqi{
    text-align: center;
}
.fx{
    object-fit: cover;
}

</style>