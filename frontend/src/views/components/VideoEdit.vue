<template>
 <div class="card mt-4">
    <div class="card-header pb-0 p-3">
      <div class="row">
        <div class="col-6 d-flex align-items-center">
          <h6 class="mb-0">{{ title }}</h6>
        </div>
        <div class="col-6 text-end">
          <input type="file" ref="upload2" @change="viewVideo2" style="display:none;"/>
          <soft-button ref="leftbtn" :style="'visibility:'+(title==='隐写后的视频：'?'visible':'hidden')" @click="uploadImg2" color="dark" variant="gradient">
            上传
          </soft-button>
        </div>
      </div>
    </div>
    <div class="card-body p-3">
      <div class="row">
        <div class="container duiqi">
            <div class="form-group">
                <video :src="videoURL" class="vcc" ref="vidWin" v-show="flag==='文字'?false:true" controls></video>
                <textarea v-show="flag==='文字'?true:false" @change="keepHideText" class="form-control" v-model="srctext" id="FormControlTextarea1" rows="5"></textarea>
            </div>
        </div>
        <div class="col-12 duiqi">
            <input type="file" ref="upload" @change="viewVideo" style="display:none;"/>
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

export default {
    name:'VideoEdit',
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
            videoURL:'',
            srctext:'',
            videoFile:null,
            videoEnText:'',
            videoDeText:'',
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
        viewVideo(e){
            const file = e.target.files[0];
            this.videoFile=file
            const reader = new FileReader();
            reader.onload = (e) => {
                this.videoURL = e.target.result; 
            };
            reader.readAsDataURL(file);
            if(this.title==='上传隐写视频：'){
                this.$store.commit('handelVideoFile',this.videoFile);
            }
        },
        viewVideo2(e){
            const file = e.target.files[0];
            this.videoFile=file;
            const reader = new FileReader();
            reader.onload = (e) => {
                this.videoURL = e.target.result; 
            };
            reader.readAsDataURL(file);
            this.$store.commit('handleVidURL',this.videoURL);
            if(this.title==="隐写后的视频："){
                this.$store.commit('handelVideoDeFile',this.videoFile);
            }
        },
        keepHideText(){
            if(this.title==="请输入要隐写的文本："){
                this.$store.commit('handleViEnText',this.srctext);
            }
        },
        b64toBlob(b64Data, contentType = '', sliceSize = 512) {
            const byteCharacters = atob(b64Data);
            const byteArrays = [];
            
            for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
                const slice = byteCharacters.slice(offset, offset + sliceSize);
                
                const byteNumbers = new Array(slice.length);
                for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
                }
                
                const byteArray = new Uint8Array(byteNumbers);
                byteArrays.push(byteArray);
            }
            
            return new Blob(byteArrays, { type: contentType });
        },
        stringToBytes(str) {
            const encoder = new TextEncoder();
            const encodedArray = encoder.encode(str);
            return encodedArray;
        },
        bytesToNumberString(bytes) {
            let numberString = "";
            for (let i = 0; i < bytes.length; i++) {
                numberString += bytes[i].toString().padStart(3, "0");
            }
            return numberString;
        },
        numberStringToBytes(numberString) {
            const bytes = [];
            for (let i = 0; i < numberString.length; i += 3) {
                const byteString = numberString.slice(i, i + 3);
                const byte = parseInt(byteString, 10);
                bytes.push(byte);
            }
            return new Uint8Array(bytes);
        },
        bytesToString(bytes) {
            const decoder = new TextDecoder();
            const decodedString = decoder.decode(bytes);
            return decodedString;
        },
        encodeVid(){
            const xhr = new XMLHttpRequest();
            const formdata = new FormData();
            const aud = this.$refs.vidWin;
            formdata.append('video',this.$store.state.videoFile);
            formdata.append('text',this.$store.state.videoText);
            console.log(this.$store.state.videoFile);
            console.log(this.$store.state.videoText);
            xhr.open('POST', 'http://127.0.0.1:4001/evideo');
            xhr.send(formdata);
            xhr.onreadystatechange = ()=> {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                const tres=JSON.parse(xhr.responseText);
                var tbase = tres.video;
                const blob = this.b64toBlob(tbase, 'video/mp4');
                const file = new File([blob], "filename.mp4", { type: 'video/mp4' });
                this.$store.commit('handelVideoDeFile',file);
                const blobUrl = URL.createObjectURL(blob);
                aud.src = blobUrl;
            }};
            aud.onload=()=>{
                this.$store.commit('handleVidURL',aud.src);
            }
        },
        decodeVid(){
            const xhr = new XMLHttpRequest();
            const formdata = new FormData();
            formdata.append('video',this.$store.state.videoDeFile);
            console.log(this.$store.state.videoDeFile);
            xhr.open('POST', 'http://127.0.0.1:4001/devideo');
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
            if(this.btntitle==='上传视频'){
                return this.uploadImg;
            }
            else if(this.btntitle==='清除'){
                return this.clrText;
            }
            else if(this.title==='解码出的文本：'){
                return this.decodeVid;
            }
            return this.encodeVid;
        }
    }
}
</script>

<style scoped>
.duiqi{
    text-align: center;
    height: auto;
}
.fx{
    object-fit: cover;
}
.vcc{
    width: 500px;
    height: 330px;
    object-fit: fill;
}
.duiqi .vcc {
  max-width: 100%; /* Ensures the video does not exceed the width of its container */
  height: auto;    /* Maintains the aspect ratio of the video */
}

.form-group {
  overflow: hidden; /* Helps prevent layout overflow issues */
}
</style>