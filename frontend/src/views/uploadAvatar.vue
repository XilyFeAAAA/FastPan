<script>
import Swal from 'sweetalert2'
import axios from 'axios'
import { ref } from 'vue'
import Request from '../utils/Request.js'
const api = '/uploadAvatar'
export default {
    props: {
        avatar_url: String,
    },
    setup(props) {
        const avatarFile = ref(null)
        const imgStr = ref(props.avatar_url)
        const showUploadAvatarDialog = () => {
            Swal.fire({
                title: '上传新头像',
                html:
                    '<div class="avatar">' +
                    '<input id="my-input" type="file" accept="image/*" >' +
                    `<img  src="${imgStr.value}"` +
                    '</div>',
                customClass: { htmlContainer: 'my-dialog-html-container-class' },
                showCancelButton: true,
                reverseButtons: true,
                confirmButtonText: '上传',
                didOpen: () => {
                    document.getElementById('my-input').addEventListener('change', onchangeImgFun)
                },
                preConfirm: async () => {
                    if (!avatarFile.value) {
                        Swal.showValidationMessage('请选择头像文件')
                        return false
                    }
                    const formData = new FormData()
                    formData.append('file', avatarFile.value)
                    const res = await Request.post(api, formData)
                    if (!res) Swal.showValidationMessage('上传头像失败')
                    else
                        Swal.fire({
                            toast: true,
                            position: 'top-end',
                            showConfirmButton: false,
                            timer: 4000,
                            type: 'success',
                            title: 'Upload avatar successfully',
                        })
                },
            })
        }

        const onchangeImgFun = (e) => {
            let file = e.target.files[0]
            // 获取图片的大小，做大小限制有用
            let imgSize = file.size
            // 比如上传头像限制5M大小，这里获取的大小单位是b
            if (imgSize <= 5 * 1024 * 1024) {
                // 开始渲染选择的图片
                var reader = new FileReader()
                reader.readAsDataURL(file) // 读出 base64
                reader.onloadend = function () {
                    // 图片的 base64 格式, 可以直接当成 img 的 src 属性值
                    var dataURL = reader.result
                    avatarFile.value = file
                    document.querySelector('.avatar img').setAttribute('src', dataURL)
                }
            } else {
                Swal.showValidationMessage('大小不合适')
                return false
            }
        }

        return {
            showUploadAvatarDialog,
            avatarFile,
            onchangeImgFun,
        }
    },
}
</script>
<style lang="scss">
.my-dialog-html-container-class {
    .avatar {
        position: relative;
        display: inline-block;
        width: 144px;
        height: 144px;
        border-radius: 50%;
        overflow: hidden;
        input {
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 100%;
            opacity: 0;
            cursor: pointer;
        }
        img {
            height: 100%;
            width: 100%;
        }
    }
}
</style>
