<template>
    <Dialog :config="dialogConfig4FileShare">
        <div class="share-body">
            <div class="line flex-start"><span>文件</span>{{ currentFile.file_name }}</div>
            <div class="line flex-start">
                <span>有效期</span>
                <div class="radios flex-center">
                    <label class="flex-center">
                        <input type="radio" value="1" v-model="valid_type" />
                        1天
                    </label>

                    <label class="flex-center">
                        <input type="radio" value="7" v-model="valid_type" />
                        7天
                    </label>

                    <label class="flex-center">
                        <input type="radio" value="30" v-model="valid_type" />
                        30天
                    </label>
                    <label class="flex-center">
                        <input type="radio" value="0" v-model="valid_type" />
                        永久有效
                    </label>
                </div>
            </div>
            <div class="line flex-start">
                <span>提取码</span>
                <div class="radios flex-center">
                    <label class="flex-center">
                        <input type="radio" value="customize" v-model="autoGenerate" />
                        自定义
                    </label>
                    <label class="flex-center">
                        <input type="radio" value="system" v-model="autoGenerate" />
                        系统生成
                    </label>
                </div>
            </div>
            <div class="line flex-center code" v-show="autoGenerate === 'customize'">
                <Input
                    type="text"
                    name="password"
                    placeholder="输入5位验证码"
                    :value="code"
                    :rule="codeRule"
                    @update="updateCode"
                />
            </div>
        </div>
    </Dialog>
</template>
<script setup>
/*TODO:
1. 优化 分享界面 见qq
2. 提取码可以为空
3. 外部分享页面
*/
import useClipboard from 'vue-clipboard3'
const { toClipboard } = useClipboard()
import Swal from 'sweetalert2'
import Dialog from '@/components/Dialog.vue'
import Input from '@/components/Input.vue'
import { ref, getCurrentInstance, defineEmits } from 'vue'
const { proxy } = getCurrentInstance()
const api = {
    createShareUrl: '/share/shareFile',
}
const valid_type = ref(1)
const autoGenerate = ref('customize')
const currentFile = ref()
const code = ref()
const shareUrl = ref()
const dialogConfig4FileShare = ref({
    title: '文件分享',
    width: '500px',
    visible: false,
    showCancel: true,
    buttons: [
        {
            title: '确定',
            async func() {
                if (autoGenerate.value === 'system') {
                    debugger
                    code.value = proxy.Utils.generateRandomString(5)
                }
                const res = await proxy.Request.post(api.createShareUrl, {
                    fileId: currentFile.value.file_id,
                    valid_type: valid_type.value,
                    code: code.value,
                })
                if (!res) return
                shareUrl.value = res.data.data.shareUrl
                Swal.fire({
                    title: '分享',
                    html:
                        '<div class="line">' +
                        '<span>分享链接</span>' +
                        shareUrl.value +
                        '</div>' +
                        '<div class="line">' +
                        '<span>提取码</span>' +
                        code.value +
                        '</div>',
                    showCloseButton: true,
                    focusConfirm: false,
                }).then(async (result) => {
                    if (result.isConfirmed) {
                        await toClipboard(`链接:${shareUrl.value} 提取码:${code.value}`)
                    }
                })
            },
        },
    ],
    show() {
        this.visible = true
    },
    close() {
        this.visible = false
    },
})
const codeRule = {
    required: true,
    minLength: 5,
    maxLength: 5,
}
const showFileShareDialog = (file) => {
    currentFile.value = file
    dialogConfig4FileShare.value.show()
}
const updateCode = (data) => {
    const { value } = data
    code.value = value
}
defineExpose({
    showFileShareDialog,
})
</script>

<style lang="scss" scoped>
.share-body {
    .line {
        span {
            width: 60px;
            text-align: right;
            margin: 0 10px;
        }
        &.code {
            width: 60%;
            margin: 5px auto 0;
        }
    }
    label {
        margin-right: 10px;
        input {
            margin-right: 5px;
        }
    }
}
</style>
