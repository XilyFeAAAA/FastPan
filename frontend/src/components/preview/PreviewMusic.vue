<template>
    <div class="music flex-center">
        <div class="body-content">
            <div class="cover">
                <!-- <img src="@/assets/music_cover.png" alt="" /> -->
            </div>
            <div class="music-player" ref="musicRef"></div>
        </div>
    </div>
</template>
<script setup>
import APlayer from 'aplayer'
import 'aplayer/dist/aplayer.min.css'
import { onMounted, onUnmounted, ref, getCurrentInstance } from 'vue'
const props = defineProps({
    url: {
        type: String,
    },
    fileName: {
        type: String,
    },
})
const { proxy } = getCurrentInstance()
const musicRef = ref()
const player = ref()

onMounted(async () => {
    const res = await proxy.Request.get(props.url, {
        responseType: 'blob',
    })
    const musicUrl = URL.createObjectURL(res.data)
    player.value = new APlayer({
        container: musicRef.value,
        audio: {
            url: musicUrl,
            name: props.fileName,
            // cover: new URL('@/assets/music_cover.png', import.meta.url),
        },
    })
})

onUnmounted(() => {
    player.value.destroy()
})
</script>
<style lang="scss" scoped>
.music {
    width: 100%;
    .body-content {
        text-align: center;
        width: 80%;
        .cover {
            margin: 0px auto;
            width: 200px;
            text-align: center;
            img {
                width: 100%;
            }
        }
        .music-player {
            margin-top: 20px;
        }
    }
}
</style>
