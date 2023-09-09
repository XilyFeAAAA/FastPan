#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import List
from sqlalchemy import select, false, update, true, and_, join
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from db.engine import general as engine
from models import Share as shareModel, File as fileModel


async def get_multi(skip: int, limit: int, userId: int):
    stmt = select(shareModel) \
        .filter(shareModel.user_id == userId) \
        .filter(shareModel.deleted == false()) \
        .offset(skip) \
        .limit(limit)
    async with AsyncSession(engine) as session:
        orm_shares = (await session.execute(stmt)).scalars().all()
    return orm_shares


async def get(shareId: str):
    stmt = select(shareModel) \
        .filter(shareModel.share_id == shareId) \
        .filter(shareModel.deleted == false())
    async with AsyncSession(engine) as session:
        orm_share = (await session.execute(stmt)).scalar_one_or_none()
    return orm_share


async def add(share_id: str, fileId: str, userId: int, valid_type: int, expire_time: datetime, curDate: datetime,
              code: str):
    db_obj = shareModel(
        share_id=share_id,
        file_id=fileId,
        user_id=userId,
        valid_type=valid_type,
        expired_time=expire_time,
        share_time=curDate,
        code=code
    )
    async with AsyncSession(engine) as session:
        session.add(db_obj)
        await session.commit()


async def del_by_id(shareIds: List[str], userId: int):
    stmt = update(shareModel) \
        .where(shareModel.share_id.in_(shareIds)) \
        .where(shareModel.user_id == userId) \
        .where(shareModel.deleted == false()) \
        .values(deleted=true())
    async with AsyncSession(engine) as session:
        await session.execute(stmt)
        await session.commit()