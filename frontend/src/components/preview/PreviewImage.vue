<template>
    <div>
        <div class="image-viewer"></div>
        <el-image-viewer
            :initial-index="previewImgIndex"
            hide-on-click-modal
            :url-list="imageList"
            @close="closeImgViewer"
            v-if="previewImgIndex != null"
        >
        </el-image-viewer>
    </div>
</template>
<script>
import { ref } from 'vue'
export default {
    props: {
        imageList: {
            type: Array,
        },
    },
    setup() {
        const previewImgIndex = ref()
        const show = (index) => {
            previewImgIndex.value = index
        }
        const closeImgViewer = () => {
            previewImgIndex.value = null
        }
        return {
            show,
            previewImgIndex,
            closeImgViewer,
        }
    },
}
</script>
