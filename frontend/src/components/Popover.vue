<template>
    <div ref="popover" class="popover">
        <transition name="fade">
            <div
                v-show="show"
                ref="contentWrapper"
                class="content-wrapper"
                :class="{ 'no-triangle': !showTriangle }"
                :data-orient="orient"
            >
                <slot name="content"></slot>
            </div>
        </transition>
        <span ref="triggerWrapper">
            <slot></slot>
        </span>
    </div>
</template>

<script>
export default {
    name: 'Popover',
    props: {
        orient: {
            type: String,
            default: 'top',
        },
        showTriangle: {
            type: Boolean,
            default: true,
        },
        method: {
            type: String,
            default: 'click',
        },
    },
    data() {
        return {
            show: false,
        }
    },
    methods: {
        position() {
            document.body.appendChild(this.$refs.contentWrapper)

            const triggerRect = this.$refs.triggerWrapper.getBoundingClientRect()
            const contentRect = this.$refs.contentWrapper.getBoundingClientRect()
            let left = 0,
                top = 0
            switch (this.orient) {
                case 'top':
                    left = triggerRect.left + (triggerRect.width - contentRect.width) / 2
                    top = triggerRect.top + window.scrollY - 10
                    break
                case 'bottom':
                    left = triggerRect.left + (triggerRect.width - contentRect.width) / 2
                    top = triggerRect.bottom + contentRect.height
                    break
                case 'left':
                    left = triggerRect.left - contentRect.width - 10
                    top =
                        triggerRect.top +
                        contentRect.height +
                        (triggerRect.height - contentRect.height) / 2
                    break
                case 'right':
                    left = triggerRect.right + 10
                    top =
                        triggerRect.top +
                        contentRect.height +
                        (triggerRect.height - contentRect.height) / 2
                    break
            }
            // 边缘检测
            if (top < 0) top = 5
            else if (top + contentRect.height > window.innerHeight)
                top = window.innerHeight - contentRect.height - 5
            if (left < 0) left = 5
            else if (left + contentRect.width > window.innerWidth)
                left = window.innerWidth - contentRect.width - 5
            this.$refs.contentWrapper.style.left = `${left}px`
            this.$refs.contentWrapper.style.top = `${top}px`
        },
        listener(event) {
            if (
                (this.$refs.popover && this.$refs.popover.contains(event.target)) ||
                this.$refs.popover === event.target
            ) {
                return
            }
            if (
                (this.$refs.contentWrapper && this.$refs.contentWrapper.contains(event.target)) ||
                this.$refs.contentWrapper === event.target
            ) {
                return
            }
            this.close()
        },
        close() {
            this.show = false
            document.removeEventListener('click', this.listener)
        },
        open() {
            this.show = true
            this.$nextTick(() => {
                this.position()
                document.addEventListener('click', this.listener)
            })
        },
        showChange() {
            // if (this.$refs.triggerWrapper.contains(event.target)) {
            if (this.show === true) {
                this.close()
            } else {
                this.open()
            }
            // }
        },
    },
}
</script>

<style lang="scss" scoped>
.popover {
    display: inline-block;
    position: relative;
}

.content-wrapper {
    position: absolute;
    padding: 6px;
    border: 1px solid #ebeef5;
    box-shadow: 0 2px 15px 0 rgba(0, 0, 0, 0.1);
    background: white;
    transform: translateY(-100%);
    z-index: 3;
}

.content-wrapper::before {
    content: ' ';
    height: 0;
    position: absolute;
    width: 0;
    border: 10px solid transparent; /* arrow size */
}

.content-wrapper.no-triangle::before {
    display: none;
}

.content-wrapper[data-orient='bottom']::before {
    border-bottom-color: #fff;
    position: absolute;
    top: 0;
    left: 50%;
    transform: translate(-50%, -100%);
    z-index: 2;
}

.content-wrapper[data-orient='left']::before {
    border-left-color: #fff;
    position: absolute;
    top: 50%;
    right: 0;
    transform: translate(100%, -50%);
    z-index: 2;
}

.content-wrapper[data-orient='right']::before {
    border-right-color: #fff;
    position: absolute;
    top: 50%;
    left: 0;
    transform: translate(-100%, -50%);
    z-index: 2;
}

.content-wrapper[data-orient='top']::before {
    border-top-color: #fff;
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translate(-50%, 100%);
    z-index: 2;
}
</style>
