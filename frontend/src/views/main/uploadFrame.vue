<template>
    <div class="uploadFrame">
        <div class="header">
            <p>上传任务</p>
        </div>
        <div class="content">
            <div v-if="fileList.length === 0" class="empty">暂无上传任务</div>
            <div v-else class="file-list">
                <div v-for="(item, index) in fileList" :key="index" class="file-item flex-center">
                    <div class="upload-panel">
                        <div class="file-name">{{ item.fileName }}</div>
                        <div
                            class="progress"
                            v-if="
                                item.status === STATUS.uploading.value ||
                                item.status === STATUS.upload_second.value ||
                                item.status === STATUS.upload_finish.value
                            "
                        >
                            <progress
                                :value="item.uploadProgress"
                                max="1"
                                style="width: 80%"
                            ></progress>
                            <span style="margin-left: 5px"
                                >{{ item.uploadProgress.toFixed(1) * 100 }} %</span
                            >
                        </div>
                        <div class="upload-status" :style="{ color: STATUS[item.status].color }">
                            <font-awesome-icon :icon="STATUS[item.status].icon" />
                            <span class="status">{{ STATUS[item.status].desc }}</span>
                            <span class="upload-info" v-if="item.status === STATUS.uploading.value">
                                {{ proxy.Utils.sizeToStr(item.uploadSize) }} /
                                {{ proxy.Utils.sizeToStr(item.totalSize) }}
                            </span>
                            <span v-else-if="item.status === STATUS.fail.value">
                                {{ item.errorMsg }}
                            </span>
                        </div>
                    </div>
                    <div class="op flex-center">
                        <radial-progress
                            v-if="item.status === STATUS.init.value"
                            :diameter="20"
                            :strokeWidth="3"
                            :innerStrokeWidth="3"
                            :completed-steps="item.md5Progress"
                            :total-steps="1"
                        >
                            <!-- <p>{{ item.md5Progress }}</p> -->
                        </radial-progress>
                        <div class="op-btn">
                            <font-awesome-icon
                                v-if="item.pause && item.status === STATUS.uploading.value"
                                icon="play"
                                @click="startUpload"
                            />
                            <font-awesome-icon v-else icon="pause" @click="pauseUpload" />
                            <font-awesome-icon
                                v-if="
                                    item.status !== STATUS.init.value &&
                                    item.status !== STATUS.upload_finish.value &&
                                    item.status !== STATUS.upload_second.value
                                "
                                icon="square-minus"
                                @click="delUpload"
                            />
                            <font-awesome-icon
                                v-if="
                                    item.status === STATUS.upload_finish.value ||
                                    item.status === STATUS.upload_second.value
                                "
                                icon="x"
                                @click="deleteRecord(index)"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import sparkMD5 from 'spark-md5'
import { ref, getCurrentInstance } from 'vue'
import RadialProgress from 'vue-radial-progress'
export default {
    components: { RadialProgress },
    setup(props, { emit }) {
        const { proxy } = getCurrentInstance()
        const chunkSize = 1024 * 1024 * 5
        const api = {
            upload: '/file/uploadFile',
        }
        const STATUS = {
            init: {
                value: 'init',
                desc: '解析中',
                icon: 'upload',
                color: 'yellow',
            },
            emptyfile: {
                value: 'emptyfile',
                desc: '文件为空',
                icon: 'circle-exclamation',
                color: 'red',
            },
            fail: {
                value: 'fail',
                desc: '上传失败',
                icon: 'circle-exclamation',
                color: 'red',
            },
            uploading: {
                value: 'uploading',
                desc: '上传中',
                color: 'blue',
                icon: 'upload',
            },
            upload_finish: {
                value: 'upload_finish',
                desc: '上传完成',
                color: 'green',
                icon: 'check',
            },
            upload_second: {
                value: 'upload_second',
                desc: '秒传',
                color: 'green',
                icon: 'check',
            },
        }
        const computeMd5 = async (fileItem) => {
            let file = fileItem.file
            let blobSlice =
                File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice
            let chunks = Math.ceil(file.size / chunkSize)
            let currentChunk = 0
            let spark = new sparkMD5.ArrayBuffer()
            let fileReader = new FileReader()
            let loadNext = () => {
                let start = currentChunk * chunkSize
                let end = Math.min(start + chunkSize, file.size)
                fileReader.readAsArrayBuffer(blobSlice.call(file, start, end))
            }
            loadNext()
            try {
                return await new Promise((resolve, reject) => {
                    let resultFile = getFileByUid(file.uid)
                    fileReader.onload = (e) => {
                        spark.append(e.target.result)
                        currentChunk++
                        if (currentChunk < chunks) {
                            console.log(
                                `${file.name}, ${currentChunk}分片解析完成， 开始第${
                                    currentChunk + 1
                                }开始`,
                            )
                            let percent = Math.floor((currentChunk / chunks) * 100)
                            resultFile.md5Progress = percent / 100
                            loadNext()
                        } else {
                            let md5 = spark.end()
                            spark.destroy()
                            resultFile.md5Progress = 1
                            resultFile.status = STATUS.uploading.value
                            resultFile.md5 = md5
                            resolve(fileItem.uid)
                        }
                    }
                    fileReader.onerror = () => {
                        resultFile.md5Progress = -1
                        resultFile.status = STATUS.fail.value
                        resolve(fileItem.uid)
                    }
                })
            } catch (error) {
                debugger
                console.log(error)
                return null
            }
        }
        const getFileByUid = (uid) => {
            let file = fileList.value.find((item) => {
                return item.uid === uid
            })
            return file
        }
        const uploadFile = async (uid, chunkIndex) => {
            chunkIndex = chunkIndex ? chunkIndex : 0
            console.log(`正在上传分片${chunkIndex}`)
            // 分片上传
            let currentFile = getFileByUid(uid)
            const file = currentFile.file
            const fileSize = file.size
            const chunks = Math.ceil(fileSize / chunkSize)
            for (let i = chunkIndex; i < chunks; i++) {
                let delIndex = delList.value.indexOf(uid)
                if (delIndex !== -1) {
                    delList.value.splice(delIndex, 1)
                    break
                }
                currentFile = getFileByUid(uid)
                if (currentFile.pause) break
                let start = i * chunkSize
                let end = Math.min(start + chunkSize, fileSize)
                let chunkFile = file.slice(start, end)
                const formData = new FormData()
                formData.append('fileId', currentFile.fileId || '')
                formData.append('fileName', file.name)
                formData.append('filePid', currentFile.filePid)
                formData.append('fileMd5', currentFile.md5)
                formData.append('chunkIndex', i)
                formData.append('chunks', chunks)
                formData.append('totalSize', currentFile.totalSize)
                formData.append('file', chunkFile)
                let uploadResult = await proxy.Request.post(api.upload, formData, {
                    headers: {
                        'content-type': 'multipart/form-data',
                    },
                    onUploadProgress: (event) => {
                        let loaded = Math.min(event['loaded'], chunkSize)
                        currentFile.uploadSize = i * chunkSize + loaded
                        currentFile.uploadProgress =
                            Math.floor((currentFile.uploadSize / fileSize) * 100) / 100
                    },
                    errorCallback: (errorMsg) => {
                        currentFile.status = STATUS.fail.value
                        currentFile.errorMsg = errorMsg
                    },
                })
                if (uploadResult === null) break
                const status_info = uploadResult.data.data.status_info
                currentFile.fileId = status_info.fileId
                currentFile.status = STATUS[status_info.status].value
                currentFile.chunkIndex = i
                if (
                    status_info.status === STATUS.upload_second.value ||
                    status_info.status === STATUS.upload_finish.value
                ) {
                    currentFile.uploadProgress = 1
                    emit('uploadCallback')
                    break
                }
            }
        }
        const deleteRecord = (index) => {
            fileList.value.splice(index, 1)
        }
        const fileList = ref([])
        const delList = ref([])
        const addFile = async (file, filePid) => {
            const fileItem = {
                file: file, // 文件
                uid: file.uid,
                md5: null,
                md5Progress: 0,
                fileName: file.name,
                status: STATUS.init.value,
                uploadSize: 0,
                totalSize: file.size,
                uploadProgress: 0,
                pause: false,
                chunkIndex: 0,
                filePid: filePid,
                errorMsg: null,
            }
            fileList.value.unshift(fileItem)
            if (fileItem.totalSize === 0) {
                fileItem.status = STATUS.emptyfile.value
                return
            }
            let md5FileUid = await computeMd5(fileItem)
            if (md5FileUid === null) return
            await uploadFile(md5FileUid)
        }
        return {
            proxy,
            fileList,
            addFile,
            STATUS,
            deleteRecord,
        }
    },
}
</script>
<style lang="scss" scoped>
.uploadFrame {
    display: flex;
    flex-direction: column;
    width: 35vw;
    height: 40vh;
    overflow-y: auto;
    .header {
        font-size: 0.875rem;
        padding: 5px 10px;
        border-bottom: 1px solid rgb(102, 102, 102, 0.5);
    }
    .content {
        flex: 1;
        .empty {
            margin-top: 20px;
            text-align: center;
            color: #acacac;
        }
        .file-list {
            font-size: 0.875rem;
            // padding: 10px 0px;
            .file-item {
                position: relative;
                padding: 5px 10px;
                border-bottom: 1px solid #ddd;
                .upload-panel {
                    flex: 1;
                    .file-name {
                        font-size: 0.875rem;
                    }
                    .upload-status {
                        font-size: 0.6rem;
                    }
                }
                .upload-status span {
                    margin: 0 7px;
                }
                .op .op-btn svg {
                    margin: 0 10px;
                    cursor: pointer;
                }
            }
        }
    }
}
</style>
