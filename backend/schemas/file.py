#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class uploadFile(BaseModel):
    fileId: str
    fileName: str
    filePid: str
    fileMd5: str
    chunkIndex: int
    chunks: int
    totalSize: int


class uploadResult(BaseModel):
    fileId: str
    status: str


class FileBase(BaseModel):
    id: int | None = None
    file_id: str | None = None
    user_id: int | None = None
    file_md5: str | None = None
    file_pid: str | None = None
    file_size: int | None = None
    file_name: str | None = None
    file_cover: str | None = None
    file_path: str | None = None
    created_time: datetime | None = None
    last_update_time: datetime | None = None
    folder_type: int | None = None
    file_category: int | None = None
    file_type: int | None = None
    status: int | None = None
    recovery_time: datetime | None = None
    deleted: bool | None = None