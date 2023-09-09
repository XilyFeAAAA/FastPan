import { createRouter, createWebHistory } from 'vue-router'
import VueCookies from 'vue-cookies'
import request from '../utils/Request'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            name: 'Login',
            component: () => import('@/views/Login.vue'),
        },
        {
            path: '/',
            name: 'Framework',
            component: () => import('@/views/Framework.vue'),
            children: [
                { path: '/', redirect: '/main/all' },
                {
                    path: '/main/:category',
                    name: '首页',
                    meta: {
                        needLogin: true,
                        menuCode: 'main',
                    },
                    component: () => import('@/views/main/Main.vue'),
                },
                {
                    path: '/share',
                    name: '分享',
                    meta: {
                        needLogin: true,
                        menuCode: 'share',
                    },
                    component: () => import('@/views/share/Share.vue'),
                },
                {
                    path: '/recycle',
                    name: '回收站',
                    meta: {
                        needLogin: true,
                        menuCode: 'recycle',
                    },
                    component: () => import('@/views/recycle/Recycle.vue'),
                },
                {
                    path: '/setting',
                    name: '设置',
                    meta: {
                        needLogin: true,
                        menuCode: 'setting',
                    },
                    component: () => import('@/views/setting/Setting.vue'),
                },
            ],
        },
        {
            path: '/shareCheck/:shareId',
            name: 'shareCheck',
            component: () => import('@/views/webShare/ShareCheck.vue'),
        },
        {
            path: '/share/:shareId',
            name: 'share',
            component: () => import('@/views/webShare/Share.vue'),
        },
    ],
})
const api = '/user/active'
const check_active = async () => {
    const res = await request.get(api)
    if (res && res.data.code === 200) return true
    return false
}

// router.beforeEach(async (to, from, next) => {
//     if (to.path == '/login') {
//         next()
//     } else {
//         //先判断是否登录
//         if (VueCookies.get('token')) {
//             if (await check_active()) next()
//             else next('/login?redirectUrl=' + to.path)
//         } else next('/login?redirectUrl=' + to.path)
//     }
// })

export default router
