import { createStore } from 'vuex'

export default createStore({
    state: {
        contextMenus: [],
    },
    mutations: {
        addMenu(state, menuRef) {
            state.contextMenus.push(menuRef)
        },
        hideAllMenus(state) {
            state.contextMenus.forEach((element) => {
                element.value = false
            })
        },
    },
})
