import axios from 'axios'
import { ElLoading } from 'element-plus'
// 全局配置
import webConfig from '@/global.config'
// base64 加密
import Swal from 'sweetalert2'
let request = axios.create({
    baseURL: 'http://localhost:7070/api/v1',
    timeout: 10 * 1000,
})

let loading = null
import VueCookies from 'vue-cookies'
request.interceptors.request.use(
    (config) => {
        // token
        if (config.showLoading) {
            loading = ElLoading.service({
                lock: true,
                text: '加载中',
                background: 'rgba(0,0,0,0.7)',
            })
        }

        let whiteList = webConfig.whiteListApi
        let url = config.url
        let token = VueCookies.get('token')
        if (whiteList.indexOf(url) === -1 && token) {
            config.headers['Authorization'] = `Bearer ${token}`
        }
        // let _secret = md5(webConfig.secretId + new Date.toString())
        // config.headers.secret = _secret
        return config
    },
    (error) => {
        return alert(error)
    },
)

request.interceptors.response.use(
    (res) => {
        // 响应统一处理
        if (loading) loading.close()
        const { errorCallback } = res.config
        const code = res.data.code || 200
        const message = res.data.msg || ''
        if (code !== 200) {
            if (errorCallback) {
                errorCallback(message)
            } else {
                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 4000,
                    type: 'error',
                    title: `code ${code}: ${message}`,
                })
            }
        }
        return res
    },
    (error) => {
        Swal.fire({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 4000,
            type: 'error',
            title: error,
        })
        return null
    },
)

export default request
