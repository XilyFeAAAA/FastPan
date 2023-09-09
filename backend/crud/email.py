#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from datetime import datetime, timedelta
# SQLAlchemy Related
from sqlalchemy import select, false, update, true
from sqlalchemy.ext.asyncio import AsyncSession

# Sql Related
from models import EmailToken, EmailCode, User
from db.engine import general as engine
from core.security import check_token


async def createToken(email: str, token: str) -> None:
    """Create EmailToken reocrd"""
    db_obj = EmailToken(
        email=email,
        token=token
    )
    async with AsyncSession(engine) as session:
        session.add(db_obj)
        await session.commit()


async def createCode(email: str, code: str, expires_delta: timedelta) -> None:
    """Creat EmailCode Record"""
    expire = datetime.utcnow() + expires_delta
    db_obj = EmailCode(
        email=email,
        code=code,
        expired_time=expire
    )
    async with AsyncSession(engine) as session:
        session.add(db_obj)
        await session.commit()


async def checkToken(email: str, token: str) -> bool:
    """Correspond the email with the token"""
    if await check_token(token) is None:
        return False
    stmt = select(EmailToken) \
        .filter(EmailToken.email == email) \
        .filter(EmailToken.token == token) \
        .filter(EmailToken.deleted == false())
    async with AsyncSession(engine) as session:
        orm_email_token = (await session.execute(stmt)).scalars().first()
        if orm_email_token is not None:
            """Change is_validated status"""
            orm_email_token.deleted = true()
            stmt = update(User) \
                .filter(User.email == email) \
                .filter(User.deleted == false()) \
                .values(is_validate=true())
            await session.execute(stmt)
            await session.commit()
    return orm_email_token


async def checkCode(email: str, code: str) -> bool:
    """Correspond the email with the code"""
    date_now = datetime.now().date()
    stmt = select(EmailCode) \
        .filter(EmailCode.email == email) \
        .filter(EmailCode.code == code) \
        .filter(EmailCode.expired_time >= date_now) \
        .filter(EmailCode.deleted == false())
    async with AsyncSession(engine) as session:
        orm_email_code = (await session.execute(stmt)).scalar()
        if orm_email_code is not None:
            orm_email_code.deleted = true()
            await session.commit()
    return orm_email_code
