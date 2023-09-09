#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
import json
import os
import string
import subprocess
from typing import List, Any, Tuple
import aioshutil
from PIL import Image
import aiofiles
import random

from natsort import natsorted

import crud
import enums
from pathlib import Path
from datetime import datetime
from redis_setup import redis
import exceptions.file
from core.config import settings
from models.user import User as userModel
from models.file import File as fileModel
from schemas.file import uploadFile as uploadSchema, uploadResult as resultSchema


async def uploadFile(user_info: userModel, file_info: uploadSchema, file) -> resultSchema:
    # 先判断磁盘空间够不够
    if file_info.totalSize + user_info.use_space > user_info.total_space:
        raise exceptions.file.NotEnoughSpace()
    tempFileFolder: Path = None
    try:
        # 重命名文件
        if not await crud.file.nameExist(file_info.filePid, user_info.id, file_info.fileName,
                                         enums.FolderType.FILE.value):
            file_info.fileName = autoRename(file_info.fileName)
        if not file_info.fileId:
            file_info.fileId = generate_random_string(settings.FILEID_LENGTH)
        curDate = datetime.now()
        # 秒传
        if file_info.chunkIndex == 0:
            # 查MD5值是否存在
            if file_list := await crud.file.md5Exist(file_info.fileMd5):
                dbFile = file_list[0]
                # 插入新文件信息
                new_file = fileModel(
                    file_id=dbFile.file_id,
                    user_id=dbFile.user_id,
                    file_md5=dbFile.file_md5,
                    file_pid=dbFile.file_pid,
                    file_size=dbFile.file_size,
                    file_cover=dbFile.file_cover,
                    file_name=file_info.fileName,
                    file_path=dbFile.file_path,
                    created_time=curDate,
                    last_update_time=curDate,
                    folder_type=enums.FolderType.FILE.value,
                    file_category=dbFile.file_category,
                    file_type=dbFile.file_type,
                    status=enums.Status.TRANSCODE_SUCCESS.value,
                    recovery_time=dbFile.recovery_time
                )
                await crud.file.add(new_file)
                # 更新useSpace
                await crud.user.updateSpace(user_info.id)
                return resultSchema(
                    fileId=file_info.fileId,
                    status='upload_second'
                )
        # 暂存目录
        tempFolder: Path = settings.FILE_TEMP_FOLDER
        currentUserFolderName = f"{user_info.id}-{file_info.fileId}"
        tempFileFolder: Path = tempFolder / currentUserFolderName
        if not tempFileFolder.exists():
            tempFileFolder.mkdir(parents=True)
        filePath = tempFileFolder / f"{file_info.chunkIndex}"
        if not filePath.exists():
            async with aiofiles.open(filePath, 'wb') as f:
                await f.write(await file.read())
            # 返回上传中状态
        if file_info.chunkIndex < file_info.chunks - 1:
            return resultSchema(
                fileId=file_info.fileId,
                status='uploading'
            )
        # 最后一个分片上传后，记录数据库，异步合并
        fileSuffix = os.path.splitext(file_info.fileName)[1]
        # 真实文件名
        realFileName = currentUserFolderName + fileSuffix
        fileType = enums.FileType.FileTypeEnums(fileSuffix)
        fileCategory = enums.FileType.FileCategoryEnums(fileSuffix)
        new_file = fileModel(
            file_id=file_info.fileId,
            user_id=user_info.id,
            file_md5=file_info.fileMd5,
            file_pid=file_info.filePid,
            file_size=file_info.totalSize,
            file_name=file_info.fileName,
            file_path=realFileName,
            created_time=curDate,
            last_update_time=curDate,
            folder_type=enums.FolderType.FILE.value,
            file_category=fileCategory,
            file_type=fileType,
            status=enums.Status.TRANSCODING.value,
        )
        await crud.file.add(new_file)
        # 异步转码文件
        asyncio.create_task(transferFile(file_info.fileId, user_info))
        return resultSchema(
            fileId=file_info.fileId,
            status='upload_finish'
        )
    except Exception as e:
        print(e)
        raise e


def autoRename(fileName: str) -> str:
    base_name, suffix = os.path.splitext(fileName)
    return f"{base_name}_{generate_random_number(settings.RENAME_LENGTH)}{suffix}"


def generate_random_number(n) -> str:
    """
    生成n位随机数字
    """
    start = 10 ** (n - 1)
    end = (10 ** n) - 1
    return str(random.randint(start, end))


def generate_random_string(n) -> str:
    """
    生成n位随机字符串
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


async def newFolder(filePid: str, userId: int, fileName: str) -> fileModel:
    await checkFileName(filePid, userId, fileName, enums.FolderType.FOLDER.value)
    curDate = datetime.now()
    new_folder = fileModel(
        file_id=generate_random_string(settings.FILEID_LENGTH),
        user_id=userId,
        file_pid=filePid,
        file_name=fileName,
        folder_type=enums.FolderType.FOLDER.value,
        created_time=curDate,
        last_update_time=curDate,
        status=enums.Status.TRANSCODE_SUCCESS.value
    )
    await crud.file.add(new_folder)
    return new_folder


async def getFolderInfo(path: str, userId: int):
    pathArray = path.split('/')
    folders = await crud.file.get_by_paths(pathArray, userId)
    return folders


async def checkFileName(filePid: str, userId: int, fileName: str, folderType: int) -> None:
    if not await crud.file.nameExist(filePid, userId, fileName, folderType):
        raise exceptions.file.FileAlreadyExist()


async def transferFile(fileId: str, user_info: userModel):
    transferSuccess: bool = True
    targetFilePath: str = None
    cover: str = None
    fileType: int = None
    fileInfo = await crud.file.get_by_id(fileId, user_info.id)
    if fileInfo is None or fileInfo.status != enums.Status.TRANSCODING.value:
        return
    try:
        # 临时目录
        tempFolder = settings.FILE_TEMP_FOLDER
        currentUserFolderName = f"{user_info.id}-{fileId}"
        tempFileFolder: Path = tempFolder / currentUserFolderName
        # 目标目录
        targetFolderName: Path = settings.FILE_SAVE_FOLDER
        targetFilePath: Path = targetFolderName / fileInfo.file_path
        # 真实文件名
        fileSuffix = os.path.splitext(fileInfo.file_name)[1]
        fileType = enums.FileType.FileTypeEnums(fileSuffix)
        realFileName = currentUserFolderName + fileSuffix
        # 合并文件
        await union(tempFileFolder, targetFilePath, fileInfo.file_name, True)
        # 视频文件切割
        if fileType == enums.FileType.VIDEO.type:
            # 视频切片
            await curFile4Video(fileId, targetFilePath)
            # 视频生成缩略图
            cover = currentUserFolderName + settings.COVER_IMAGE_SUFFIX
            coverPath: Path = targetFolderName / cover
            createCover4Video(targetFilePath, settings.COVER_LENGTH, coverPath)
        elif fileType == enums.FileType.IMAGE.type:
            # 图片生成缩略图
            cover = realFileName.replace('.', '_.')
            coverPath = targetFolderName / cover
            if not generate_thumbnail(targetFilePath, settings.COVER_LENGTH, coverPath):
                # 如果失败则复制
                await aioshutil.copy2(targetFilePath, coverPath)
    except Exception as e:
        print(f'文件转码失败，文件ID:{fileInfo.file_id}, 用户ID:{user_info.id}')
        transferSuccess = False
        raise e
    finally:            
        # 修改文件status    
        # 修改文件cover
        if transferSuccess:
            if cover is not None:
                await crud.file.updateCover(fileInfo.file_id, user_info.id, cover)
            await crud.file.updateStatus(fileInfo.file_id, user_info.id, enums.Status.TRANSCODE_SUCCESS.value)           
            # 更新用户信息
            await crud.user.updateSpace(user_info.id)
            print(f'更新状态{enums.Status.TRANSCODE_SUCCESS.value}')
        else:
            await crud.file.updateStatus(fileInfo.file_id, user_info.id, enums.Status.TRANSCODE_FAILED.value)
            print(f'更新状态{enums.Status.TRANSCODE_FAILED.value}')


async def union(dirPath: Path, toFilePath: Path, fileName: str, delSource: bool):
    if not dirPath.exists():
        raise exceptions.file.FolderNotExist()
    try:
        async with aiofiles.open(toFilePath, "wb") as output:
            for file_path in natsorted(dirPath.iterdir(), key=lambda x: x.name):
                async with aiofiles.open(file_path, "rb") as part:
                    await output.write(await part.read())
        await asyncio.sleep(0)
    except Exception as e:
        print(f'合并文件分片{fileName}失败')
        raise e
    finally:
        if delSource and dirPath.exists():
            await aioshutil.rmtree(dirPath)


async def curFile4Video(fileId: str, videoFilePath: str):
    # 创建同名切片目录
    tsFolder: Path = settings.FILE_CUTTING_FOLDER / os.path.splitext(videoFilePath)[0]
    if not tsFolder.exists():
        tsFolder.mkdir()
    tsPath = tsFolder / settings.TS_NAME
    m3u8Path = tsFolder / settings.M3U8_NAME
    CMD_TRANSFER_2TS = ['ffmpeg', '-y', '-i', videoFilePath, '-vcodec', 'copy', '-acodec', 'copy', '-vbsf',
                        'h264_mp4toannexb',
                        tsPath.absolute()]
    CMD_CUT_TS = ['ffmpeg', '-i', tsPath.absolute(), '-c', 'copy', '-map', '0', '-f', 'segment', '-segment_list', m3u8Path.absolute(),
                  '-segment_time', '30', f'{tsFolder.absolute()}/{fileId}_%04d.ts']
    # 生成ts
    subprocess.call(CMD_TRANSFER_2TS, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # 生成索引文件.m3u8 和 切片.ts
    subprocess.call(CMD_CUT_TS, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # 删除index.ts
    tsPath.unlink()


def createCover4Video(sourceFile: Path, width: int, targetFile: Path):
    """
    生成视频缩略图
    """
    CMD_CREATE_COVER = ['ffmpeg', '-i', sourceFile.absolute(), '-y', '-vframes', '1', '-vf', f'scale={width}:{width}/a', targetFile.absolute()]
    subprocess.call(CMD_CREATE_COVER, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_thumbnail(image_path: Path, width: int, thumbnail_path: Path) -> bool:
    """
    生成图片缩略图
    1. 检查大小,如果小于width则返回false,复制原图
    2. 用ffmpeg缩小
    """
    try:
        with Image.open(image_path) as img:
            pWidth, pHeight = img.size
        if min(pWidth, pHeight) <= width:
            return False
        compressImage(image_path, width, thumbnail_path)
        return True
    except:
        print('生成图片缩略图失败')
        return False

def sort_files_by_number(file_list):
    def file_number_key(file_name):
        parts = file_name.split('.')
        if len(parts) > 1 and parts[-1].isdigit():
            return int(parts[-1])
        else:
            return file_name
    return sorted(file_list, key=file_number_key)


def compressImage(image_path: Path, width: int, thumbnail_path: Path):
    """
    压缩图片
    """
    CMD_COMPRESS_IMAGE = ['ffmpeg', '-i', image_path.absolute(), '-vf', f'scale={width}:-1', thumbnail_path.absolute(), '-y']
    subprocess.call(CMD_COMPRESS_IMAGE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def getFile(fileId: str, userId: int) -> Path:
    """
    获取文件
    """
    filePath: Path = None
    if fileId.endswith(".ts"):
        realFileId = fileId.split('_')[0]
        fileInfo = await crud.file.get_by_id(realFileId, userId)
        if fileInfo is None:
            raise exceptions.file.FileNotExist()
        fileNameNoSuffix = os.path.splitext(fileInfo.file_path)[0]
        filePath = settings.FILE_SAVE_FOLDER / fileNameNoSuffix / fileId
    else:
        fileInfo = await crud.file.get_by_id(fileId, userId)
        if fileInfo is None:
            raise exceptions.file.FileNotExist()
        if fileInfo.file_category == enums.FileCategory.VIDEO.value:
            # 视频返回m3u8
            fileNameNoSuffix = os.path.splitext(fileInfo.file_path)[0]
            filePath = settings.FILE_SAVE_FOLDER / fileNameNoSuffix / settings.M3U8_NAME
        else:
            filePath = settings.FILE_SAVE_FOLDER / fileInfo.file_path
    if not filePath.exists():
        return
    return filePath


async def createDownloadUrl(fileId: str, userId: int) -> None:
    """ 
    获取下载链接
    """
    code: str = generate_random_string(settings.DOWNLOAD_LINK_LENGTH)
    val = f"{fileId}-{userId}"
    await redis.setex(name=settings.REDIS_KEY_DOWNLOAD + code, time=settings.REDIS_KEY_EXPIRE_TIMEDELTA, value=val)
    return code
    

async def download(code: str) -> Tuple[Path, str]:
    """
    根据code下载文件
    """
    val = await redis.get(name=settings.REDIS_KEY_DOWNLOAD + code)
    fileId, userId = val.decode('utf-8').split('-')
    fileInfo = await crud.file.get_by_id(fileId, int(userId))
    print(fileInfo.folder_type, enums.FolderType.FOLDER.value)
    if fileInfo is None or fileInfo.folder_type == enums.FolderType.FOLDER.value:
        return
    filePath = settings.FILE_SAVE_FOLDER / fileInfo.file_path
    fileName = fileInfo.file_name
    return filePath, fileName

async def delFile(fileIds: str, userId: int) -> None:
    """批量删除文件"""
    fileIdList = fileIds.split(',')
    fileInfoList = await crud.file.get_by_ids(fileIdList, userId)
    if not fileInfoList:
        return
    delFileIdList = []
    for fileInfo in fileInfoList:
        await findAllSubFolderFileList(delFileIdList, fileInfo, userId)
    if delFileIdList:
        await crud.file.updateFlag_by_id(delFileIdList, userId, enums.DelFlag.DELETED.value)
    # 文件放进回收站
    await crud.file.updateRecovery_by_id(fileIdList, userId)
    await crud.file.updateFlag_by_id(fileIdList, userId, enums.DelFlag.RECYCLE.value)
    await crud.user.updateSpace(userId)

async def findAllSubFolderFileList(fileIdList, fileInfo: fileModel, userId: int):
    """
    递归查找文件夹
    """
    fileIdList.append(fileInfo.file_id)
    if fileInfo.folder_type == enums.FolderType.FILE.value:
        return
    # 文件夹则递归查找
    fileInfoList = await crud.file.get_by_pid(fileInfo.file_id, userId)
    for subFileInfo in fileInfoList:
        await findAllSubFolderFileList(fileIdList, subFileInfo, userId) 
