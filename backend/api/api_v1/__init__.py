#! /usr/bin/env python
# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         __init__.py.py
# Author:       Xilyfe
# Date:         2023/6/11
# Description:  
# -------------------------------------------------------------------------------
from fastapi import APIRouter

from api.api_v1.endpoints import user, captcha, login, avatar, file, share

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(captcha.router, prefix="/captcha", tags=["cpatcha"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(avatar.router, tags=["avatar"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
api_router.include_router(share.router, prefix="/share", tags=["share"])