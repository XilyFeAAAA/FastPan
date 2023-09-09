<template>
    <div>
        <transition name="fade">
            <div class="context-menu" v-show="show" :style="{ top: y + 'px', left: x + 'px' }">
                <div class="menu-item" v-for="(item, idx) in menuItems" :key="idx">
                    <div
                        class="sub-menu-item"
                        v-for="(sub_item, idx) in item"
                        :key="idx"
                        @click="sub_item.onClick"
                    >
                        <font-awesome-icon :icon="sub_item.icon" class="icon" />{{ sub_item.text }}
                    </div>
                </div>
            </div>
        </transition>
        <div class="content" style="height: 100%" @contextmenu="handleContextMenu">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useStore } from 'vuex'
export default {
    name: 'ContextMenu',
    props: {
        menuItems: {
            type: Array,
            required: true,
        },
        showMenu: Function,
    },
    setup(props) {
        const x = ref()
        const y = ref()
        const show = ref(false)
        const Wrapper = ref()
        const store = useStore()
        const handleContextMenu = (event) => {
            event.preventDefault()
            x.value = event.clientX
            y.value = event.clientY
            store.commit('hideAllMenus')
            show.value = true
        }

        const hideMenu = () => {
            show.value = false
        }

        onMounted(() => {
            store.commit('addMenu', show)
            document.addEventListener('click', hideMenu)
        })

        return {
            x,
            y,
            show,
            Wrapper,
            handleContextMenu,
        }
    },
}
</script>

<style lang="scss" scoped>
.context-menu {
    position: fixed;
    padding: 10px 0;
    z-index: 10;
    width: 230px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: height 0.5s all;
}
.menu-item {
    padding: 5px 0;
}

.menu-item:not(:last-child) {
    padding: 5px 0;
    border-bottom: 1px solid rgb(0, 0, 0, 0.3);
}
.sub-menu-item {
    padding: 0 1.5rem;
    font-size: 0.875rem;
    height: 30px;
    line-height: 30px;
    cursor: pointer;
    .icon {
        width: 20px;
        margin-right: 15px;
    }
}

.sub-menu-item:hover {
    background: #eee;
}
</style>
