<template>
 <div class="card mt-4">
    <div class="card-header pb-0 p-3">
      <div class="row">
        <div class="col-6 d-flex align-items-center">
          <h6 class="mb-0">{{ title }}</h6>
        </div>
        <div class="col-6 text-end">
          <input type="file" ref="upload2" @change="viewImg2" style="display:none;"/>
          <soft-button ref="leftbtn" :style="'visibility:'+(title==='隐写后的图片：'?'visible':'hidden')" @click="uploadImg2" color="dark" variant="gradient">
            上传
          </soft-button>
        </div>
      </div>
    </div>
    <div class="card-body p-3">
      <div class="row">
        <div class="container duiqi">
            <div class="form-group">
                <div class="img-fluid fx">
                    <img v-show="flag==='文字'?false:true" :src="imageURL" ref="imgWin" alt="" width="500" height="500">
                </div>
                <textarea v-show="flag==='文字'?true:false" @change="keepHideText" class="form-control" v-model="srctext" id="FormControlTextarea1" rows="8"></textarea>
            </div>
        </div>
        <div class="col-12 duiqi">
            <input type="file" ref="upload" @change="viewImg" style="display:none;"/>
            <soft-button @click="handlebtn" color="dark" variant="gradient">
            {{ btntitle }}
            </soft-button>
            <soft-button style="margin-left:10px;" v-show="title==='隐写后的图片：'?true:false" @click="download" color="dark" variant="gradient">
            下载
            </soft-button>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>
import SoftButton from "@/components/SoftButton.vue";
import baseURL from "@/config/config.js";
import axios from "axios";

export default {
    name:'ImageEdit',
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
            imageURL:'https://via.placeholder.com/500/808080',
            srctext:'',
            imgFile:null,
            imageEnText:'',
            imageDeText:'',
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
        viewImg(e){
            const file = e.target.files[0];
            this.imgFile=file
            const reader = new FileReader();
            reader.onload = (e) => {
                this.imageURL = 'data:image/png;base64,'+e.target.result.split(',')[1]; 
            };
            reader.readAsDataURL(file);
            if(this.title==="请上传要隐写的图片："){
                this.$store.commit('handleImgFile',this.imgFile);
            }
        },
        viewImg2(e){
            const file = e.target.files[0];
            this.imgFile=file;
            const reader = new FileReader();
            reader.onload = (e) => {
                this.imageURL = e.target.result; 
            };
            reader.readAsDataURL(file);
            this.$store.commit('handleImgURL',this.imageURL);
            if(this.title==="隐写后的图片："){
                this.$store.commit('handleImgDeFile',this.imgFile);
            }
        },
        keepHideText(){
            if(this.title==="请输入要隐写的文字："){
                this.$store.commit('handleImgEnText',this.srctext);
            }
        },
        download(){
            var base64String = this.$store.state.imgDeurl;
            var byteString = atob(base64String.split(',')[1]);
            var mimeString = base64String.split(',')[0].split(':')[1].split(';')[0];
            var ab = new ArrayBuffer(byteString.length);
            var ia = new Uint8Array(ab);
            for (var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            var blob = new Blob([ab], { type: mimeString });
            var downloadLink = document.createElement('a');
            downloadLink.href = URL.createObjectURL(blob);
            downloadLink.download = 'encoded_image.png'; 
            document.body.appendChild(downloadLink);
            downloadLink.click(); 
            document.body.removeChild(downloadLink); 
        },
        base64ToBlob(base64){
            var byteString = atob(base64);
            var mimeString = "image/jpeg"; // 设置图片类型，这里假设为 JPEG
            var ab = new ArrayBuffer(byteString.length);
            var ia = new Uint8Array(ab);
            for (var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            return new Blob([ab], { type: mimeString });
        },
        encodeImg(){
            const xhr = new XMLHttpRequest();
            const formdata = new FormData();
            const img = this.$refs.imgWin;
            formdata.append('image',this.$store.state.imgEnFile);
            formdata.append('text',this.$store.state.imgenText);
            xhr.open('POST', baseURL+'/encrypt');
            xhr.send(formdata);
            xhr.onreadystatechange = ()=> {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                const tres=JSON.parse(xhr.responseText);
                var tbase = tres.img.substring(2, tres.img.length - 1);
                img.src = "data:image/jpeg;base64," + tbase;
                var byteString = atob(tbase);
                var mimeString = "image/jpeg"; // 设置图片类型，这里假设为 JPEG
                var ab = new ArrayBuffer(byteString.length);
                var ia = new Uint8Array(ab);
                for (var i = 0; i < byteString.length; i++) {
                    ia[i] = byteString.charCodeAt(i);
                }
                var blob = new Blob([ab], { type: mimeString });
                var file = new File([blob], 'image.jpg', {
                    type: 'image/jpeg',
                });
                this.$store.commit('handleImgDeFile',file);
            }};
            img.onload=()=>{
                this.$store.commit('handleImgURL',img.src);
            }
        },
        decodeImg(){
            const xhr = new XMLHttpRequest();
            const formdata = new FormData();
            console.log(this.$store.state.imgDeFile);
            formdata.append('image',this.$store.state.imgDeFile);
            console.log(this.$store.state.imgDeFile);
            xhr.open('POST', baseURL+'/decoimg');
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
            if(this.btntitle==='上传图片'){
                return this.uploadImg;
            }
            else if(this.btntitle==='清除'){
                return this.clrText;
            }
            else if(this.title==='解码出的文字：'){
                return this.decodeImg;
            }
            return this.encodeImg;
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
.duiqi .img-fluid {
  max-width: 100%; /* 确保图片不会超出其容器宽度 */
  height: auto;    /* 保持图片的原始宽高比 */
}

.form-group {
  overflow: hidden; /* 添加这个可以避免某些布局问题 */
}
</style>