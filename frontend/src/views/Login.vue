<template>
    <div class="login-body">
        <div class="container">
            <div class="title">
                <h2>登录到FastPan</h2>
            </div>
            <form @submit.prevent="doSubmit()" novalidate>
                <div class="form-line">
                    <Input
                        type="text"
                        name="email"
                        placeholder="输入邮箱"
                        :value="formData.email"
                        :rule="rules.emailRule"
                        @update="updateForm"
                    />
                    <!-- <input type="email" v-model="formData.email" placeholder="输入邮箱" /> -->
                </div>
                <div class="form-line" v-show="opType === 2">
                    <div class="email-code-panel">
                        <Input
                            type="text"
                            name="code"
                            placeholder="输入邮箱验证码"
                            :value="formData.code"
                            :rule="rules.emailCodeRule"
                            @update="updateForm"
                        />
                        <!-- <input type="text" v-model="formData.code" placeholder="输入邮箱验证码" /> -->
                        <button type="button" @click="showDialog" :disabled="isDisabled">
                            {{ buttonText }}
                        </button>
                    </div>
                    <Popover orient="left">
                        <template v-slot:default>
                            <span style="margin-left: 2px; font-size: 12px; cursor: pointer"
                                >未收到验证码？</span
                            >
                        </template>

                        <template v-slot:content>
                            <div class="popover-content">
                                <p>1、在垃圾箱中查找邮箱验证码</p>
                                <p>2、在邮箱中头像->设置->反垃圾->白名单->设置邮件地址白名单</p>
                                <p>
                                    3、将邮箱【1 aoluo@(wuhancoder,com】添加到白名单不知道怎么设置
                                </p>
                            </div>
                        </template>
                    </Popover>
                </div>
                <div class="form-line" v-if="opType === 1">
                    <Input
                        type="user"
                        name="nickname"
                        placeholder="输入用户名"
                        :value="formData.nickname"
                        :rule="rules.nicknameRule"
                        @update="updateForm"
                    />
                    <!-- <input type="user" v-model="formData.nickname" placeholder="输入用户名" /> -->
                </div>
                <div class="form-line">
                    <Input
                        type="password"
                        name="password"
                        placeholder="输入密码"
                        :value="formData.password"
                        :rule="rules.passwordRule"
                        @update="updateForm"
                    />
                    <!-- <input type="password" v-model="formData.password" placeholder="输入密码" /> -->
                </div>
                <div class="form-line" v-if="opType !== 0">
                    <input
                        type="password"
                        v-model="formData.passwordRepeat"
                        placeholder="重复输入密码"
                    />
                </div>
                <div class="form-line" v-if="opType !== 0">
                    <div class="check-code-panel">
                        <input
                            type="text"
                            v-model="formData.captcha_code"
                            class="check-code"
                            placeholder="输入验证码"
                        />
                        <img :src="captcha_url" @click="refreshCaptcha(0)" />
                    </div>
                </div>
                <div class="form-line">
                    <div class="rememberme-panel" v-if="opType === 0">
                        <input type="checkbox" v-model="formData.rememberMe" />记住我
                    </div>
                    <div class="no-account-panel">
                        <a
                            href="javascript: void(0)"
                            v-if="opType === 0"
                            class="a-link"
                            @click="changeOnType(2)"
                            >忘记密码?</a
                        ><a
                            href="javascript: void(0)"
                            v-if="opType !== 0"
                            class="a-link"
                            @click="changeOnType(0)"
                            >已有账号</a
                        >
                        <a
                            href="javascript: void(0)"
                            v-if="opType === 0"
                            class="a-link"
                            @click="changeOnType(1)"
                            >没有账号?</a
                        >
                    </div>
                </div>
                <div class="form-line">
                    <div class="btns">
                        <button v-if="opType === 0">登陆</button>
                        <button v-if="opType === 0">QQ 快捷登陆</button>
                        <button v-if="opType === 1">注册</button>
                        <button v-if="opType === 2">重置密码</button>
                    </div>
                </div>
            </form>
        </div>
        <Dialog :config="dialogConfig4SendMailCode">
            <div class="mail-dialog">
                <div class="dialog-item"><span>邮箱</span> {{ formData.email }}</div>
                <div class="dialog-item">
                    <span>验证码</span>
                    <input type="text" v-model="dialogConfig4SendMailCode.data.captcha_code" /><img
                        :src="
                            'http://localhost:7070/api/v1/captcha/' +
                            dialogConfig4SendMailCode.data.captcha_id +
                            '.png'
                        "
                    />
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script>
import Dialog from '../components/Dialog.vue'
import Input from '../components/Input.vue'
import Popover from '../components/Popover.vue'
import { formValidator, itemValidator } from '../utils/Validator.js'
import { ref, reactive, computed, onMounted, getCurrentInstance } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Swal from 'sweetalert2'
export default {
    components: {
        Dialog,
        Input,
        Popover,
    },
    setup() {
        const { proxy } = getCurrentInstance()
        const router = useRouter()
        const route = useRoute()
        const api = {
            login: '/login/access-token',
            register: '/user',
            resetPwd: '/user/resetPwd',
            qqlogin: '/login/qqlogin',
            checkCode: '/captcha',
            verifyCaptcha: '/captcha/verify',
            sendEmailCode: '/captcha/sendEmailCode',
        }
        const countdown = ref(0)
        const isOpen = ref(false)
        const opType = ref(0)
        const formData = ref({})
        const popoverPosition = ref({ top: 0, right: 0 })
        const captcha_url = computed(() => {
            const id = formData.value.captcha_id
            if (id) return `http://localhost:7070/api/v1/captcha/${id}.png`
            else return ''
        })
        const checkCodeUrl4Dialog = ref('src/assets/img/checkCode.jfif')
        const startCountdown = () => {
            countdown.value = 10
            const timer = setInterval(() => {
                countdown.value--
                if (countdown.value === 0) {
                    clearInterval(timer)
                }
            }, 1000)
        }
        const isDisabled = computed(() => {
            return countdown.value > 0
        })
        const buttonText = computed(() => {
            return countdown.value > 0 ? `${countdown.value}s` : '获取验证码'
        })
        // 表单验证
        const rules = {
            nicknameRule: {
                required: true,
                minLength: 6,
                maxLength: 15,
            },
            passwordRule: {
                required: true,
                minLength: 6,
            },
            emailRule: {
                required: true,
                email: true,
            },
            emailCodeRule: {
                required: true,
            },
            loginRule: {
                email: {
                    required: true,
                    email: true,
                },
                password: {
                    required: true,
                    minLength: 6,
                },
            },
            registerRule: {
                email: {
                    required: true,
                    email: true,
                },
                nickname: {
                    required: true,
                    minLength: 6,
                    maxLength: 15,
                },
                password: {
                    required: true,
                    minLength: 6,
                },
                passwordRepeat: {
                    required: true,
                    confirm: 'password',
                },
                captcha_code: {
                    required: true,
                },
            },
            resetRule: {
                email: {
                    required: true,
                    email: true,
                },
                code: {
                    required: true,
                },
                password: {
                    required: true,
                    minLength: 6,
                },
                passwordRepeat: {
                    required: true,
                    confirm: 'password',
                },
                captcha_code: {
                    required: true,
                },
            },
        }
        const readCookie = () => {
            const cookieLoginInfo = proxy.VueCookies.get('loginInfo')
            if (cookieLoginInfo) {
                formData.value = cookieLoginInfo
            }
        }
        // 重新获取验证码
        const refreshCaptcha = async (idx) => {
            const res = await proxy.Request.get(api.checkCode, {
                params: {
                    timestamp: Date.now(),
                },
            })
            const captcha_id = res.data.data.captcha_id
            if (idx === 0) formData.value.captcha_id = captcha_id
            else if (idx === 1) dialogConfig4SendMailCode.data.captcha_id = captcha_id
        }
        // 重置表单
        const resetForm = () => {
            refreshCaptcha(0) // 重新获取验证码
            formData.value = {}
            console.log(formData.value)
            if (opType.value === 0) readCookie()
        }
        // 发送表单验证码
        const sendEmailCode = async () => {
            const res = itemValidator(formData.value.email, rules.emailRule)
            if (res !== true) return
            const params = Object.assign({}, formData)
            params.type = opType === 0 ? 0 : 1
            try {
                let result = await proxy.Request({
                    url: api.sendEmailCode,
                    type: 'get',
                    params: params,
                })
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: error,
                })
            }
        }
        // 改变状态
        const changeOnType = (new_type) => {
            opType.value = new_type
            resetForm()
        }
        // 验证码dialog信息
        const dialogConfig4SendMailCode = reactive({
            title: '发送邮箱验证码',
            width: '500px',
            visible: false,
            showCancel: true,
            email: '',
            data: {
                captcha_id: '',
                captcha_code: '',
            },
            buttons: [
                {
                    title: 'Confirm',
                    async func() {
                        startCountdown()
                        let result = await proxy.Request.post(api.sendEmailCode, {
                            email: formData.value.email,
                            captcha_id: dialogConfig4SendMailCode.data.captcha_id,
                            captcha_code: dialogConfig4SendMailCode.data.captcha_code,
                        })
                        if (result.data.code === 400) {
                            Swal.fire({
                                icon: 'waring',
                                title: '验证码',
                                text: '验证码错误',
                            })
                            return await refreshCaptcha(1)
                        }
                        Swal.fire({
                            toast: true,
                            position: 'top-end',
                            showConfirmButton: false,
                            timer: 3000,
                            type: 'success',
                            title: 'Signed in successfully',
                        })
                    },
                },
            ],
            show() {
                this.visible = true
            },
            close() {
                this.visible = false
                this.email = ''
            },
        })
        // 弹出dialog + 验证
        const showDialog = () => {
            const res = itemValidator(formData.value.email, rules.emailRule)
            if (res === true) {
                refreshCaptcha(1)
                dialogConfig4SendMailCode.data.captcha_code = ''
                return dialogConfig4SendMailCode.show()
            } else
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: res,
                })
        }
        const handleLogin = async () => {
            const params = Object.assign({}, formData.value)
            const res = formValidator(params, rules.loginRule)
            if (res !== true) return alert(res)
            let result = await proxy.Request.post(
                api.login,
                {
                    username: params.email,
                    password: params.password,
                },
                {
                    transformRequest: [
                        (data) => {
                            const formData = new FormData()
                            Object.entries(data).forEach(([key, value]) => {
                                formData.append(key, value)
                            })
                            return formData
                        },
                    ],
                },
            )
            if (!result) return
            if (params.rememberMe) {
                const loginInfo = {
                    email: params.email,
                    password: params.password,
                    rememberMe: params.rememberMe,
                }
                proxy.VueCookies.set('loginInfo', loginInfo, '7d')
            } else proxy.VueCookies.remove('loginInfo')
            Swal.fire({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 4000,
                type: 'success',
                title: 'Signed in successfully',
            })
            // 存储用户信息userInfo
            proxy.VueCookies.set('userInfo', result.data.info, 0)
            // 存储登陆信息cookie
            proxy.VueCookies.set('token', result.data.access_token, 0)
            // 重定向
            setTimeout(() => {
                router.push(route.query.redirectUrl || '/')
            }, 2000)
        }
        const handleRegister = async () => {
            const params = Object.assign({}, formData.value)
            const res = formValidator(params, rules.registerRule)
            if (res !== true) return alert(res)
            let result = await proxy.Request.post(api.register, params)
            if (!result) return
            alert('注册成功')
            changeOnType(0)
        }
        const handleReset = async () => {
            const params = Object.assign({}, formData.value)
            const res = formValidator(params, rules.resetRule)
            if (res !== true) return alert(res)
            let result = await proxy.Request.post(api.resetPwd, params)
            if (!result) return
            alert('重置成功')
            changeOnType(0)
        }
        // 表单提交
        const doSubmit = async () => {
            if (opType.value === 0) await handleLogin()
            else if (opType.value === 1) await handleRegister()
            else await handleReset()
        }
        onMounted(() => {
            readCookie()
        })
        const updateForm = (param) => {
            formData.value[param.name] = param.value
        }
        return {
            rules,
            isOpen,
            opType,
            formData,
            captcha_url,
            popoverPosition,
            showDialog,
            refreshCaptcha,
            doSubmit,
            changeOnType,
            isDisabled,
            buttonText,
            dialogConfig4SendMailCode,
            checkCodeUrl4Dialog,
            updateForm,
        }
    },
}
</script>

<style scoped lang="scss">
.login-body {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    background-size: 400%;
    background-image: linear-gradient(
        125deg,
        #845ec2,
        #d65db1,
        #ff6f91,
        #ff9671,
        #ffc75f,
        #f9f871,
        #845ec2
    );
    animation: bgmove 20s infinite;
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        row-gap: 1rem;
        width: 380px;
        border-radius: 0.75rem;
        padding: 24px;
        background: #fff;
        transition: 0.5s;
        .title {
            display: flex;
            align-items: center;
            color: #0091ff;
            justify-content: space-around;
            h2 {
                font-size: 1.7rem;
            }
        }
        form {
            position: relative;
            width: 100%;
            .form-line {
                width: 100%;
                margin-bottom: 10px;
                input {
                    width: 100%;
                }
                .check-code-panel {
                    position: relative;
                    width: 100%;
                    display: flex;
                    img {
                        width: 70%;
                        margin-left: 15px;
                        cursor: pointer;
                    }
                }
                .email-code-panel {
                    position: relative;
                    width: 100%;
                    display: flex;
                    button {
                        width: 50%;
                        margin-left: 15px;
                        cursor: pointer;
                    }
                }
                .rememberme-panel {
                    display: flex;
                    justify-content: flex-start;
                    align-items: center;
                    margin-top: 1.5rem;
                    font-size: 0.875rem;
                    input {
                        margin-right: 10px;
                        width: 0.875rem;
                        height: 0.875rem;
                    }
                }
                .no-account-panel {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-top: 1rem;
                    .a-link {
                        font-size: 0.875rem;
                        font-weight: 700;
                        color: rgb(91, 91, 165);
                        text-decoration: none;
                    }
                }
                .btns {
                    display: flex;
                    flex-direction: column;
                    button {
                        margin-bottom: 0.5rem;
                        width: 100%;
                    }
                }
            }
        }
    }
}
.mail-dialog {
    font-size: 0.875rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    .dialog-item {
        display: flex;
        align-items: center;
        width: 100%;
        height: 40px;
        span {
            display: inline-block;
            width: 15%;
        }
        input {
            flex: 1;
            margin-right: 1rem;
        }
    }
}
.popover-content {
    border-radius: 10px;
    padding: 10px 5px;
    p {
        padding: 5px 0;
    }
}
</style>
