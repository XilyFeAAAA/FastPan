<template>
    <teleport to="body">
        <div class="window" v-if="show">
            <div class="window-mask" @click="close" v-if="show"></div>
            <div class="close flex-center" @click="close">
                <span>x</span>
            </div>
            <div
                class="window-content"
                :style="{
                    left: windowContentLeft + 'px',
                    width: windowContentWidth + 'px',
                }"
            >
                <div class="title">{{ title }}</div>
                <div
                    class="content-body"
                    :style="{ 'align-item': align, width: windowContentWidth + 'px' }"
                >
                    <slot></slot>
                </div>
            </div>
        </div>
    </teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
const props = defineProps({
    show: {
        type: Boolean,
    },
    width: {
        type: Number,
        default: 1000,
    },
    title: {
        type: String,
    },
    align: {
        type: String,
        default: 'top',
    },
})
const windowWidth = ref(window.innerWidth)
const windowContentWidth = computed(() => {
    return Math.min(props.width, windowWidth.value)
})
const windowContentLeft = computed(() => {
    let left = windowWidth.value - props.width
    return left < 0 ? 0 : left / 2
})

const emit = defineEmits(['close'])
const close = () => {
    emit('close')
}

const resizeWindow = () => {
    windowWidth.value = window.innerWidth
}

onMounted(() => {
    window.addEventListener('resize', resizeWindow)
})

onUnmounted(() => {
    window.removeEventListener('resize', resizeWindow)
})
</script>

<style lang="scss" scoped>
.window {
    .window-mask {
        position: fixed;
        top: 0px;
        left: 0px;
        width: 100%;
        height: 100vh;
        z-index: 200;
        opacity: 0.5;
        background-color: #000;
    }
    .close {
        position: absolute;
        z-index: 202;
        cursor: pointer;
        top: 40px;
        right: 40px;
        width: 44px;
        height: 44px;
        border-radius: 22px;
        background-color: #606266;
    }
    .window-content {
        position: absolute;
        top: 10vh;
        z-index: 201;
        background-color: #fff;
        .title {
            text-align: center;
            line-height: 40px;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
        }
        .content-body {
            height: calc(80vh);
            width: 100%;
            display: flex;
            overflow-y: auto;
        }
    }
}
</style>
