export default {
    sizeToStr: (limit) => {
        let size = ''
        if (limit < 0.1 * 1024) size = limit.toFixed(2) + 'B'
        else if (limit < 0.1 * 1024 * 1024) size = (limit / 1024).toFixed(2) + 'KB'
        else if (limit < 0.1 * 1024 * 1024 * 1024) size = (limit / 1024 / 1024).toFixed(2) + 'MB'
        else size = (limit / 1024 / 1024 / 1024).toFixed(2) + 'GB'
        let sizeStr = size + ''
        let index = sizeStr.indexOf('.')
        let dou = sizeStr.substr(index + 1, 2)
        if (dou == '00') {
            return sizeStr.substring(0, index) + sizeStr.substr(index + 3, 2)
        }
        return size
    },

    generateRandomString: (length) => {
        var result = ''
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        for (var i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * characters.length))
        }
        return result
    },

    datetime2str: (dateStr) => {
        if (dateStr === null) return '无限期'
        const date = new Date(dateStr)
        return new Intl.DateTimeFormat('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
        }).format(date)
    },
}
