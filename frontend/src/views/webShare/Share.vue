<template>
    <div></div>
</template>
<script setup>
import { ref, getCurrentInstance } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const { proxy } = getCurrentInstance()
const route = useRoute()
const router = useRouter()
const shareInfo = ref()
const shareId = route.params.shareId
const api = {
    getShareInfo: '/share/getShareInfo',
}
const getShareInfo = async () => {
    const res = await proxy.Request.get(api.getShareInfo, {
        params: {
            shareId,
        },
    })
    if (!res) return
    if (res.data.data === null) {
        router.push(`/shareCheck/${shareId}`)
        return
    }
    shareInfo.value = res.data.data.shareInfo
}
getShareInfo()
</script>
<style lang="scss" scoped></style>
