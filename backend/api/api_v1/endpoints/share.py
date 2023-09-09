#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
# Fundamental
from fastapi import APIRouter, Response, Body, Depends
from fastapi.responses import JSONResponse
import utils
import models
from api import deps
from schemas.response import Response200, Response400
from schemas.user import UserUpdate
import crud
from exceptions import user as exception

router = APIRouter()


@router.get("/getShareList", response_model=Response200 | Response400)
async def getShareList(skip: int = 0, limit: int = 100,
                       current_user: models.User = Depends(deps.get_current_user)):
    # try:
    shares, files = await utils.share.getShareList(skip, limit, current_user.id)
    return Response200(data={"shares": shares, 'files':files })
    # except Exception as e:
    #     return Response400(msg=e.__class__.__name__)


@router.post("/shareFile", response_model=Response200 | Response400)
async def shareFile(fileId: str = Body(), valid_type: int = Body(), code: str = Body(), current_user: models.User = Depends(deps.get_current_user)):
    """Generate share url"""
    try:
        url = await utils.share.create_share_url(fileId, current_user.id, valid_type, code)
        return Response200(data={
            "shareUrl": url
        })
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.post('/cancelShare', response_model=Response200 | Response400)
async def delFile(shareIds: str = Body(...), current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        shareIdList = shareIds.split(',')
        await crud.share.del_by_id(shareIdList, current_user.id)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.get('/getShareInfo', response_model=Response200 | Response400)
async def getShareInfo(shareId: str):
    # try:
    share_info = await crud.share.get(shareId)
    if not share_info:
        return Response200()
    file_info = await crud.file.get_by_id(share_info.file_id, share_info.user_id)
    return Response200(data={
            'shareInfo': share_info,
            'fileInfo': file_info
        })
    # except Exception as e:
    #     return Response400(msg=e.__class__.__name__)


@router.post('/checkShare', response_model=Response200 | Response400)
async def checkShare(shareId: str = Body(...), code: str = Body(...)):
    # try:
    shareInfo = await crud.share.get(shareId)
    return Response200(data={
            "confirm": (shareInfo is not None and code == shareInfo.code)
        })
    # except Exception as e:
    #     return Response400(msg=e.__class__.__name__)