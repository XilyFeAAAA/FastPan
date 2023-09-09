#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
# Fundamental
from datetime import datetime, timedelta
# SQLAlchemy Related
from sqlalchemy import select, false, true
from sqlalchemy.ext.asyncio import AsyncSession

# Sql Related
from models import Captcha as captchaModel
from db.engine import general as engine
from exceptions.captcha import CaptchaNotExist

async def create(captcha_id: str, captcha_code: str) -> None:
    """Create captcha reocrd"""
    expired_time = datetime.now() + timedelta(minutes=15)
    db_obj = captchaModel(
        captcha_id=captcha_id,
        captcha_code=captcha_code,
        expired_time=expired_time
    )
    async with AsyncSession(engine) as session:
        session.add(db_obj)
        await session.commit()


async def query(captcha_id: str) -> str:
    date_now = datetime.now().date()
    stmt = select(captchaModel) \
        .filter(captchaModel.captcha_id == captcha_id) \
        .filter(captchaModel.expired_time >= date_now) \
        .filter(captchaModel.deleted == false())
    async with AsyncSession(engine) as session:
        orm_captcha = (await session.execute(stmt)).scalar()
        if orm_captcha is None:
            raise CaptchaNotExist()
        return orm_captcha.captcha_code


async def check(captcha_id: str, captcha_code: str) -> bool:
    """Correspond the captcha with the code"""
    date_now = datetime.now().date()
    stmt = select(captchaModel) \
        .filter(captchaModel.captcha_id == captcha_id) \
        .filter(captchaModel.captcha_code == captcha_code) \
        .filter(captchaModel.expired_time >= date_now) \
        .filter(captchaModel.deleted == false())
    async with AsyncSession(engine) as session:
        orm_captcha = (await session.execute(stmt)).scalars().first()
        if orm_captcha is not None:
            orm_captcha.deleted = true()
            await session.commit()
    return orm_captcha is not None
