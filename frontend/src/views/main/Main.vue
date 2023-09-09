<template>
    <div class="main">
        <div class="header flex-start">
            <div class="bread" v-show="options.selectedRow.length === 0">
                <Breadcrumb ref="breadRef" baseRoute="我的云端硬盘" @breadUpdate="breadUpdate" />
            </div>
            <div class="ops flex-start" v-show="options.selectedRow.length !== 0">
                <span class="flex-center" @click.stop="handleRemove">
                    <font-awesome-icon icon="x" />
                </span>
                <p>已选择{{ options.selectedRow.length }}项内容</p>
                <span class="flex-center" @click.stop="handleShare">
                    <font-awesome-icon icon="arrow-up-right-from-square" />
                </span>
                <span class="flex-center" @click.stop="handleDownload">
                    <font-awesome-icon icon="download" />
                </span>
                <span class="flex-center" @click.stop="handleMove">
                    <font-awesome-icon icon="file-export" />
                </span>
                <span class="flex-center" @click.stop="handleDelete">
                    <font-awesome-icon icon="trash" />
                </span>
                <span class="flex-center" @click.stop="handleLink">
                    <font-awesome-icon icon="link" />
                </span>
            </div>
        </div>
        <div class="content">
            <context-menu :menu-items="tableMenuItem">
                <Table :options="options" ref="tableRef">
                    <template v-slot:thead>
                        <tr>
                            <th v-if="options.icon" style="width: 50px"></th>
                            <th v-for="(column, index) in options.columns" :key="index">
                                {{ column.label }}
                            </th>
                            <th style="width: 150px"></th>
                        </tr>
                    </template>
                    <template v-slot:tbody>
                        <tr
                            v-for="(row, index) in options.rows"
                            :key="index"
                            :class="{ selected: options.selectedRow.includes(row) }"
                            :draggable="options.selectedRow.includes(row) ? 'true' : 'false'"
                            @click="selectRow(row)"
                            @dblclick="handleDblclick(row)"
                            @contextmenu.prevent="selectRow(row)"
                            @dragover.prevent
                            @drop="handleDrop($event, index)"
                        >
                            <td v-if="options.icon" style="text-align: center">
                                <rowIcon
                                    width="20px"
                                    :folder_type="row.folder_type"
                                    :file_type="row.file_type"
                                    :status="row.status"
                                    :cover="row.file_cover"
                                />
                            </td>
                            <td v-for="(column, c_index) in options.columns" :key="c_index">
                                {{
                                    column.key === 'file_size' && row[column.key] !== null
                                        ? proxy.Utils.sizeToStr(row[column.key])
                                        : row[column.key]
                                }}
                                <span
                                    v-if="row.status !== 3 && column.key === 'file_name'"
                                    style="font-size: 0.5rem"
                                    :style="{ color: row.status === 1 ? 'green' : 'red' }"
                                >
                                    {{ row.status === 1 ? '转码中' : '转码失败' }}
                                </span>
                            </td>
                            <td>
                                <div class="table-btns">
                                    <span class="flex-center" @click="shareRow(row)">
                                        <font-awesome-icon :icon="['far', 'share-from-square']" />
                                    </span>
                                    <span class="flex-center" @click="downloadRow(row)">
                                        <font-awesome-icon icon="download" />
                                    </span>
                                    <span class="flex-center" @click="renameRow(row)">
                                        <font-awesome-icon icon="pen-to-square" />
                                    </span>
                                    <span class="flex-center" @click="deleteRow(row)">
                                        <font-awesome-icon icon="trash" />
                                    </span>
                                </div>
                            </td>
                        </tr>
                    </template>
                </Table>
            </context-menu>
            <context-menu :menu-items="blankMenuItem" style="height: 100%"></context-menu>
        </div>
        <Preview ref="previewRef" />
        <fileShare ref="fileShareRef" />
        <folderSelect ref="folderSelectRef" @handleFileMove="handleFileMove" />
    </div>
</template>
<script setup>
import Swal from 'sweetalert2'
import { ref, defineAsyncComponent, getCurrentInstance, onMounted, onUnmounted } from 'vue'
const Breadcrumb = defineAsyncComponent(() => import('@/components/Breadcrumb.vue'))
const contextMenu = defineAsyncComponent(() => import('@/components/contextMenu.vue'))
const Table = defineAsyncComponent(() => import('@/components/Table.vue'))
const Preview = defineAsyncComponent(() => import('@/components/preview/Preview.vue'))
const folderSelect = defineAsyncComponent(() => import('@/components/folderSelect.vue'))
const fileShare = defineAsyncComponent(() => import('@/views/main/fileShare.vue'))
const rowIcon = defineAsyncComponent(() => import('@/components/rowIcon.vue'))
const emit = defineEmits(['addFile', 'updateSpace'])
const data = ref({})
const currentFolder = ref({
    fileId: '0',
})
const folderSelectRef = ref()
const categoryId = ref()
const { proxy } = getCurrentInstance()
const api = {
    getData: '/file',
    newFolder: '/file/newFolder',
    rename: '/file/renameFile',
    delFile: '/file/delFile',
    createDownloadUrl: '/file/createDownloadUrl',
    downloadUrl: 'http://localhost:7070/api/v1/file/download',
    fileMove: '/file/moveFile',
}
const generateUid = () => {
    let timestamp = new Date().getTime().toString(36)
    let randomStr = Math.random().toString(36).substr(2, 5)
    let uid = `${timestamp}${randomStr}`
    return uid
}
const addFile = async () => {
    const input = document.createElement('input')
    input.type = 'file'
    // 监听 input 元素的 change 事件
    input.addEventListener('change', () => {
        if (input.files.length > 0) {
            const file = input.files[0]
            file.uid = generateUid()
            emit('addFile', {
                file: file,
                filePid: currentFolder.value.fileId,
            })
        }
    })
    input.click()
}
const blankMenuItem = [
    [
        { text: '新建文件夹', icon: 'folder', onClick: () => createNewFolder() },
        {
            text: '刷新',
            icon: 'rotate-right',
            onClick: async () => {
                await refresh()
            },
        },
        { text: '排序方式', icon: 'arrow-up-z-a', onClick: () => {} },
    ],
    [
        { text: '上传文件', icon: 'file', onClick: () => addFile() },
        { text: '上传文件夹', icon: 'upload', onClick: () => {} },
    ],
    [
        { text: 'Google文档', icon: 'file-word', onClick: () => {} },
        { text: 'Google表格', icon: 'file-excel', onClick: () => {} },
    ],
]
const tableMenuItem = [
    [{ text: '预览', icon: 'eye', onClick: () => {} }],
    [
        { text: '共享', icon: 'share', onClick: () => {} },
        { text: '复制链接', icon: 'copy', onClick: () => {} },
        { text: '添加星标', icon: 'star', onClick: () => {} },
        { text: '重命名', icon: 'pen', onClick: () => {} },
    ],
    [
        { text: '查看详细信息', icon: 'share', onClick: () => {} },
        { text: '下载', icon: 'copy', onClick: () => {} },
    ],
    [{ text: '删除', icon: 'trash', onClick: () => {} }],
]
const options = ref({
    icon: true,
    currentPage: 1,
    pageSize: 20,
    pageCount: 1,
    columns: [
        {
            label: '名称',
            key: 'file_name',
        },
        {
            label: '上次更新时间',
            key: 'last_update_time',
        },
        {
            label: '大小',
            key: 'file_size',
        },
    ],
    columnWidths: ['40%', '20%', '20%', '20%'],
    rows: [],
    selectedRow: [],
})
const fileShareRef = ref()
const shareRow = async (row) => {
    fileShareRef.value.showFileShareDialog(row)
}
const downloadRow = async (row) => {
    if (row.folder_type == 0) await download(row.file_id)
}
const fileNameFuzzy = ref()
const getData = async () => {
    let params = {
        category: categoryId.value === 'all' ? null : categoryId.value,
        filePid: currentFolder.value.fileId,
        page: options.value.currentPage,
        limit: options.value.pageSize,
        fileNameFuzzy: fileNameFuzzy.value,
    }
    const result = await proxy.Request.get(api.getData, {
        params: params,
    })
    if (result) {
        options.value.rows = result.data.data.files
    }
}
const refresh = async () => {
    await getData()
    emit('updateSpace')
}
const breadUpdate = async (data) => {
    const { _currentFolder, _categoryId } = data
    currentFolder.value = _currentFolder
    categoryId.value = _categoryId
    await refresh()
}

const createNewFolder = () => {
    Swal.fire({
        title: '请输入新文件夹的名称',
        input: 'text',
        inputPlaceholder: '请输入文件夹名称',
        showCancelButton: true,
        confirmButtonText: '创建',
        cancelButtonText: '取消',
        reverseButtons: true,
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: true,
        inputValidator: (value) => {
            if (!value) return '请输入文件夹名称'
            else if (/[\|\\\/\?\*<>:"]/.test(value)) return '文件夹不得包含特殊字符 | / \ ? * < > :'
        },
    }).then(async (result) => {
        if (result.isConfirmed) {
            // 用户点击了确认按钮，可以在这里处理输入的文件夹名称
            const folderName = result.value
            await proxy.Request.post(api.newFolder, {
                filePid: currentFolder.value.fileId,
                fileName: folderName,
            })
            await getData()
        }
    })
}
const renameRow = async (row) => {
    Swal.fire({
        title: '请输入文件新名称',
        input: 'text',
        inputValue: row.file_name,
        inputPlaceholder: '请输入文件名称',
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        reverseButtons: true,
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: true,
        inputValidator: (value) => {
            if (!value) return '请输入文件名称'
            else if (/[\|\\\/\?\*<>:"]/.test(value)) return '文件不得包含特殊字符 | / \ ? * < > :'
        },
    }).then(async (result) => {
        if (result.isConfirmed) {
            const newFileName = result.value
            await proxy.Request.post(api.rename, {
                fileId: row.file_id,
                newFileName: newFileName,
            })
            await refresh()
            Swal.fire('Renamed!', '', 'success')
        } else if (result.isDenied) {
            Swal.fire('Rename is not implemented', '', 'info')
        }
    })
}
const deleteRow = (row) => {
    Swal.fire({
        title: '你确定删除文件吗?',
        showDenyButton: true,
        reverseButtons: true,
        showCancelButton: true,
        confirmButtonText: 'Delete',
        denyButtonText: `Don't delete`,
    }).then(async (result) => {
        if (result.isConfirmed) {
            let fileIds
            if (Array.isArray(row)) {
                // 如果是数组则批量删除
                fileIds = row.map((item) => item.file_id).join(',')
            } else {
                fileIds = row.file_id
            }
            const res = await proxy.Request.post(api.delFile, `${fileIds}`, {
                showLoading: true,
            })
            if (res) {
                await refresh()
                Swal.fire('Deleted!', '', 'success')
            }
        } else if (result.isDenied) {
            Swal.fire('Deletes are not implemented', '', 'info')
        }
    })
}
const breadRef = ref()
const previewRef = ref()
const handleDblclick = (row) => {
    options.value.selectedRow = []
    // 目录则进入
    if (row.folder_type === 1) {
        breadRef.value.openFolder(row)
        return
    }
    // 文件则预览
    if (row.status !== 3) {
        Swal.fire('文件未完成转码', '', 'warning')
    } else {
        previewRef.value.showPreview(row, 0)
    }
}
const handleRemove = (event) => {
    event.stopPropagation() // 阻止事件冒泡
    options.value.selectedRow = []
}
const handleShare = async (event) => {
    event.stopPropagation() // 阻止事件冒泡
}
const handleDelete = (event) => {
    event.stopPropagation() // 阻止事件冒泡
    deleteRow(options.value.selectedRow)
}
const handleDownload = (event) => {
    event.stopPropagation() // 阻止事件冒泡
    options.value.selectedRow.forEach(async (row) => {
        if (row.folder_type == 0) await download(row.file_id)
    })
}
const handleMove = async (event) => {
    event.stopPropagation() // 阻止事件冒泡
    folderSelectRef.value.showFolderDialog(
        currentFolder.value,
        options.value.selectedRow.map((row) => row.file_id),
    )
}
const handleLink = async (event) => {
    event.stopPropagation() // 阻止事件冒泡
}
const download = async (fileId) => {
    const res = await proxy.Request.get(api.createDownloadUrl + '/' + fileId)
    if (res) {
        window.location.href = api.downloadUrl + '/' + res.data.data.code
    }
}
const handleFileMove = async (folderId) => {
    const fileIds = options.value.selectedRow.map((row) => row.file_id).join(',')
    const res = await proxy.Request.post(api.fileMove, {
        fileIds: fileIds,
        targetFolderId: folderId,
    })
    if (!res) return
    // 移动结束清除选择
    options.value.selectedRow = []
    await refresh()
}

// Table部分逻辑
const isShift = ref()
const tableRef = ref()
onMounted(() => {
    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('keyup', handleKeyUp)
    document.addEventListener('click', handleMouseDown)
})
onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown)
    window.removeEventListener('keyup', handleKeyUp)
    document.removeEventListener('click', handleMouseDown)
})
const handleKeyDown = (e) => {
    if (e.key === 'Shift') {
        isShift.value = true
    }
}
const handleKeyUp = (e) => {
    if (e.key === 'Shift') {
        isShift.value = false
    }
}
function selectRow(row) {
    const index = options.value.selectedRow.findIndex((item) => item === row)
    if (isShift.value) {
        if (index !== -1) {
            options.value.selectedRow.splice(index, 1)
        } else options.value.selectedRow.push(row)
    } else {
        options.value.selectedRow = index === -1 ? [row] : []
    }
}
const handleMouseDown = (event) => {
    // 点击了表格之外的区域，取消选中行
    options.value.selectedRow = []
}
const handleDrop = async (event, index) => {
    event.preventDefault()
    // 拖拽到文件上不移动
    const targetFolder = options.value.rows[index]
    if (targetFolder.folder_type === 0) return
    await handleFileMove(targetFolder.file_id)
}
</script>
<style lang="scss" scoped>
.main {
    display: flex;
    flex-direction: column;
    padding: 20px 10px;
    width: 100%;
    height: 100%;
    user-select: none;
    .header {
        height: 40px;
        line-height: 40px;
        .ops {
            padding: 0 10px;
            span {
                margin: 0 10px;
                border-radius: 50%;
                height: 40px;
                width: 40px;
                cursor: pointer;
                &:hover {
                    background-color: rgb(102, 102, 102, 0.1);
                }
            }
        }
    }
    .content {
        flex: 1;
    }
}
.table-btns {
    display: flex;
    align-items: center;
    justify-content: center;
    visibility: hidden;
    span {
        height: 30px;
        width: 30px;
        border-radius: 50%;
        cursor: pointer;
        &:hover {
            background-color: #dfdfdf;
        }
    }
}
</style>
