<template>
    <div ref="player" id="player"></div>
</template>
<script setup>
import Hls from 'hls.js'
import DPlayer from 'dplayer'
import { onMounted, ref, getCurrentInstance } from 'vue'
const props = defineProps({
    url: {
        type: String,
    },
})
const { proxy } = getCurrentInstance()
const player = ref()
const videoInfo = ref()
const initPlayer = () => {
    const dp = new DPlayer({
        element: player.value,
        theme: '#b7daff',
        screenshot: true,
        video: {
            url: `http://localhost:7070/api/v1${props.url}`,
            type: 'customHls',
            customType: {
                customHls: function (video, player) {
                    const hls = new Hls({
                        xhrSetup: function (xhr, url) {
                            xhr.setRequestHeader(
                                'Authorization',
                                'Bearer ' + proxy.VueCookies.get('token'),
                            )
                        },
                    })
                    hls.loadSource(video.src)
                    hls.attachMedia(video)
                },
            },
        },
    })
}
onMounted(() => {
    initPlayer()
})
</script>
<style lang="scss" scoped>
#player {
    width: 100%;
    :deep .dplayer-video-wrap {
        text-align: center;
        .dplayer-video {
            margin: 0px auto;
            max-height: calc(100vh - 40px);
        }
    }
}
</style>
