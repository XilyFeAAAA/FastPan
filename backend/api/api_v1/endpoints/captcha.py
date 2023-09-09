#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
# Fundamental
from fastapi import APIRouter, Response, Body
from fastapi.responses import JSONResponse
import utils
from schemas.response import Response200, Response400
from schemas.user import UserUpdate
import crud
from exceptions import user as exception


router = APIRouter()


@router.get("/", response_model=Response200 | Response400)
async def checkcode(timestamp: int):
    """Generate checkcode_id"""
    # try:
    captcha_id = await utils.captcha.create_captcha(timestamp)
    return Response200(data={
            "captcha_id": captcha_id
        })
    # except Exception as e:
    #     return Response400(msg=e.__class__.__name__)


@router.get("/{captcha_id}.png")
async def generate(captcha_id: str):
    """Return captcha png"""
    img_data = await utils.captcha.generate_captcha(captcha_id)
    return Response(content=img_data, media_type="image/png")


@router.post("/sendEmailCode", response_model=Response200 | Response400)
async def emailcode(email: str = Body(), captcha_id: str = Body(), captcha_code: str = Body()):
    """Send email checkcode"""
    try:
        # 验证码
        await utils.captcha.validate(captcha_id, captcha_code)
        # 邮箱是否存在
        if await crud.user.get_by_email(email) is None:
            raise exception.UserNotExist()
        await utils.email.send_code_email(email)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)
