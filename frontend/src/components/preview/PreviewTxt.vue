<template>
    <div class="code">
        <div class="top-op flex-around">
            <div class="encode-select flex-start">
                <select placeholder="选择编码" v-modle="encode" @change="changeEncode">
                    <option value="utf-8">UTF-8编码</option>
                    <option value="gbk">GBK编码</option>
                </select>
            </div>
            <div class="copy-btn">
                <button @click="copy">复制</button>
            </div>
        </div>
        <highlightjs autodetect :code="txtContent"></highlightjs>
    </div>
</template>
<script setup>
import useClipboard from 'vue-clipboard3'
import { ref, onMounted, getCurrentInstance } from 'vue'
const props = defineProps({
    url: {
        type: String,
    },
})
const { toClipboard } = useClipboard()
const { proxy } = getCurrentInstance()
const codeRef = ref()
const txtContent = ref('')
const blobResult = ref()
const encode = ref('utf8')
const readTxt = async () => {
    let res = await proxy.Request.get(props.url, {
        responseType: 'blob',
    })
    if (!res) return
    blobResult.value = res.data
    debugger
    showTxt()
}

const changeEncode = (e) => {
    encode.value = e
    showTxt()
}

const showTxt = () => {
    const reader = new FileReader()
    reader.onload = () => {
        let txt = reader.result
        txtContent.value = txt
    }
    reader.readAsText(blobResult.value, encode.value)
}

const copy = async () => {
    await toClipboard(txtContent.value)
    alert('复制成功')
}

onMounted(async () => {
    debugger
    await readTxt()
})
</script>
<style lang="scss" scoped>
.code {
    width: 100%;
    .encode-select {
        flex: 1;
        margin: 5px 10px;
        select {
            font-size: 0.875rem;
            height: 40px;
            line-height: 1.25rem;
            text-rendering: auto;
            width: 200px;
            border-radius: 5px;
            border: 1px solid #eaeaea;
            background: #fff;
            color: #000;
            padding: 0 12px;
            cursor: pointer;
        }
    }
    .copy-btn {
        margin-right: 10px;
        button {
            width: 100px;
        }
    }
    pre {
        margin: 0;
    }
}
</style>
