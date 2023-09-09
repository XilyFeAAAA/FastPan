<template>
    <div class="others flex-center">
        <div class="body-content flex-center flex-column">
            <div>
                <rowIcon
                    width="80"
                    :folder_type="fileInfo.folder_type"
                    :file_type="fileInfo.file_type"
                    :status="fileInfo.status"
                    :cover="fileInfo.file_cover"
                />
                <div class="file-name">{{ fileInfo.file_name }}</div>
                <div class="tips">该类型文件不支持预览，请下载后查看</div>
                <div class="download-btn flex-center">
                    <button @click="download">
                        点击下载 {{ proxy.Utils.sizeToStr(fileInfo.file_size) }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue'
import rowIcon from '@/components/rowIcon.vue'
const props = defineProps({
    createDownloadUrl: {
        type: String,
    },
    downloadUrl: {
        type: String,
    },
    fileInfo: {
        type: Object,
    },
})
const { proxy } = getCurrentInstance()
const download = async () => {
    const res = await proxy.Request.get(props.createDownloadUrl)
    if (!res) return
    window.location.href = props.downloadUrl + '/' + res.data.data.code
}
</script>
<style lang="scss" scoped>
.others {
    width: 100%;
    .body-content {
        text-align: center;
    }
}
</style>
