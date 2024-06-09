<template>
  <div class="card mt-4">
    <div class="card-header pb-0 p-3">
      <div class="row">
        <div class="col-6 d-flex align-items-center">
          <h6 class="mb-0">{{ title }}</h6>
        </div>
        <div class="col-6 text-end">
          <soft-button @click="clrText" color="dark" variant="gradient">
            清除
          </soft-button>
        </div>
      </div>
    </div>
    <div class="card-body p-3">
      <div class="row">
        <div class="container">
            <div class="form-group">
                <textarea @change="keepHideText" class="form-control" v-model="srctext" id="FormControlTextarea1" rows="8"></textarea>
            </div>
        </div>
        <div class="col-6 text-end">
          <soft-button v-show="(btntitle==='清除'?false:true)&&(title==='隐写后的文本：')" @click="encodeStr" color="dark" variant="gradient">
            获取
          </soft-button>
          <soft-button v-show="(btntitle==='清除'?false:true)&&(title==='被隐写的文本：')" @click="decodeStr" color="dark" variant="gradient">
            获取
          </soft-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SoftButton from "@/components/SoftButton.vue";

export default {
  name: "TextEdit",
  components: {
    SoftButton,
  },
  data() {
    return {
      srctext:'',
      cipherText:[],
      hiddenText:'',
      decodeText:''
    };
  },
  methods:{
    clrText(){
      this.srctext='';
    },
    keepHideText(){
      if(this.title==="请输入隐写文本："){
        this.$store.commit('handelHideText',this.srctext);
      }
      else if(this.title==="请输入载体文本："){
        this.$store.commit('handelSrcText',this.srctext);
      }
      else if(this.title==="请输入解码文本："){
        this.$store.commit('handelDecoText',this.srctext);
      }
    },
    encodeStr() {
      this.hiddenText=this.$store.state.hideText;
        this.cipherText = this.$store.state.tohideText.split("");
        this.cipherText.splice(
            parseInt(Math.random() * (this.$store.state.tohideText.length + 1)),
            0,
            this.hiddenText
                .split("")
                .map((char) => char.codePointAt(0).toString(2))
                .join(" ")
                .split("")
                .map((binaryNum) => {
                    if (binaryNum === "1") {
                        return String.fromCharCode(8203); // 零宽空格符&#8203;
                    } else if (binaryNum === "0") {
                        return String.fromCharCode(8204); // 零宽不连字符&#8204;
                    } else {
                        return String.fromCharCode(8205); //空格 -> 零宽连字符&#8205;
                    }
                })
                .join(String.fromCharCode(8206))
        );
        this.cipherText = this.cipherText.join("");
        this.srctext=this.cipherText;
        console.log(this.cipherText, "cipherText");
        navigator.clipboard.writeText(this.srctext);
    },
    decodeStr() {
        if (!this.$store.state.decoText) {
            this.decodeText = "";
            return;
        }
        let text = this.$store.state.decoText.replace(/[\u200b-\u200f\uFEFF\u202a-\u202e]/g, "");
        let hiddenText = this.$store.state.decoText.replace(/[^\u200b-\u200f\uFEFF\u202a-\u202e]/g, "");
        console.log(text, "text");
        console.log(hiddenText, "hiddenText");
        this.decodeText = hiddenText
            .split("‎")
            .map((char) => {
                if (char === "​" /* 不是空字符串,是&#8203; */) {
                    return "1";
                } else if (char === "‌" /*  不是空字符串,是&#8204; */) {
                    return "0";
                } else {
                    return " ";
                }
            })
            .join("")
            .split(" ")
            .map((binaryNum) => String.fromCharCode(parseInt(binaryNum, 2)))
            .join("");
        this.srctext = this.decodeText;
        navigator.clipboard.writeText(this.srctext);
    },
  },
  props:{
    title:String,
    btntitle:String,
  },
};
</script>

<style scoped>

</style>