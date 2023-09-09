# Fundamental
from fastapi import APIRouter, Depends, Body, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
from aiofiles import open as async_open
from api import deps
import models
# Backend
from core.config import settings
from schemas.response import Response200, Response400


router = APIRouter()


@router.get("/getAvatar/{userId}")
async def getAvatar(userId: str):
    """Retrieve avatars"""
    try:
        avatarFolderPath: Path = settings.AVATAR_FOLDER
        # 判断文件夹路径
        if not avatarFolderPath.exists():
            avatarFolderPath.mkdir()
        # 判断文件
        avatarFilePath: Path = avatarFolderPath / f'{userId}.{settings.AVATAR_SUFFIX}'
        # 没有返回默认头像
        if not avatarFilePath.exists():
            avatarFilePath = avatarFolderPath / settings.DEFAULT_AVATAR
        return FileResponse(avatarFilePath)
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.post("/uploadAvatar")
async def create_upload_file(file: UploadFile = File(...),
                             current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        avatarFolderPath: Path = settings.AVATAR_FOLDER
        # 判断文件夹路径
        if not avatarFolderPath.exists():
            avatarFolderPath.mkdir()
        avatarFilePath: Path = avatarFolderPath / f'{current_user.id}.{settings.AVATAR_SUFFIX}'
        # 异步保存
        async with async_open(avatarFilePath, 'wb') as f:
            contents = await file.read()
            await f.write(contents)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)
