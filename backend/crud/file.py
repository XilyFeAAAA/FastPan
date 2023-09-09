#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
# Fundamental
from datetime import datetime, timedelta
# SQLAlchemy Related
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import literal_column
from typing import List

import enums
# Sql Related
from db.engine import general as engine
from models import File as fileModel


async def get_multi(filePid: str, userId: int, page: int, limit: int, category: str = None, fileNameFuzzy: str = None):
    skip = max(page - 1, 0) * limit
    stmt = select(fileModel) \
        .filter(fileModel.user_id == userId) \
        .filter(fileModel.del_flag == enums.DelFlag.EXIST.value) \
        .offset(skip) \
        .limit(limit)
    if category:
        stmt = stmt.filter(fileModel.file_category == enums.FileCategory[category].value)
    else:
        stmt = stmt.filter(fileModel.file_pid == filePid) 
    if fileNameFuzzy:
        stmt = stmt.filter(fileModel.file_name.like(f'%{fileNameFuzzy}%'))
    async with AsyncSession(engine) as session:
        orm_files = (await session.execute(stmt)).scalars().all()
    return orm_files


async def get_by_id(fileId: str, userId: int) -> fileModel:
    stmt = select(fileModel) \
        .filter(fileModel.file_id == fileId) \
        .filter(fileModel.user_id == userId) \
        .filter(fileModel.del_flag == enums.DelFlag.EXIST.value)

    async with AsyncSession(engine) as session:
        orm_file = (await session.execute(stmt)).scalar()
    return orm_file


async def get_by_ids(fileIds: List[str], userId: int):
    stmt = select(fileModel) \
        .filter(fileModel.file_id.in_(fileIds)) \
        .filter(fileModel.user_id == userId) \
        .filter(fileModel.del_flag == enums.DelFlag.EXIST.value)

    async with AsyncSession(engine) as session:
        orm_files = (await session.execute(stmt)).scalars().all()
    return orm_files


async def get_by_pid(filePid: str, userId: int):
    stmt = select(fileModel) \
        .filter(fileModel.file_pid == filePid) \
        .filter(fileModel.user_id == userId) \
        .filter(fileModel.del_flag == enums.DelFlag.EXIST.value)
    async with AsyncSession(engine) as session:
        orm_files = (await session.execute(stmt)).scalars().all()
    return orm_files

async def get_by_paths(pathArray: list, userId: int):
    # 构建 CASE 表达式
    result = []
    for path in pathArray:
        async with AsyncSession(engine) as session:
            stmt = select(fileModel) \
                .filter(fileModel.file_id == path) \
                .filter(fileModel.user_id == userId) \
                .filter(fileModel.folder_type == enums.FolderType.FOLDER.value) \
                .filter(fileModel.del_flag == enums.DelFlag.EXIST.value)
            orm_folder = (await session.execute(stmt)).scalar()
        result.append(orm_folder)
    return result


async def add(new_file: fileModel):
    async with AsyncSession(engine) as session:
        session.add(new_file)
        await session.commit()


async def md5Exist(md5: str):
    stmt = select(fileModel) \
        .filter(fileModel.file_md5 == md5) \
        .filter(fileModel.status == enums.Status.TRANSCODE_SUCCESS.value) \
        .filter(fileModel.del_flag == enums.DelFlag.EXIST.value)
    async with AsyncSession(engine) as session:
        orm_file = (await session.execute(stmt)).scalars().all()
    print(orm_file.count)
    return orm_file


async def nameExist(filePid: str, userId: str, fileName: str, folderType: int) -> bool:
    stmt = select(fileModel) \
        .filter(fileModel.user_id == userId) \
        .filter(fileModel.file_pid == filePid) \
        .filter(fileModel.folder_type == folderType) \
        .filter(fileModel.file_name == fileName) \
        .filter(fileModel.del_flag == enums.DelFlag.EXIST.value)
    async with AsyncSession(engine) as session:
        orm_file = (await session.execute(stmt)).scalars().all()
    return len(orm_file) == 0

async def rename(fileId: str, userId: int, newFileName: str) -> None:
    stmt = update(fileModel) \
        .where(fileModel.file_id == fileId) \
        .where(fileModel.user_id == userId) \
        .where(fileModel.del_flag == enums.DelFlag.EXIST.value) \
        .values(file_name=newFileName)
    async with AsyncSession(engine) as session:
        await session.execute(stmt)
        await session.commit()


async def updateCover(fileId: str, userId: int, cover: str):
    stmt = update(fileModel) \
        .where(fileModel.file_id == fileId) \
        .where(fileModel.user_id == userId) \
        .where(fileModel.del_flag == enums.DelFlag.EXIST.value) \
        .values(file_cover=cover)
    async with AsyncSession(engine) as session:
        await session.execute(stmt)
        await session.commit()


async def updateStatus(fileId: str, userId: int, status: int) -> None:
    stmt = update(fileModel) \
        .where(fileModel.file_id == fileId) \
        .where(fileModel.user_id == userId) \
        .where(fileModel.del_flag == enums.DelFlag.EXIST.value) \
        .values(status=status)
    async with AsyncSession(engine) as session:
        await session.execute(stmt)
        await session.commit()


async def updateFlag_by_id(fileIds: List[str], userId: int, flag: int) -> None:
    stmt = update(fileModel) \
        .where(fileModel.user_id == userId) \
        .where(fileModel.file_id.in_(fileIds)) \
        .values(del_flag=flag) 
    async with AsyncSession(engine) as session:
        await session.execute(stmt)
        await session.commit()


async def updateRecovery_by_id(fileIds: List[str], userId: int) -> None:
    stmt = update(fileModel) \
        .where(fileModel.user_id == userId) \
        .where(fileModel.file_id.in_(fileIds)) \
        .values(recovery_time=datetime.now()) 
    async with AsyncSession(engine) as session:
        await session.execute(stmt)
        await session.commit()


async def get_folder_by_id(filePid: str, userId: int):
    stmt = select(fileModel) \
        .filter(fileModel.file_pid == filePid) \
        .filter(fileModel.user_id == userId) \
        .filter(fileModel.folder_type == enums.FolderType.FOLDER.value) \
        .filter(fileModel.del_flag == enums.DelFlag.EXIST.value)
    async with AsyncSession(engine) as session:
        orm_folders = (await session.execute(stmt)).scalars().all()
    return orm_folders


async def update_file_pid(fileIds: List[str], filePid: str, userId: int):
    stmt = update(fileModel) \
        .where(fileModel.file_id.in_(fileIds)) \
        .where(fileModel.user_id == userId) \
        .where(fileModel.del_flag == enums.DelFlag.EXIST.value) \
        .values(file_pid=filePid)
    async with AsyncSession(engine) as session:
        await session.execute(stmt)
        await session.commit()


