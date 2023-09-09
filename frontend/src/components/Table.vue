<template>
    <div class="table-container" @contextmenu.prevent>
        <table>
            <thead>
                <slot name="thead"></slot>
            </thead>
            <tbody @click.stop>
                <slot name="tbody"></slot>
            </tbody>
        </table>
        <div class="pagination">
            <span :class="{ disabled: options.currentPage === 1 }" @click="currentPage--">
                <font-awesome-icon icon="chevron-left" size="xs" />
            </span>
            <!-- 左侧 -->
            <span
                v-for="pageNumber in left_pagination"
                :key="pageNumber"
                @click="options.currentPage = pageNumber"
            >
                {{ pageNumber }}
            </span>
            <!-- 选中 -->
            <span class="current">{{ options.currentPage }}</span>
            <!-- 左侧 -->
            <span
                v-for="pageNumber in right_pagination"
                :key="pageNumber"
                @click="options.currentPage = pageNumber"
            >
                {{ pageNumber }}
            </span>
            <span
                :class="{ disabled: options.currentPage === options.pageCount }"
                @click="currentPage = pageCount"
            >
                <font-awesome-icon icon="chevron-right" size="xs" />
            </span>

            <div class="jump">Go to<input type="number" v-model="jumpToPage" /></div>
        </div>
    </div>
</template>

<script>
import { toRefs, ref, computed, onMounted, onUnmounted, getCurrentInstance } from 'vue'
import rowIcon from './rowIcon.vue'
/*TODO: 文件框选 */

export default {
    props: {
        options: {
            type: Object,
            required: true,
        },
    },
    components: { rowIcon },
    setup(props) {
        const { proxy } = getCurrentInstance()
        const jumpToPage = ref(1)
        const left_pagination = computed(() => {
            const start = Math.max(1, props.options.currentPage - 4)
            return Array.from({ length: props.options.currentPage - start }, (_, i) => i + start)
        })
        const right_pagination = computed(() => {
            const start = props.options.currentPage + 1
            const end = Math.min(start + 3, props.options.pageCount)
            return Array.from({ length: end - start + 1 }, (_, i) => i + start)
        })
        function handleJump() {
            if (jumpToPage.value >= 1 && jumpToPage.value <= pageCount.value) {
                currentPage.value = jumpToPage.value
            }
        }

        return {
            proxy,
            handleJump,
            left_pagination,
            right_pagination,
            jumpToPage,
        }
    },
}
</script>
<style lang="scss">
.table-container {
    padding: 0 20px;
    table {
        margin: 20px 0 0 0;
        width: 100%;
        border-spacing: 0;
        color: #666;
        font-size: 12px;
        border-collapse: collapse;

        th {
            // padding: 10px 8px;
            text-align: left;
            vertical-align: inherit;
            color: #666;
            font-weight: normal;
        }
        td {
            // padding: 10px 8px;
            text-align: left;
            white-space: nowrap; /* 防止文字换行 */
            text-overflow: ellipsis; /* 使用省略号代替溢出部分 */
            input {
                height: 100%;
            }
            &.row-slot div {
                visibility: hidden;
            }
        }
        tr {
            font-size: 0.875rem;
            height: 45px;
            border-bottom: 0.5px solid #c9c7c7;
            cursor: pointer;
            &:hover .table-btns {
                visibility: visible;
            }
            &.selected {
                background-color: #c2e7ff;
            }
        }
        tbody tr {
            cursor: pointer;
            &:not(.selected):hover {
                background-color: #f5f5f5;
            }
        }
    }
    .pagination {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        margin-top: 20px;
        span {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 35px;
            padding: 0 13px;
            cursor: pointer;
            &.current {
                color: #409eff;
                font-weight: bold;
                cursor: auto;
            }
            &.disabled {
                cursor: not-allowed;
            }
            &:not(.disabled):hover {
                color: #409eff;
            }
        }
        div.jump {
            height: 35px;
            padding: 0 13px;
            input {
                margin: 0 10px;
                height: 100%;
                width: 50px;
                text-align: center;
                -webkit-appearance: none;
                &:focus {
                    border-color: #409eff;
                    outline: 0;
                }
                &::-webkit-inner-spin-button {
                    -webkit-appearance: none;
                }
            }
        }
    }
}
</style>
