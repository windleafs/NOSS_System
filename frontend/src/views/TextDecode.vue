<template>
    <div class="container-fluid mt-4">
        <div class="row">
            <div class="col-md-12">
                <text-edit title="请输入解码文本："  btntitle="清除"/>
            </div>
            <div class="col-md-12">
                <text-edit title="被隐写的文本：" btntitle="获取"/>
            </div>
        </div>
    </div>
</template>

<script>
import TextEdit from './components/TextEdit.vue';

export default {
    name:'TextEncode',
    components:{
        TextEdit
    }
}
</script>

<style>

</style>