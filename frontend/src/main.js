import './assets/style/base.css'
import './assets/style/UI.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import request from '@/utils/Request.js'
import Utils from '@/utils/Utils.js'
import VueCookies from 'vue-cookies'
import 'element-plus/theme-chalk/index.css'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
library.add(fas, far)

// 代码高亮
import HljsVuePlugin from '@highlightjs/vue-plugin'
import 'highlight.js/styles/atom-one-dark-reasonable.css'
import 'highlight.js/lib/common'
const app = createApp(App)
app.config.globalProperties.Request = request
app.config.globalProperties.VueCookies = VueCookies
app.config.globalProperties.Utils = Utils
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.use(HljsVuePlugin)
app.use(store)
app.use(ElementPlus)
app.mount('#app')
