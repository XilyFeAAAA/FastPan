<template>
    <PreviewImage ref="imageViewRef" :imageList="[imageUrl]" />
    <Window
        :show="windowShow"
        @close="closeWindow"
        :width="fileInfo.file_type == 1 ? 1500 : 900"
        :title="fileInfo.file_name"
        :align="fileInfo.file_type == 1 ? 'center' : 'top'"
    >
        <PreviewVideo :url="url" v-if="fileInfo.file_type === 0"></PreviewVideo>
        <PreviewMusic
            :url="url"
            :fileName="fileInfo.file_name"
            v-else-if="fileInfo.file_type === 1"
        ></PreviewMusic>
        <PreviewPdf :url="url" v-else-if="fileInfo.file_type === 3"></PreviewPdf>
        <PreviewDoc :url="url" v-else-if="fileInfo.file_type === 4"></PreviewDoc>
        <PreviewExcel :url="url" v-else-if="fileInfo.file_type === 5"></PreviewExcel>
        <PreviewTxt
            :url="url"
            v-else-if="fileInfo.file_type === 6 || fileInfo.file_type === 7"
        ></PreviewTxt>
        <PreviewDownload
            :createDownloadUrl="createDownloadUrl"
            :downloadUrl="downloadUrl"
            :fileInfo="fileInfo"
            v-else
        ></PreviewDownload>
    </Window>
</template>

<script>
import { nextTick, ref, computed } from 'vue'
import PreviewImage from './PreviewImage.vue'
import Window from '@/components/Window.vue'
import PreviewDoc from './PreviewDoc.vue'
import PreviewVideo from './PreviewVideo.vue'
import PreviewExcel from './PreviewExcel.vue'
import PreviewPdf from './PreviewPdf.vue'
import PreviewTxt from './PreviewTxt.vue'
import PreviewMusic from './PreviewMusic.vue'
import PreviewDownload from './PreviewDownload.vue'
const FILE_URL_MAP = {
    0: {
        fileUrl: '/file/getFile',
        videoUrl: '/file/ts/getVideo',
        createDownloadUrl: '/file/createDownloadUrl',
        downloadUrl: 'http://localhost:7070/api/v1/file/download',
    },
}
export default {
    components: {
        PreviewImage,
        Window,
        PreviewVideo,
        PreviewDoc,
        PreviewExcel,
        PreviewPdf,
        PreviewTxt,
        PreviewMusic,
        PreviewDownload,
    },
    setup() {
        const createDownloadUrl = ref(null)
        const downloadUrl = ref(null)
        const imageUrl = computed(() => {
            if (fileInfo.value.file_cover != null)
                return (
                    'http://localhost:7070/api/v1/file/getCover/' +
                    fileInfo.value.file_cover.replace('_.', '.')
                )
            else return ''
        })
        const url = ref(null)
        const imageViewRef = ref()
        const fileInfo = ref({})
        const showPreview = (data, showPart) => {
            fileInfo.value = data
            if (data.file_category == 3) {
                nextTick(() => {
                    imageViewRef.value.show(0)
                })
            } else {
                windowShow.value = true
                let _url = FILE_URL_MAP[showPart].fileUrl
                let _createDownloadUrl = FILE_URL_MAP[showPart].createDownloadUrl
                let _downloadUrl = FILE_URL_MAP[showPart].downloadUrl
                if (data.file_category === 1) {
                    _url = FILE_URL_MAP[showPart].videoUrl
                }
                if (showPart === 0) {
                    _url = _url + '/' + fileInfo.value.file_id
                    _createDownloadUrl = _createDownloadUrl + '/' + fileInfo.value.file_id
                }
                url.value = _url
                createDownloadUrl.value = _createDownloadUrl
                downloadUrl.value = _downloadUrl
            }
        }
        const windowShow = ref(false)
        const closeWindow = () => {
            windowShow.value = false
        }
        return {
            imageUrl,
            fileInfo,
            showPreview,
            imageViewRef,
            closeWindow,
            windowShow,
            url,
            createDownloadUrl,
            downloadUrl,
        }
    },
}
</script>

<style lang="scss" scoped></style>
