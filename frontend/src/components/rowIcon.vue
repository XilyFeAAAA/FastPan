<template>
    <div class="icon flex-center">
        <!-- 文件夹图标 -->
        <font-awesome-icon
            v-if="props.folder_type === 1"
            :icon="['far', 'folder']"
            class="fa"
            size="xl"
        />
        <!-- 如果是文件则判断类型，有封面并且转码好的去请求api -->
        <!-- 转码好的视频图片图标 -->
        <img
            v-else-if="(props.file_type === 0 || props.file_type === 2) && props.status == 3"
            :src="'http://localhost:7070/api/v1/file/getCover/' + cover"
        />
        <!-- 其他默认类型文件封面 -->
        <!-- 视频默认icon -->
        <font-awesome-icon
            v-else-if="props.file_type === 0"
            icon="file-video"
            class="fa"
            size="xl"
        />
        <!-- 音乐默认icon -->
        <span v-else-if="props.file_type === 1" class="fa flex-center">
            <svg
                t="1687505461940"
                class="icon"
                viewBox="0 0 1024 1024"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                p-id="1805"
                :width="props.width"
                :height="props.width"
            >
                <path
                    d="M554.666667 384h234.666666L554.666667 149.333333V384M256 85.333333h341.333333l256 256v512a85.333333 85.333333 0 0 1-85.333333 85.333334H256a85.333333 85.333333 0 0 1-85.333333-85.333334V170.666667c0-47.36 37.973333-85.333333 85.333333-85.333334m128 597.333334a85.333333 85.333333 0 0 0-85.333333 85.333333 85.333333 85.333333 0 0 0 85.333333 85.333333 85.333333 85.333333 0 0 0 85.333333-85.333333v-213.333333h128v-85.333334h-170.666666v224.853334c-12.373333-7.253333-27.306667-11.52-42.666667-11.52z"
                    fill="#666666"
                    p-id="1806"
                ></path></svg
        ></span>

        <!-- 图片默认icon -->
        <font-awesome-icon
            v-else-if="props.file_type === 2"
            icon="file-image"
            class="fa"
            size="xl"
        />
        <!-- pdf默认icon -->
        <font-awesome-icon v-else-if="props.file_type === 3" icon="file-pdf" class="fa" size="xl" />
        <!-- word默认icon -->
        <font-awesome-icon
            v-else-if="props.file_type === 4"
            icon="file-word"
            class="fa"
            size="xl"
        />
        <!-- excel默认icon -->
        <font-awesome-icon
            v-else-if="props.file_type === 5"
            icon="file-excel"
            class="fa"
            size="xl"
        />
        <!-- 压缩包默认icon -->
        <span v-else-if="props.file_type === 8" class="fa flex-center">
            <svg
                t="1687430842836"
                class="icon"
                viewBox="0 0 1024 1024"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                p-id="2976"
                :width="props.width"
                :height="props.width"
            >
                <path
                    d="M582.294588 0H120.470588v1024h783.058824V319.728941L582.294588 0zM602.352941 104.929882L799.503059 301.176471H602.352941V104.929882zM180.705882 963.764706V60.235294h180.705883v60.235294h60.235294V60.235294h120.470588v301.176471h301.176471v602.352941H180.705882z m120.470589-481.882353h60.235294v60.235294H301.176471V481.882353z m60.235294 0V421.647059h60.235294v60.235294H361.411765z m0-120.470588V301.176471h60.235294v60.235294H361.411765zM301.176471 361.411765h60.235294v60.235294H301.176471V361.411765z m0-120.470589h60.235294v60.235295H301.176471V240.941176z m60.235294 0V180.705882h60.235294v60.235294H361.411765zM301.176471 120.470588h60.235294v60.235294H301.176471V120.470588z m60.235294 445.078588c-66.439529 0-120.470588 54.031059-120.470589 120.470589s54.031059 120.470588 120.470589 120.470588c3.734588 0 7.288471-0.421647 13.191529-1.204706a120.289882 120.289882 0 0 0 92.220235-61.801412c9.999059-18.251294 15.058824-37.586824 15.058824-57.46447 0-66.439529-54.031059-120.470588-120.470588-120.470589z m52.585411 149.082353a59.873882 59.873882 0 0 1-45.899294 30.840471l-6.746353 0.843294a60.235294 60.235294 0 0 1 0.060236-120.470588c33.189647 0 60.235294 27.045647 60.235294 60.235294a59.753412 59.753412 0 0 1-7.649883 28.551529z"
                    p-id="2977"
                ></path>
            </svg>
        </span>
        <font-awesome-icon v-else icon="file" class="fa" size="xl" />
    </div>
</template>
<script setup>
import { defineProps } from 'vue'
const props = defineProps({
    width: String,
    folder_type: Number,
    file_type: Number,
    status: Number,
    cover: String,
})
</script>
<style lang="scss" scoped>
.icon {
    position: relative;
    overflow: hidden;
    img {
        height: 80%;
        width: 80%;
        object-fit: cover;
    }
}
</style>
