<template>
    <teleport to="body">
        <div class="dialog-mask" v-if="config.visible">
            <div class="dialog" :style="{ width: config.width }">
                <div class="dialog-header">{{ config.title }}</div>
                <div class="dialog-body">
                    <slot></slot>
                </div>
                <div class="dialog-footer">
                    <button v-if="config.showCancel" @click="config.close()">取消</button>
                    <button
                        v-for="(btn, index) in config.buttons"
                        :key="index"
                        @click="handleClick(btn.func)"
                    >
                        {{ btn.title }}
                    </button>
                </div>
            </div>
        </div>
    </teleport>
</template>

<script>
import { ref } from 'vue'

export default {
    name: 'Dialog',
    props: {
        config: {
            type: Object,
        },
    },
    setup(props) {
        const handleClick = (func) => {
            func()
            props.config.close()
        }
        return {
            handleClick,
        }
    },
}
</script>

<style lang="scss" scoped>
.dialog-mask {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;
    user-select: none;
    .dialog {
        background-color: #fff;
        border-radius: 4px;
        position: absolute;
        top: 35%;
        left: 50%;
        transform: translate(-50%, -50%);
        .dialog-header {
            padding: 10px 16px;
            font-size: 18px;
            font-weight: 700;
            border-bottom: 1px solid #ccc;
            text-align: center;
        }

        .dialog-body {
            padding: 16px;
        }

        .dialog-footer {
            padding: 5px 16px;
            display: flex;
            justify-content: flex-end;
            border-top: 1px solid #ccc;
            button {
                margin-left: 1rem;
            }
        }
    }
}
</style>
