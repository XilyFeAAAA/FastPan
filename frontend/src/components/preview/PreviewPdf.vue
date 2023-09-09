<template>
    <div class="pdf">
        <vue-pdf-embed
            ref="pdfRef"
            class="vue-pdf-embed"
            :source="state.url"
            width="850"
            :page="state.pageNum"
            :headers="state.header"
        ></vue-pdf-embed>
    </div>
</template>
<script setup>
import VuePdfEmbed from 'vue-pdf-embed'
import { ref, onMounted, getCurrentInstance } from 'vue'
const props = defineProps({
    url: {
        type: String,
    },
})
const { proxy } = getCurrentInstance()
const pdfRef = ref()
const state = ref({
    url: '',
    pageNum: 0,
    numPages: 0,
    header: {
        Authorization: `Bearer ${proxy.VueCookies.get('token')}`,
    },
})
const initExcel = async () => {
    let res = await proxy.Request.get(props.url, {
        responseType: 'arraybuffer',
    })
    state.value.url = new Uint8Array(res.data)
}
onMounted(async () => {
    await initExcel()
})
</script>
<style lang="scss" scoped>
.pdf {
    width: 100%;
}
</style>
