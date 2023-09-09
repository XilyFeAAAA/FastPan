const itemValidator = (fieldValue, rule) => {
    for (let ruleName in rule) {
        const ruleValue = rule[ruleName]
        switch (ruleName) {
            case 'required':
                if (ruleValue && !fieldValue) {
                    return `The field  is required`
                }
                break
            case 'minLength':
                if (ruleValue && fieldValue.length < ruleValue) {
                    return `The field has a minLengh of ${ruleValue}`
                }
                break
            case 'maxLength':
                if (ruleValue && fieldValue.length > ruleValue) {
                    return `The field has a maxLengh of ${ruleValue}`
                }
                break
            case 'email':
                if (ruleValue && !isValidEmail(fieldValue)) {
                    return `The field must be email`
                }
                break
            case 'pattern':
                if (ruleValue && !new RegExp(ruleValue).test(fieldValue)) {
                    return `The field doesn't match the pattern`
                }
                break
            case 'confirm':
                if (ruleValue && fieldValue !== formField[ruleValue]) {
                    return `The field ${fieldName} must match ${ruleValue}`
                }
                break
            // 可以根据需要添加其他验证规则
            default:
                break
        }
    }
    return true
}

// 对整个表单验证
const formValidator = (formField, rules) => {
    for (let fieldName in rules) {
        const fieldValue = formField[fieldName]
        const rule = rules[fieldName]
        for (let ruleName in rule) {
            const ruleValue = rule[ruleName]
            switch (ruleName) {
                case 'required':
                    if (ruleValue && !fieldValue) {
                        return `The field ${fieldName} is required`
                    }
                    break
                case 'minLength':
                    if (ruleValue && fieldValue.length < ruleValue) {
                        return `The field ${fieldName} has a minLengh of ${ruleValue}`
                    }
                    break
                case 'maxLength':
                    if (ruleValue && fieldValue.length > ruleValue) {
                        return `The field ${fieldName} has a maxLengh of ${ruleValue}`
                    }
                    break
                case 'email':
                    if (ruleValue && !isValidEmail(fieldValue)) {
                        return `The field ${fieldName} must be email`
                    }
                    break
                case 'pattern':
                    if (ruleValue && !new RegExp(ruleValue).test(fieldValue)) {
                        return `The field ${fieldName} doesn't match the pattern`
                    }
                    break
                case 'confirm':
                    if (ruleValue && fieldValue !== formField[ruleValue]) {
                        return `The field ${fieldName} must match ${ruleValue}`
                    }
                    break
                // 可以根据需要添加其他验证规则
                default:
                    break
            }
        }
    }

    return true
}

function isValidEmail(email) {
    // 实现一个简单的邮箱验证逻辑
    return /\S+@\S+\.\S+/.test(email)
}

export { formValidator, itemValidator }
