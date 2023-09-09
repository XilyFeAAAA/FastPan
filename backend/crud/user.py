#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
# Fundamental
from time import time
from typing import Optional
import enums
# SQLAlchemy Related
from sqlalchemy import select, or_, false, true, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash
# Sql Related
from schemas import user as userSchema
from models import User as userModel, File as fileModel
from db.engine import general as engine
from core.security import verify_password


async def create(obj_in: userSchema.UserCreate) -> userModel:
    time_now = int(round(time() * 1000))
    db_obj = userModel(
        nickname=obj_in.nickname,
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        created_time=time_now,
        last_login_time=time_now,
        use_space=0,
        total_space=1024
    )
    async with AsyncSession(engine) as session:
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
    return db_obj


async def get_multi(skip: int, limit: int):
    stmt = select(userModel).filter(userModel.deleted ==
                                    false()).offset(skip).limit(limit)
    async with AsyncSession(engine) as session:
        orm_users = (await session.execute(stmt)).scalars().all()
        return orm_users


async def authenticate(email: str, password: str) -> Optional[userModel]:
    user = await get_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_by_email(email: str):
    stmt = select(userModel) \
        .filter(userModel.email == email) \
        .filter(userModel.deleted == false())
    async with AsyncSession(engine) as session:
        orm_user = (await session.execute(stmt)).scalars().first()
        return orm_user


async def get_by_id(id: int):
    stmt = select(userModel) \
        .filter(userModel.id == id) \
        .filter(userModel.deleted == false())
    async with AsyncSession(engine) as session:
        orm_user = (await session.execute(stmt)).scalar()
        return orm_user


async def is_superuser(user: userModel) -> bool:
    return user.is_superuser


async def resetPwd(email: str, password: str):
    stmt = update(userModel) \
        .where(userModel.email == email) \
        .where(userModel.deleted == false()) \
        .values(hashed_password=get_password_hash(password))
    async with AsyncSession(engine) as session:
        await session.execute(stmt)
        await session.commit()


async def active(user: userModel, status):
    stmt = update(userModel) \
        .where(userModel.id == user.id) \
        .where(userModel.deleted == false()) \
        .values(is_active=status)
    async with AsyncSession(engine) as session:
        await session.execute(stmt)
        await session.commit()


async def updateSpace(userId: int):
    stmt_sum = select(func.sum(fileModel.file_size)) \
        .where(fileModel.user_id == userId) \
        .where(fileModel.del_flag == enums.DelFlag.EXIST.value)
    async with AsyncSession(engine) as session:
        total_size = (await session.execute(stmt_sum)).scalar()
        stmt = update(userModel) \
            .where(userModel.id == userId) \
            .where(userModel.deleted == false()) \
            .values(use_space=total_size)
        await session.execute(stmt)
        await session.commit()
