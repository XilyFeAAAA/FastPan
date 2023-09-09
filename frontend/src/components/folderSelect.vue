<template>
    <Dialog :config="dialogConfig4folderSelect">
        <div class="breadcrumb-panel"></div>
        <div class="folder-list" v-if="folderList.length > 0">
            <div
                class="folder-item flex-start"
                :class="{ select: targetFolder == item }"
                v-for="(item, index) in folderList"
                :key="index"
                @click.stop="handleClick(item)"
                @dblclick.stop="handleDblclick(item)"
            >
                <rowIcon />
                <span class="file-name">{{ item.file_name }}</span>
            </div>
        </div>
        <div v-else class="else flex-center">当前目录为空</div>
    </Dialog>
</template>
<script setup>
import rowIcon from '@/components/rowIcon.vue'
import Breadcrumb from './Breadcrumb.vue'
import Dialog from './Dialog.vue'
import { ref, getCurrentInstance, defineEmits } from 'vue'
const { proxy } = getCurrentInstance()
const api = {
    loadAllFolder: '/file/loadAllFolder',
}
const selectFileIds = ref([])
const targetFolder = ref({})
const currentFolder = ref({})
const folderList = ref([])
const emits = defineEmits(['handleFileMove'])
const loadAllFolder = async () => {
    const res = await proxy.Request.get(api.loadAllFolder, {
        params: {
            filePid: currentFolder.value.fileId,
        },
    })
    if (!res) return
    folderList.value = res.data.data.folder.filter(
        (item) => selectFileIds.value.indexOf(item.file_id) === -1,
    )
}
const dialogConfig4folderSelect = ref({
    title: '移动到',
    width: '400px',
    visible: false,
    showCancel: true,
    buttons: [
        {
            title: '移动到此',
            func() {
                emits('handleFileMove', targetFolder.value.file_id)
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
const showFolderDialog = (_currentFolder, _selectFileIds) => {
    currentFolder.value = _currentFolder
    selectFileIds.value = _selectFileIds
    dialogConfig4folderSelect.value.show(currentFolder.file)
    loadAllFolder()
}

const handleClick = (item) => {
    targetFolder.value = item
}
const handleDblclick = async (item) => {
    // 进入子目录后，选择的目录清空
    targetFolder.value = null
    currentFolder.value = {
        fileId: item.file_id,
        fileName: item.file_name,
    }
    await loadAllFolder()
}

const breadUpdate = async (data) => {
    const { _currentFolder } = data
    currentFolder.value = _currentFolder
    await loadAllFolder()
}
defineExpose({
    showFolderDialog,
})
</script>

<style lang="scss" scoped>
.breadcrumb-panel {
    padding-left: 10px;
    background-color: #f1f1f1;
}
.folder-list {
    max-height: calc(100vh - 200px);
    min-height: 200px;
    .folder-item {
        cursor: pointer;
        padding: 10px;
        .file-name {
            display: inline-block;
            margin-left: 10px;
        }
        &.select,
        &:hover {
            background-color: #e0dfdf;
        }
    }
}
.else {
    font-size: 0.875rem;
}
.tips {
    text-align: center;
    line-height: 200px;
    span {
        color: #06a7ff;
    }
}
</style>
