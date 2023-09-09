<template>
    <div class="m-breadcrumb" :style="`height: ${height}px;`">
        <div class="m-bread" @click="backToRoot">
            <a :class="['u-route', { active: folderList.length === 0 }]">{{ baseRoute }} </a>
        </div>
        <span class="u-separator" v-if="folderList.length !== 0">/</span>
        <div class="m-bread" v-for="(folder, index) in folderList" :key="index">
            <a
                :class="['u-route', { active: index === folderList.length - 1 }]"
                @click="toPath(index + 1)"
            >
                {{ folder.fileName || '--' }}
            </a>
            <template v-if="index !== folderList.length - 1">
                <span class="u-separator">/</span>
            </template>
        </div>
    </div>
</template>
<script>
import { computed, ref, watch, getCurrentInstance } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
    name: 'Breadcrumb',
    props: {
        watchPath: {
            type: Boolean,
            default: true,
        },
        shareId: {
            type: Boolean,
        },
        adminShow: {
            type: Boolean,
            default: false,
        },
        baseRoute: {
            type: String,
        },
    },
    setup(props, { emit }) {
        const route = useRoute()
        const router = useRouter()
        const categoryId = ref()
        const folderList = ref([])
        const currentFolder = ref({
            fileId: '0',
        })

        const { proxy } = getCurrentInstance()
        const api = {
            getFolderInfo: '/file/getFolderInfo',
        }

        const callBack = () => {
            emit('breadUpdate', {
                _categoryId: categoryId.value,
                _currentFolder: currentFolder.value,
            })
        }
        const init = () => {
            currentFolder.value.fileId = '0'
            folderList.value = []
            callBack()
        }
        const setPath = () => {
            if (!props.watchPath) {
                //TODO
                return
            }
            let pathArray = []
            folderList.value.forEach((item) => {
                pathArray.push(item.fileId)
            })
            router.push({
                path: route.path,
                query: pathArray.length === 0 ? '' : { path: pathArray.join('/') },
            })
            callBack()
        }
        const getFolder = async (path) => {
            let url = api.getFolderInfo
            if (props.shareId) url = api.getFolderInfo4Share
            if (props.adminShow) url = api.getFolderInfo4Admin
            const res = await proxy.Request.get(url, {
                params: {
                    path: path,
                    shareId: props.shareId,
                },
            })
            if (res) {
                folderList.value = res.data.data.folder_info.map(
                    ({ file_id: fileId, file_name: fileName }) => ({ fileId, fileName }),
                )
            }
        }
        const backToRoot = () => {
            router.push({
                path: route.path,
                query: '',
            })
        }
        const toPath = (index) => {
            currentFolder.value = folderList.value[index]
            folderList.value = folderList.value.slice(0, index)
            setPath()
        }
        const openFolder = (data) => {
            const { file_id, file_name } = data
            const folder = {
                fileId: file_id,
                fileName: file_name,
            }
            folderList.value.push(folder)
            currentFolder.value = folder
            setPath()
        }
        watch(
            () => route,
            async (newVal, oldVal) => {
                if (!props.watchPath) return
                if (newVal.path.indexOf('/main') === -1) return
                const path = newVal.query.path
                categoryId.value = newVal.params.category
                if (path === undefined) {
                    init()
                } else {
                    await getFolder(path)
                    const pathArray = path.split('/')
                    currentFolder.value = {
                        fileId: pathArray[pathArray.length - 1],
                    }
                    callBack()
                }
            },
            { immediate: true, deep: true },
        )

        return {
            init,
            openFolder,
            folderList,
            backToRoot,
            toPath,
            currentFolder,
        }
    },
}
</script>
<style lang="scss" scoped>
.m-breadcrumb {
    display: flex;
    align-items: center;
    .m-bread {
        display: inline-flex;
        align-items: center;
        line-height: 1.5;
        .u-route {
            color: rgba(0, 0, 0, 0.45);
            font-size: 22px;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
            cursor: pointer;
            padding: 0 15px;
            border-radius: 20px;
            transition: color 0.2s, background-color 0.2s;
            &:hover {
                background-color: rgba(0, 0, 0, 0.05);
                color: rgba(0, 0, 0, 0.88);
            }
        }
        .active {
            color: rgba(0, 0, 0, 0.88);
        }

        .u-arrow {
            width: 12px;
            height: 12px;
            fill: rgba(0, 0, 0, 0.45);
        }
    }

    .assist {
        height: 100%;
        width: 0;
        display: inline-block;
        vertical-align: middle;
    }
}
.u-separator {
    margin: 0 10px;
    color: rgba(0, 0, 0, 0.45);
}
</style>
