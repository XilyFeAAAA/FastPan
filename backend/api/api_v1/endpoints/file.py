#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
# Fundamental
from typing import List
from fastapi import APIRouter, Depends, Body, UploadFile, File, UploadFile, Form
from fastapi.responses import FileResponse
from pathlib import Path
from aiofiles import open as async_open
from pydantic import BaseModel

from api import deps
import models
import utils
import crud
# Backend
from core.config import settings
from schemas.file import uploadFile
from schemas.response import Response200, Response400

"""
    文件列表 完成
    文件切片上传 完成
    显示封面 完成
    视频预览 完成
    文件重命名 完成
    新建文件夹 完成
    获取所有目录 完成
    修改目录 、移动文件 完成
    创建下载链接 完成
    下载文件 完成
    删除文件 完成
    多选文件压缩
"""

"""
TODO: 操作文件之后修改日期
"""

router = APIRouter()


@router.get('/', response_model=Response200 | Response400)
async def get_file(filePid: str, category: str | None = None, fileNameFuzzy: str | None = None, page: int = 0, limit: int = 100,
                   current_user: models.User = Depends(deps.get_current_active_user)):
    """Retrieve files"""
    try:
        files = await crud.file.get_multi(filePid, current_user.id, page, limit, category, fileNameFuzzy)
        return Response200(data={"files": files})
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.post('/uploadFile', response_model=Response200 | Response400)
async def upload_file(fileId: str = Form(default=""),
                      fileName: str = Form(...),
                      filePid: str = Form(...),
                      fileMd5: str = Form(...),
                      chunkIndex: int = Form(...),
                      chunks: int = Form(...),
                      totalSize: int = Form(...),
                      current_user: models.User = Depends(deps.get_current_active_user),
                      file: UploadFile = File(...)):
    file_info = uploadFile(
        fileId=fileId,
        fileName=fileName,
        filePid=filePid,
        fileMd5=fileMd5,
        chunkIndex=chunkIndex,
        chunks=chunks,
        totalSize=totalSize
    )
    try:
        res = await utils.file.uploadFile(current_user, file_info, file)
        return Response200(data={
            'status_info': res
        })
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.post('/newFolder', response_model=Response200 | Response400)
async def create_new_folder(filePid: str = Body(), fileName: str = Body(),
                            current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        fileInfo = await utils.file.newFolder(filePid, current_user.id, fileName)
        return Response200(data={
            'file_info': fileInfo
        })
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.get('/getFolderInfo', response_model=Response200 | Response400)
async def getFolderInfo(path: str, current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        folderInfo = await utils.file.getFolderInfo(path, current_user.id)
        return Response200(data={
            'folder_info': folderInfo
        })
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.post('/renameFile', response_model=Response200 | Response400)
async def rename(fileId: str = Body(), newFileName: str = Body(),
                 current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        await crud.file.rename(fileId, current_user.id, newFileName)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)



@router.get('/getCover/{imageName}')
async def getCover(imageName: str):
    try:
        coverFolderPath: Path = settings.FILE_SAVE_FOLDER
        # 判断文件
        coverFilePath: Path = coverFolderPath / imageName
        # 判断文件夹路径
        if not coverFolderPath.exists() or not coverFilePath.exists():
            return FileResponse(None)
        return FileResponse(coverFilePath)
    except Exception as e:
        return Response400(msg=e.__class__.__name__)
    

@router.get('/ts/getVideo/{fileId}')
async def getVideo(fileId: str, current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        res = await utils.file.getFile(fileId, current_user.id)
        print(res.absolute())
        return FileResponse(res)
    except Exception as e:
        return Response400(msg=e.__class__.__name__)
    
@router.get('/getFile/{fileId}')
async def getFile(fileId: str, current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        res = await utils.file.getFile(fileId, current_user.id)
        return FileResponse(res)
    except Exception as e:
        return Response400(msg=e.__class__.__name__)
    

@router.get('/createDownloadUrl/{fileId}')
async def createDownloadUrl(fileId: str, current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        code = await utils.file.createDownloadUrl(fileId, current_user.id)
        return Response200(data={
            "code": code
        })
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.get('/download/{code}')
async def download(code: str):
    try:
        filePath, fileName = await utils.file.download(code)
        return FileResponse(filePath, filename=fileName)
    except Exception as e:
        return Response400(msg=e.__class__.__name__)

@router.post('/delFile')
async def delFile(fileIds: str = Body(...), current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        await utils.file.delFile(fileIds, current_user.id)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)

@router.get('/loadAllFolder')
async def loadAllFolder(filePid: str, current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        folders = await crud.file.get_folder_by_id(filePid, current_user.id)
        return Response200(data={
                'folder': folders
        })
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.post('/moveFile', response_model=Response200 | Response400)
async def moveFile(fileIds: str = Body(...), targetFolderId: str = Body(...), current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        fileIdList = fileIds.split(',')
        await crud.file.update_file_pid(fileIdList, targetFolderId, current_user.id)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)