<template>
    <form @submit.prevent="handleSubmit">
        <slot></slot>
    </form>
</template>

<script setup>
import { ref, watchEffect } from 'vue'

const emitFn = defineEmits(['validation'])

const formInputs = ref([])

const registerInput = (input) => {
    formInputs.value.push(input)
}

const unregisterInput = (input) => {
    const index = formInputs.value.findIndex((i) => i.name === input.name)
    if (index !== -1) {
        formInputs.value.splice(index, 1)
    }
}

const validateInputs = () => {
    let valid = true
    formInputs.value.forEach((input) => {
        if (input.rule) {
            const res = input.validate()
            if (res !== true) {
                valid = false
            }
        }
    })
    return valid
}

const handleSubmit = () => {
    const isValid = validateInputs()
    emitFn('validation', isValid)
    if (isValid) {
        const formData = formInputs.value.reduce((acc, input) => {
            acc[input.name] = input.value
            return acc
        }, {})
        emitFn('submit', formData)
    }
}

watchEffect(() => {
    provide('registerInput', registerInput)
    provide('unregisterInput', unregisterInput)
})
</script>
