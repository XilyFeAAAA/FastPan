<template>
    <div class="input-container">
        <input
            :type="type"
            :value="value"
            :placeholder="placeholder"
            :style="{ ...inputStyle }"
            :class="{ 'is-invalid': inputRef.error }"
            @input="input"
            @blur="handleBlur"
        />
        <div v-if="inputRef.error" class="error-text">
            {{ inputRef.message }}
        </div>
    </div>
</template>
<script setup>
import { reactive } from 'vue'
import { itemValidator } from '../utils/Validator.js'
const emitFn = defineEmits(['update'])
const props = defineProps({
    type: {
        type: String,
        default: 'text',
    },
    name: String,
    value: String,
    placeholder: String,
    rule: Object,
    inputStyle: Object,
})
const inputRef = reactive({
    error: false,
    message: '',
})
const handleBlur = () => {
    const res = itemValidator(props.value, props.rule)
    if (res === true) inputRef.error = false
    else {
        inputRef.error = true
        inputRef.message = res
    }
}

const input = (e) => {
    const targetValue = e.target.value
    emitFn('update', { name: props.name, value: targetValue }) // 传回一个对象
}
</script>
<style lang="scss" scoped>
.input-container {
    width: 100%;
}
input {
    width: 100%;
    &.is-invalid {
        border: 1px solid red;
    }
}
.error-text {
    padding-left: 5px;
    font-size: 8px;
    color: red;
    text-align: left;
}
</style>
