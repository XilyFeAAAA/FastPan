<template>
    <div class="framework">
        <div class="header flex-start">
            <div class="logo flex-start">
                <a class="flex-center">
                    <img
                        src="https://ssl.gstatic.com/images/branding/product/1x/drive_2020q4_48dp.png"
                    />
                    <span>FastPan</span>
                </a>
            </div>
            <div class="top-nav">
                <div class="input-fragment" :class="{ open: isInputFocused }">
                    <div class="keyword-input flex-between">
                        <span class="flex-center"
                            ><font-awesome-icon icon="magnifying-glass"
                        /></span>
                        <input
                            type="text"
                            @focus="isInputFocused = true"
                            @blur="isInputFocused = false"
                            placeholder="在云端硬盘中搜索"
                        />
                        <span class="flex-center">
                            <svg
                                class="Q6yead QJZfhe"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                focusable="false"
                            >
                                <path
                                    d="M3 17v2h6v-2H3zM3 5v2h10V5H3zm10 16v-2h8v-2h-8v-2h-2v6h2zM7 9v2H3v2h4v2h2V9H7zm14 4v-2H11v2h10zm-6-4h2V7h4V5h-4V3h-2v6z"
                                ></path>
                            </svg>
                        </span>
                    </div>
                    <div class="category-list">
                        <ul class="flex-between">
                            <li>
                                <div class="category-block">
                                    <svg
                                        t="1686833350618"
                                        class="icon"
                                        viewBox="0 0 1024 1024"
                                        version="1.1"
                                        xmlns="http://www.w3.org/2000/svg"
                                        p-id="2381"
                                        width="30"
                                        height="30"
                                    >
                                        <path
                                            d="M398.848 670.72c5.12 0 9.728-1.536 14.336-4.096l225.792-130.048c13.312-7.68 18.432-25.088 10.752-38.4-2.56-4.096-6.144-7.68-10.24-10.24L413.184 357.376c-13.824-7.68-30.72-3.072-38.4 10.752-2.56 4.096-3.584 9.216-3.584 13.824v260.608c-0.512 15.36 12.288 28.16 27.648 28.16z m28.16-240.128L568.32 512l-141.312 81.408V430.592z"
                                            fill="#9c5249"
                                            p-id="2382"
                                        ></path>
                                        <path
                                            d="M926.208 873.472H97.792C44.032 873.472 0 829.44 0 775.168V248.832C0 194.56 44.032 150.528 97.792 150.528h827.904c54.272 0 97.792 44.032 97.792 97.792v526.848c0.512 54.272-43.52 98.304-97.28 98.304zM97.792 211.968c-20.48 0-36.864 16.384-36.864 36.864v526.848c0 20.48 16.384 36.864 36.864 36.864h827.904c20.48 0 36.864-16.384 36.864-36.864V248.832c0-20.48-16.384-36.864-36.864-36.864H97.792z"
                                            fill="#9c5249"
                                            p-id="2383"
                                        ></path>
                                    </svg>
                                </div>
                            </li>
                            <li>
                                <div class="category-block">
                                    <svg
                                        t="1686834929300"
                                        class="icon"
                                        viewBox="0 0 1024 1024"
                                        version="1.1"
                                        xmlns="http://www.w3.org/2000/svg"
                                        p-id="3967"
                                        width="30"
                                        height="30"
                                    >
                                        <path
                                            d="M304 665.6a22.4 22.4 0 1 0 44.8 0 22.4 22.4 0 1 0-44.8 0z m275.2-48a22.4 22.4 0 1 0 44.8 0 22.4 22.4 0 1 0-44.8 0z"
                                            p-id="3968"
                                            fill="#545d91"
                                        ></path>
                                        <path
                                            d="M512 32C246.4 32 32 246.4 32 512s214.4 480 480 480 480-214.4 480-480S777.6 32 512 32z m176 585.6c0 51.2-38.4 89.6-86.4 89.6-48 0-86.4-38.4-86.4-86.4s38.4-86.4 86.4-86.4c9.6 0 16 0 22.4 3.2v-99.2L412.8 480v188.8c0 48-38.4 86.4-86.4 86.4-48 0-86.4-38.4-86.4-86.4s38.4-86.4 86.4-86.4c9.6 0 16 0 22.4 3.2V371.2c0-25.6 19.2-51.2 48-57.6l208-48c25.6-6.4 48 0 64 12.8C681.6 288 688 304 688 320v297.6z"
                                            p-id="3969"
                                            fill="#545d91"
                                        ></path>
                                        <path
                                            d="M412.8 371.2v41.6L624 368v-44.8h-6.4l-204.8 48z"
                                            p-id="3970"
                                            fill="#545d91"
                                        ></path>
                                    </svg>
                                </div>
                            </li>
                            <li>
                                <div class="category-block">
                                    <svg
                                        t="1686833350618"
                                        class="icon"
                                        viewBox="0 0 1024 1024"
                                        version="1.1"
                                        xmlns="http://www.w3.org/2000/svg"
                                        p-id="2381"
                                        width="30"
                                        height="30"
                                    >
                                        <path
                                            d="M398.848 670.72c5.12 0 9.728-1.536 14.336-4.096l225.792-130.048c13.312-7.68 18.432-25.088 10.752-38.4-2.56-4.096-6.144-7.68-10.24-10.24L413.184 357.376c-13.824-7.68-30.72-3.072-38.4 10.752-2.56 4.096-3.584 9.216-3.584 13.824v260.608c-0.512 15.36 12.288 28.16 27.648 28.16z m28.16-240.128L568.32 512l-141.312 81.408V430.592z"
                                            fill="#9c5249"
                                            p-id="2382"
                                        ></path>
                                        <path
                                            d="M926.208 873.472H97.792C44.032 873.472 0 829.44 0 775.168V248.832C0 194.56 44.032 150.528 97.792 150.528h827.904c54.272 0 97.792 44.032 97.792 97.792v526.848c0.512 54.272-43.52 98.304-97.28 98.304zM97.792 211.968c-20.48 0-36.864 16.384-36.864 36.864v526.848c0 20.48 16.384 36.864 36.864 36.864h827.904c20.48 0 36.864-16.384 36.864-36.864V248.832c0-20.48-16.384-36.864-36.864-36.864H97.792z"
                                            fill="#9c5249"
                                            p-id="2383"
                                        ></path>
                                    </svg>
                                </div>
                            </li>
                            <li>
                                <div class="category-block">
                                    <svg
                                        t="1686833350618"
                                        class="icon"
                                        viewBox="0 0 1024 1024"
                                        version="1.1"
                                        xmlns="http://www.w3.org/2000/svg"
                                        p-id="2381"
                                        width="30"
                                        height="30"
                                    >
                                        <path
                                            d="M398.848 670.72c5.12 0 9.728-1.536 14.336-4.096l225.792-130.048c13.312-7.68 18.432-25.088 10.752-38.4-2.56-4.096-6.144-7.68-10.24-10.24L413.184 357.376c-13.824-7.68-30.72-3.072-38.4 10.752-2.56 4.096-3.584 9.216-3.584 13.824v260.608c-0.512 15.36 12.288 28.16 27.648 28.16z m28.16-240.128L568.32 512l-141.312 81.408V430.592z"
                                            fill="#9c5249"
                                            p-id="2382"
                                        ></path>
                                        <path
                                            d="M926.208 873.472H97.792C44.032 873.472 0 829.44 0 775.168V248.832C0 194.56 44.032 150.528 97.792 150.528h827.904c54.272 0 97.792 44.032 97.792 97.792v526.848c0.512 54.272-43.52 98.304-97.28 98.304zM97.792 211.968c-20.48 0-36.864 16.384-36.864 36.864v526.848c0 20.48 16.384 36.864 36.864 36.864h827.904c20.48 0 36.864-16.384 36.864-36.864V248.832c0-20.48-16.384-36.864-36.864-36.864H97.792z"
                                            fill="#9c5249"
                                            p-id="2383"
                                        ></path>
                                    </svg>
                                </div>
                            </li>
                            <li>
                                <div class="category-block">
                                    <svg
                                        t="1686833350618"
                                        class="icon"
                                        viewBox="0 0 1024 1024"
                                        version="1.1"
                                        xmlns="http://www.w3.org/2000/svg"
                                        p-id="2381"
                                        width="30"
                                        height="30"
                                    >
                                        <path
                                            d="M398.848 670.72c5.12 0 9.728-1.536 14.336-4.096l225.792-130.048c13.312-7.68 18.432-25.088 10.752-38.4-2.56-4.096-6.144-7.68-10.24-10.24L413.184 357.376c-13.824-7.68-30.72-3.072-38.4 10.752-2.56 4.096-3.584 9.216-3.584 13.824v260.608c-0.512 15.36 12.288 28.16 27.648 28.16z m28.16-240.128L568.32 512l-141.312 81.408V430.592z"
                                            fill="#9c5249"
                                            p-id="2382"
                                        ></path>
                                        <path
                                            d="M926.208 873.472H97.792C44.032 873.472 0 829.44 0 775.168V248.832C0 194.56 44.032 150.528 97.792 150.528h827.904c54.272 0 97.792 44.032 97.792 97.792v526.848c0.512 54.272-43.52 98.304-97.28 98.304zM97.792 211.968c-20.48 0-36.864 16.384-36.864 36.864v526.848c0 20.48 16.384 36.864 36.864 36.864h827.904c20.48 0 36.864-16.384 36.864-36.864V248.832c0-20.48-16.384-36.864-36.864-36.864H97.792z"
                                            fill="#9c5249"
                                            p-id="2383"
                                        ></path>
                                    </svg>
                                </div>
                            </li>
                            <li>
                                <div class="category-block">
                                    <svg
                                        t="1686833350618"
                                        class="icon"
                                        viewBox="0 0 1024 1024"
                                        version="1.1"
                                        xmlns="http://www.w3.org/2000/svg"
                                        p-id="2381"
                                        width="30"
                                        height="30"
                                    >
                                        <path
                                            d="M398.848 670.72c5.12 0 9.728-1.536 14.336-4.096l225.792-130.048c13.312-7.68 18.432-25.088 10.752-38.4-2.56-4.096-6.144-7.68-10.24-10.24L413.184 357.376c-13.824-7.68-30.72-3.072-38.4 10.752-2.56 4.096-3.584 9.216-3.584 13.824v260.608c-0.512 15.36 12.288 28.16 27.648 28.16z m28.16-240.128L568.32 512l-141.312 81.408V430.592z"
                                            fill="#9c5249"
                                            p-id="2382"
                                        ></path>
                                        <path
                                            d="M926.208 873.472H97.792C44.032 873.472 0 829.44 0 775.168V248.832C0 194.56 44.032 150.528 97.792 150.528h827.904c54.272 0 97.792 44.032 97.792 97.792v526.848c0.512 54.272-43.52 98.304-97.28 98.304zM97.792 211.968c-20.48 0-36.864 16.384-36.864 36.864v526.848c0 20.48 16.384 36.864 36.864 36.864h827.904c20.48 0 36.864-16.384 36.864-36.864V248.832c0-20.48-16.384-36.864-36.864-36.864H97.792z"
                                            fill="#9c5249"
                                            p-id="2383"
                                        ></path>
                                    </svg>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <div class="advanced-search flex-center">
                        <button>高级搜索</button>
                    </div>
                </div>
                <div class="btn-fragment flex-start">
                    <div class="icon-block">
                        <Popover orient="bottom" ref="popover_ref_1">
                            <template v-slot:default>
                                <span
                                    class="flex-center"
                                    v-on:mouseenter="popover_ref_1.showChange()"
                                    v-on:mouseleave="popover_ref_1.showChange()"
                                >
                                    <svg
                                        class="wo35tf"
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="24px"
                                        height="24px"
                                        viewBox="0 0 24 24"
                                        fill="#000000"
                                        focusable="false"
                                    >
                                        <path fill="none" d="M0 0h24v24H0z"></path>
                                        <path
                                            d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"
                                        ></path>
                                    </svg>
                                </span>
                            </template>
                            <template v-slot:content>
                                <div class="popover-content">
                                    <p>支持</p>
                                </div>
                            </template>
                        </Popover>
                    </div>
                    <div class="icon-block">
                        <Popover orient="bottom" ref="popover_ref_2">
                            <template v-slot:default>
                                <span
                                    class="flex-center"
                                    v-on:mouseenter="popover_ref_2.showChange()"
                                    v-on:mouseleave="popover_ref_2.showChange()"
                                >
                                    <svg
                                        class="a-s-fa-Ha-pa c-qd"
                                        width="24px"
                                        height="24px"
                                        viewBox="0 0 24 24"
                                        fill="currentColor"
                                        focusable="false"
                                    >
                                        <path
                                            d="M13.85 22.25h-3.7c-.74 0-1.36-.54-1.45-1.27l-.27-1.89c-.27-.14-.53-.29-.79-.46l-1.8.72c-.7.26-1.47-.03-1.81-.65L2.2 15.53c-.35-.66-.2-1.44.36-1.88l1.53-1.19c-.01-.15-.02-.3-.02-.46 0-.15.01-.31.02-.46l-1.52-1.19c-.59-.45-.74-1.26-.37-1.88l1.85-3.19c.34-.62 1.11-.9 1.79-.63l1.81.73c.26-.17.52-.32.78-.46l.27-1.91c.09-.7.71-1.25 1.44-1.25h3.7c.74 0 1.36.54 1.45 1.27l.27 1.89c.27.14.53.29.79.46l1.8-.72c.71-.26 1.48.03 1.82.65l1.84 3.18c.36.66.2 1.44-.36 1.88l-1.52 1.19c.01.15.02.3.02.46s-.01.31-.02.46l1.52 1.19c.56.45.72 1.23.37 1.86l-1.86 3.22c-.34.62-1.11.9-1.8.63l-1.8-.72c-.26.17-.52.32-.78.46l-.27 1.91c-.1.68-.72 1.22-1.46 1.22zm-3.23-2h2.76l.37-2.55.53-.22c.44-.18.88-.44 1.34-.78l.45-.34 2.38.96 1.38-2.4-2.03-1.58.07-.56c.03-.26.06-.51.06-.78s-.03-.53-.06-.78l-.07-.56 2.03-1.58-1.39-2.4-2.39.96-.45-.35c-.42-.32-.87-.58-1.33-.77l-.52-.22-.37-2.55h-2.76l-.37 2.55-.53.21c-.44.19-.88.44-1.34.79l-.45.33-2.38-.95-1.39 2.39 2.03 1.58-.07.56a7 7 0 0 0-.06.79c0 .26.02.53.06.78l.07.56-2.03 1.58 1.38 2.4 2.39-.96.45.35c.43.33.86.58 1.33.77l.53.22.38 2.55z"
                                        ></path>
                                        <circle cx="12" cy="12" r="3.5"></circle>
                                    </svg>
                                </span>
                            </template>
                            <template v-slot:content>
                                <div class="popover-content">
                                    <p>设置</p>
                                </div>
                            </template>
                        </Popover>
                    </div>
                    <div class="icon-block">
                        <Popover orient="bottom" :showTriangle="false" ref="popover_ref_3">
                            <template v-slot:default>
                                <span class="flex-center" @click="popover_ref_3.showChange()">
                                    <font-awesome-icon icon="upload" size="lg" />
                                </span>
                            </template>
                            <template v-slot:content>
                                <div class="popover-content">
                                    <uploadFrame
                                        ref="uploader"
                                        @uploadCallback="uploadCallbackHandle"
                                    />
                                </div>
                            </template>
                        </Popover>
                    </div>
                    <div class="icon-block">
                        <Popover orient="bottom" :showTriangle="false" ref="popover_ref_4">
                            <template v-slot:default>
                                <span
                                    class="flex-center"
                                    v-on:mouseenter="popover_ref_4.showChange()"
                                    v-on:mouseleave="popover_ref_4.showChange()"
                                >
                                    <svg
                                        style="color: #000; width: 25px"
                                        focusable="false"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            d="M6,8c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM12,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM6,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM6,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM12,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM16,6c0,1.1 0.9,2 2,2s2,-0.9 2,-2 -0.9,-2 -2,-2 -2,0.9 -2,2zM12,8c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM18,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM18,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2z"
                                        ></path>
                                    </svg>
                                </span>
                            </template>
                            <template v-slot:content>
                                <div class="popover-content">应用</div>
                            </template>
                        </Popover>
                    </div>
                    <div class="icon-block">
                        <Popover orient="bottom" :showTriangle="false" ref="popover_ref_5">
                            <template v-slot:default>
                                <span class="flex-center" @click="popover_ref_5.showChange()">
                                    <img class="avatar-img" :src="avatar_url" />
                                </span>
                            </template>
                            <template v-slot:content>
                                <ul class="avatar-menu-popover">
                                    <li
                                        class="flex-center"
                                        @click="uploadAvatarDialog.showUploadAvatarDialog()"
                                    >
                                        修改头像
                                    </li>
                                    <li
                                        class="flex-center"
                                        @click="changePasswordDialog.showChangePasswordDialog()"
                                    >
                                        修改密码
                                    </li>
                                    <li class="flex-center" @click="logout">退出</li>
                                </ul>
                            </template>
                        </Popover>
                    </div>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="nav-bar">
                <div class="create">
                    <button class="flex-center"><font-awesome-icon icon="plus" />新建</button>
                </div>
                <nav>
                    <ul class="menu">
                        <li v-for="(menu, idx) in menus" :key="idx" class="menu-item">
                            <div
                                class="menu-link flex-start"
                                :class="{
                                    folder: menu.children,
                                    open: menu.allShow,
                                    active: menu.menuCode === currentMenu.menuCode,
                                }"
                                @click="handleMenuClick(menu)"
                            >
                                <font-awesome-icon :icon="menu.icon" class="font-icon" />{{
                                    menu.name
                                }}
                            </div>
                            <ul
                                class="sub-menu"
                                v-if="menu.children"
                                :class="{ open: menu.allShow }"
                            >
                                <li
                                    v-for="(sub_menu, idx) in menu.children"
                                    class="sub-menu-item"
                                    :class="{ active: sub_menu.menuCode === currentMenu.menuCode }"
                                    :key="idx"
                                    @click="jump(sub_menu)"
                                >
                                    <font-awesome-icon :icon="sub_menu.icon" class="font-icon" />{{
                                        sub_menu.name
                                    }}
                                </li>
                            </ul>
                        </li>
                    </ul>
                </nav>
                <div class="drive-space">
                    <div class="space-progress"></div>
                    <div class="space-info flex-evenly">
                        <p>
                            {{ proxy.Utils.sizeToStr(space.used) }}/{{
                                proxy.Utils.sizeToStr(space.total)
                            }}
                        </p>
                        <span>
                            <font-awesome-icon
                                icon="arrows-rotate"
                                class="refresh-icon"
                                @click="updateSpace"
                            />
                        </span>
                    </div>
                    <div class="more-space-btn flex-center">
                        <button>获取更多空间</button>
                    </div>
                </div>
            </div>
            <div class="main-panel">
                <router-view v-slot="{ Component }">
                    <component
                        :is="Component"
                        @addFile="addFile"
                        @updateSpace="updateSpace"
                        ref="Component"
                    ></component>
                </router-view>

                <!-- <router-view></router-view> -->
            </div>
        </div>
        <ChangePasswordDialog ref="changePasswordDialog" />
        <UploadAvatarDialog ref="uploadAvatarDialog" :avatar_url="avatar_url" />
    </div>
</template>
<script>
import { ref, watch, getCurrentInstance, computed, nextTick, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Popover from '../components/Popover.vue'
import uploadFrame from './main/uploadFrame.vue'
import ChangePasswordDialog from './updatePwd.vue'
import UploadAvatarDialog from './uploadAvatar.vue'
import Swal from 'sweetalert2'
export default {
    components: { Popover, uploadFrame, ChangePasswordDialog, UploadAvatarDialog },
    setup(props, { emit }) {
        const route = useRoute()
        const router = useRouter()
        const isInputFocused = ref(false)
        const folder_isopen = ref(false)
        const space = ref({
            used: '100MB',
            all: '15GB',
        })
        const api = {
            logout: '/user/logout',
            me: '/user/me',
        }
        const Component = ref()
        const uploader = ref()
        const popover_ref_1 = ref()
        const popover_ref_2 = ref()
        const popover_ref_3 = ref()
        const popover_ref_4 = ref()
        const popover_ref_5 = ref()
        const updatePwdDialog = ref()
        const changePasswordDialog = ref()
        const uploadAvatarDialog = ref()
        const currentMenu = ref({})
        const currentPath = ref()
        const avatar_url = computed(() => {
            const info = proxy.VueCookies.get('userInfo')
            if (info) {
                return `http://localhost:7070/api/v1/getAvatar/${info.id}`
            } else return ''
        })
        const { proxy } = getCurrentInstance()
        const menus = ref([
            {
                icon: 'hard-drive',
                name: '我的云端硬盘',
                menuCode: 'main',
                path: '/main/all',
                allShow: true,
                children: [
                    {
                        icon: 'border-all',
                        name: '全部',
                        path: '/main/all',
                        category: 'all',
                    },
                    {
                        icon: 'video',
                        name: '视频',
                        path: '/main/VIDEO',
                        category: 'VIDEO',
                    },
                    {
                        icon: 'music',
                        name: '音频',
                        path: '/main/MUSIC',
                        category: 'MUSIC',
                    },
                    {
                        icon: 'image',
                        name: '图片',
                        path: '/main/IMAGE',
                        category: 'IMAGE',
                    },
                    {
                        icon: 'book',
                        name: '文档',
                        path: '/main/DOC',
                        category: 'DOC',
                    },
                    {
                        icon: 'ellipsis',
                        name: '其他',
                        path: '/main/OTHERS',
                        category: 'OTHERS',
                    },
                ],
            },
            {
                icon: 'square-share-nodes',
                name: '分享',
                menuCode: 'share',
                path: '/share',
                allShow: true,
            },
            {
                icon: 'trash',
                name: '回收站',
                menuCode: 'recycle',
                path: '/recycle',
            },
            {
                icon: 'gear',
                name: '设置',
                menuCode: 'setting',
                path: '/setting',
            },
        ])
        const jump = (menuItem) => {
            router.push({ path: menuItem.path })
        }
        const handleMenuClick = (menuItem) => {
            if (menuItem.children) {
                menuItem.allShow = !menuItem.allShow
                return
            }
            jump(menuItem)
        }
        const setMenu = (menuCode, path) => {
            const menu = menus.value.find((item) => {
                return item.menuCode === menuCode
            })
            currentMenu.value = menu
            currentPath.value = path
        }
        const logout = async () => {
            const result = await Swal.fire({
                title: '你确定要退出吗？',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: '确定',
                cancelButtonText: '取消',
            })

            if (result.isConfirmed) {
                const res = await proxy.Request.get(api.logout)
                if (!res) return
                proxy.VueCookies.remove('userInfo')
                proxy.VueCookies.remove('token')
                router.push('/login')
            } else {
                // 用户点击了取消按钮
            }
        }

        const addFile = async (data) => {
            const { file, filePid } = data
            popover_ref_3.value.showChange()
            await uploader.value.addFile(file, filePid)
        }
        const uploadCallbackHandle = () => {
            nextTick(() => {
                //更新用户空间
                Component.value.getData()
            })
        }
        const updateSpace = async () => {
            const res = await proxy.Request.get(api.me)
            if (res) {
                space.value.used = res.data.data.user.use_space
                space.value.total = res.data.data.user.total_space
            }
        }
        watch(
            () => route,
            (newValue, oldValue) => {
                if (newValue.meta.menuCode) {
                    setMenu(newValue.meta.menuCode, newValue.path)
                }
            },
            { immediate: true, deep: true },
        )
        return {
            proxy,
            uploader,
            popover_ref_1,
            popover_ref_2,
            popover_ref_3,
            popover_ref_4,
            popover_ref_5,
            menus,
            space,
            jump,
            isInputFocused,
            folder_isopen,
            currentMenu,
            currentPath,
            updatePwdDialog,
            handleMenuClick,
            logout,
            avatar_url,
            changePasswordDialog,
            uploadAvatarDialog,
            addFile,
            updateSpace,
            Component,
            uploadCallbackHandle,
        }
    },
}
</script>
<style lang="scss" scoped>
// 全局变量
$header-height: 64px;
$left-panel-padding: 5px;
$left-panel-width: 264px;
$bg-color: #f7f9fc;

.framework {
    position: relative;
    height: 100vh;
    width: 100vw;
    background-color: $bg-color;
    user-select: none;
    .header {
        height: $header-height;
        .logo {
            padding: 20px;
            min-width: $left-panel-width;
            span {
                margin-left: 10px;
                font-size: 1.5rem;
            }
        }
        .top-nav {
            display: flex;
            justify-content: space-between;
            flex: 1;
            height: 100%;

            .input-fragment {
                margin-top: 6.5px;
                width: 100%;
                max-width: 720px;
                height: 50px;
                border-radius: 1.875rem;
                background-color: #edf2fc;
                transition: all 0.7s cubic-bezier(0.4, 0, 0, 1);
                transition-delay: 0.2s;
                z-index: 2;
                overflow: hidden;
                .keyword-input {
                    width: 100%;
                    height: 51px;
                    line-height: 51px;
                    padding: 0 10px;
                    input {
                        width: 90%;
                        border: 0;
                        font-size: 1rem;
                        color: #000 !important;
                        &:focus {
                            border: 0;
                        }
                    }
                    span {
                        height: 40px;
                        width: 40px;
                        border-radius: 50%;
                        cursor: pointer;
                        &:hover {
                            background-color: #dee4ed;
                        }
                    }
                }
                .keyword-input {
                    border-bottom: 1px solid rgb(151, 150, 150, 0.5);
                }
                .category-list {
                    display: block;
                    width: 100%;
                    height: 50px;
                    ul {
                        list-style: none;
                        height: 100%;
                        padding: 0 10px;
                        li {
                            display: inline-block;
                            flex: 1;
                            height: 50px;
                            line-height: 50px;
                            cursor: pointer;
                            &:hover {
                                background-color: rgb(187, 187, 187, 0.3);
                            }
                            .category-block {
                                display: flex;
                                height: 50px;
                                flex-direction: column;
                                justify-content: center;
                                align-items: center;
                            }
                        }
                    }
                }
                .advanced-search {
                    display: flex;
                    justify-content: center;
                    width: 100%;
                    height: 50px;
                    border-top: 1px solid rgb(151, 150, 150, 0.5);
                }
            }
            .input-fragment.open {
                transition-duration: 0.3s;
                transition-delay: 0;
                height: 150px;
                box-shadow: 0 1px 1px 0 rgba(65, 69, 73, 0.3), 0 1px 3px 1px rgba(65, 69, 73, 0.15);
                background-color: #fff;
            }
            .btn-fragment {
                padding: 0 30px;
                .icon-block {
                    margin-left: 10px;
                    span {
                        position: relative;
                        height: 40px;
                        width: 40px;
                        border-radius: 50%;
                        cursor: pointer;
                        transition: all 0.1s ease-in-out 0.1s;

                        img {
                            width: 30px;
                            height: 30px;
                            overflow: hidden;
                            border-radius: 50%;
                        }
                    }
                    &:hover span {
                        background-color: #dee4ed;
                    }
                }
            }
        }
    }
    .container {
        position: relative;
        padding: 5px 15px 25px 0;
        display: flex;
        width: 100%;
        height: calc(100% - $header-height);
        .create {
            margin-bottom: 20px;
            button {
                border: 0;
                outline: 0;
                width: 100%;
                color: #000;
                border-radius: 25px;
                box-shadow: var(
                    --dt-surface1-shadow,
                    0 1px 2px 0 rgba(60, 64, 67, 0.3),
                    0 1px 3px 1px rgba(60, 64, 67, 0.15)
                );
                transition: transform 0.4s;
                &:hover {
                    background-color: #edf2fa;
                    box-shadow: 0 1px 2px 0 rgba(60, 64, 67, 0.3),
                        0 2px 5px 2px rgba(60, 64, 67, 0.15);
                }
                &:active {
                    transform: scale(0.96);
                }
            }
        }
        .nav-bar {
            padding: 0 20px;
            height: 100%;
            width: $left-panel-width;
            nav {
                .menu {
                    user-select: none;
                    list-style: none;
                    font-size: 0.875rem;
                    .menu-item {
                        .menu-link {
                            position: relative;
                            padding-left: 27px;
                            width: 100%;
                            height: 35px;
                            line-height: 35px;
                            border-radius: 20px;
                            cursor: pointer;

                            &.folder {
                                padding-left: 5px;
                            }
                            &:not(.active):hover {
                                background-color: #e6e8ea;
                            }
                            &.folder::before {
                                padding: auto auto;
                                content: '\25B6';
                                width: 20px;
                                height: 35px;
                                text-align: center;
                                font-size: 0.5rem;
                                display: inline-block;
                                transition: transform 0.2s ease-in-out;
                                transform: rotate(0deg);
                            }
                            &.folder.open::before {
                                transform: rotate(90deg);
                            }
                            &.open::after {
                                transform: rotate(180deg);
                            }
                            .font-icon {
                                width: 20px;
                                margin-right: 10px;
                            }
                        }

                        .sub-menu {
                            height: 0px;
                            list-style: none;
                            padding-left: 25px;
                            overflow: hidden;
                            transition: all 0.3s ease-in-out;
                            &.open {
                                height: 210px;
                            }
                            .sub-menu-item {
                                padding-left: 20px;
                                width: 100%;
                                height: 35px;
                                line-height: 35px;
                                border-radius: 20px;
                                cursor: pointer;
                                &:hover {
                                    background-color: #e6e8ea;
                                }
                                .font-icon {
                                    width: 20px;
                                    margin-right: 10px;
                                }
                            }
                        }
                    }
                }
                .active {
                    font-weight: bold;
                    background-color: #c2e7ff;
                }
            }
            .drive-space {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-top: 10px;
                .space-progress {
                    height: 4px;
                    border-radius: 5px;
                    width: 80%;
                    background-color: #bbb;
                }
                .space-info {
                    width: 100%;
                    margin: 10px 0;
                    .refresh-icon {
                        cursor: pointer;
                    }
                }
            }
        }
        .main-panel {
            position: relative;
            flex: 1;
            border-radius: 30px;
            background-color: #fff;
            overflow: hidden;
        }
    }
}
.avatar-menu-popover {
    min-width: 58px;
    width: auto;
    font-size: 0.875rem;
    outline: none;
    background: #fff;
    list-style: none;
    li {
        user-select: none;
        color: #000;
        outline: none;
        cursor: pointer;
        padding: 0 8px;
        height: 36px;
        border-radius: 5px;
        &:hover {
            background: #eaeaea;
        }
    }
}
</style>
