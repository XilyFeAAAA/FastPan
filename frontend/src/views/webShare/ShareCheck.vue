<template>
    <div class="share flex-center">
        <div class="container flex-center flex-column">
            <div class="header">
                <h1 class="title">FastPan网盘</h1>
            </div>
            <div class="content" v-if="exist">
                <div style="font-weight: bold">Your Share Link is Protected</div>
                <div class="tips">Please type the password to get shared content</div>
            </div>
            <div class="content" v-else>
                <div style="font-weight: bold">Your Share Link does not Exist</div>
            </div>
            <div class="footer flex-between" v-if="exist">
                <input type="text" class="public" v-model="code" />
                <button class="public" @click="checkShare">Submit ></button>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, getCurrentInstance } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const { proxy } = getCurrentInstance()
const route = useRoute()
const router = useRouter()
const code = ref()
const shareId = route.params.shareId
const exist = ref(false)
const api = {
    checkShare: '/share/checkShare',
    getShareInfo: '/share/getShareInfo',
}
const checkShare = async () => {
    const res = await proxy.Request.post(api.checkShare, {
        shareId: shareId,
        code: code.value,
    })
    if (!res.data.data.confirm) return
    router.push('/share/' + shareId)
}
const getShareInfo = async () => {
    const res = await proxy.Request.get(api.getShareInfo, {
        params: {
            shareId,
        },
    })
    if (!res) return
    if (res.data.data !== null) {
        exist.value = true
    }
}
getShareInfo()
</script>
<style lang="scss" scoped>
.share {
    height: 100vh;
    width: 100vw;
    background-color: #151515;
    color: #bec6cd;
    .container {
        transform: translateY(-10%);
        .header {
            font-size: 0.875rem;
        }
        .content {
            margin: 15px 0 50px;
            line-height: 1.2;
            font-size: 3rem;
            text-align: center;
            .tips {
                font-size: 1.6rem;
            }
        }
        .footer {
            width: 100%;
            .public {
                height: 50px;
                line-height: 50px;
                color: #fff;
            }
            input {
                width: 70%;
                border: 1px solid #619685;
            }
            button {
                width: 20%;
                font-size: 1rem;
                font-weight: bold;
                background-color: #151515;
                border: 2px solid #fff;
            }
        }
    }
}
</style>
