<template>
    <div ref="docRef" class="doc-content"></div>
</template>
<script setup>
import * as docx from 'docx-preview'
import { ref, getCurrentInstance, onMounted } from 'vue'
const { proxy } = getCurrentInstance()
const props = defineProps({
    url: {
        type: String,
    },
})
const docRef = ref()
const initDoc = async () => {
    let res = await proxy.Request.get(props.url, {
        responseType: 'blob',
    })
    docx.renderAsync(res.data, docRef.value)
}
onMounted(async () => {
    await initDoc()
})
</script>
<style lang="scss" scoped>
.doc-content {
    margin: 0px auto;
    :deep .docx-wrapper {
        background-color: #fff;
        padding: 10px 0px;
    }
    :deep .docx-wrapper > section.docx {
        margin-bottom: 0px;
    }
}
</style>
