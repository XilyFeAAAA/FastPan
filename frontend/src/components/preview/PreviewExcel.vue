<template>
    <div v-html="excelContent" class="table-info"></div>
</template>
<script setup>
import * as XLSX from 'xlsx'
import { ref, onMounted, getCurrentInstance } from 'vue'
const props = defineProps({
    url: {
        type: String,
    },
})
const { proxy } = getCurrentInstance()
const excelContent = ref()
const initExcel = async () => {
    let res = await proxy.Request.get(props.url, {
        responseType: 'arraybuffer',
    })
    let workbook = XLSX.read(new Uint8Array(res.data), { type: 'array' })
    var worksheet = workbook.Sheets[workbook.SheetNames[0]]

    excelContent.value = XLSX.utils.sheet_to_html(worksheet)
}
onMounted(async () => {
    await initExcel()
})
</script>
<style lang="scss" scoped>
.table-info {
    width: 100%;
    padding: 10px;
    :deep table {
        width: 100%;
        border-collapse: collapse;
        td {
            border: 1px solid #ddd;
            border-collapse: collapse;
            padding: 5px;
            height: 30px;
            min-width: 50px;
        }
    }
}
</style>
