<template>
    <div class="share">
        <div class="header flex-start">
            <div class="title" v-if="options.selectedRow.length === 0">
                <span>我的分享</span>
            </div>
            <div class="ops flex-start" v-else>
                <span class="flex-center" @click.stop="handleRemove">
                    <font-awesome-icon icon="x" />
                </span>
                <p>已选择{{ options.selectedRow.length }}项内容</p>
                <span class="flex-center" @click.stop="handleShare">
                    <font-awesome-icon icon="arrow-up-right-from-square" />
                </span>
                <span class="flex-center" @click.stop="handleDelete">
                    <font-awesome-icon icon="trash" />
                </span>
            </div>
        </div>
        <div class="content">
            <Table :options="options">
                <template v-slot:thead>
                    <tr>
                        <th v-if="options.icon" style="width: 50px"></th>
                        <th v-for="(column, index) in options.columns" :key="index">
                            {{ column.label }}
                        </th>
                        <th></th>
                    </tr>
                </template>
                <template v-slot:tbody>
                    <tr
                        v-for="(row, index) in options.rows"
                        :key="index"
                        :class="{ selected: options.selectedRow.includes(row) }"
                        @click="selectRow(row)"
                        @dblclick="handleDblclick(row)"
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
        </div>
    </div>
</template>
<script setup>
import Swal from 'sweetalert2'
import useClipboard from 'vue-clipboard3'
const { toClipboard } = useClipboard()
import { ref, getCurrentInstance, onMounted, onUnmounted, defineAsyncComponent } from 'vue'
const Table = defineAsyncComponent(() => import('@/components/Table.vue'))
const rowIcon = defineAsyncComponent(() => import('@/components/rowIcon.vue'))
const api = {
    getShareList: '/share/getShareList',
    cancelShare: '/share/cancelShare',
}
const { proxy } = getCurrentInstance()
const isShift = ref(false)
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
            label: '分享时间',
            key: 'share_time',
        },
        {
            label: '失效时间',
            key: 'expired_time',
        },
        {
            label: '浏览量',
            key: 'show_count',
        },
    ],
    rows: [],
    selectedRow: [],
})
const getData = async () => {
    const result = await proxy.Request.get(api.getShareList, {
        params: {
            page: options.value.currentPage,
            limit: options.value.pageSize,
        },
    })
    if (result) {
        const shares = result.data.data.shares
        const files = result.data.data.files
        options.value.rows = shares.map((item, index) => ({
            ...item,
            ...files[index],
            share_time: proxy.Utils.datetime2str(item.share_time),
            expired_time: proxy.Utils.datetime2str(item.expired_time),
        }))
    }
}
const selectRow = (row) => {
    const index = options.value.selectedRow.findIndex((item) => item === row)
    if (isShift.value) {
        if (index !== -1) {
            options.value.selectedRow.splice(index, 1)
        } else options.value.selectedRow.push(row)
    } else {
        options.value.selectedRow = index === -1 ? [row] : []
    }
}
const handleDblclick = (row) => {
    const url = 'http://localhost:7070/share/' + row.share_id
    const code = row.code
    Swal.fire({
        title: '分享',
        html:
            '<div class="line">' +
            '<span>分享链接</span>' +
            url +
            '</div>' +
            '<div class="line">' +
            '<span>提取码</span>' +
            code +
            '</div>',
        focusConfirm: false,
    }).then(async (result) => {
        if (result.isConfirmed) {
            await toClipboard(`链接:${url} 提取码:${code}`)
        }
    })
}
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
const handleMouseDown = (event) => {
    // 点击了表格之外的区域，取消选中行
    options.value.selectedRow = []
}
const deleteRow = (row) => {
    Swal.fire({
        title: '你确定撤销分享吗?',
        showDenyButton: true,
        reverseButtons: true,
        showCancelButton: true,
        confirmButtonText: 'Revoke',
        denyButtonText: `Don't revoke`,
    }).then(async (result) => {
        if (result.isConfirmed) {
            let shareIds
            if (Array.isArray(row)) {
                // 如果是数组则批量删除
                shareIds = row.map((item) => item.share_id).join(',')
            } else {
                shareIds = row.share_id
            }
            const res = await proxy.Request.post(api.cancelShare, `${shareIds}`, {
                showLoading: true,
            })
            if (res) {
                Swal.fire('Deleted!', '', 'success')
            }
        } else if (result.isDenied) {
            Swal.fire('Deletes are not implemented', '', 'info')
        }
    })
}
onMounted(async () => {
    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('keyup', handleKeyUp)
    document.addEventListener('click', handleMouseDown)
    await getData()
})
</script>
<style lang="scss" scoped>
.share {
    display: flex;
    flex-direction: column;
    padding: 20px 10px;
    width: 100%;
    height: 100%;
    user-select: none;
    .header {
        margin-left: 20px;
        height: 40px;
        line-height: 40px;
        color: rgba(0, 0, 0, 0.88);
        .title {
            font-size: 22px;
        }
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
}
</style>
