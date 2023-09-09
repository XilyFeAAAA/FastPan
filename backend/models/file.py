#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Boolean, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from db.base_class import Base
import enums


class File(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String(10), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    file_md5: Mapped[str] = mapped_column(String(32), nullable=True)
    file_pid: Mapped[str] = mapped_column(String(10))
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=True)
    file_name: Mapped[str] = mapped_column(String(200))
    file_cover: Mapped[str] = mapped_column(String(100), nullable=True)
    file_path: Mapped[str] = mapped_column(String(100), nullable=True)
    created_time: Mapped[datetime] = mapped_column(DateTime)
    last_update_time: Mapped[datetime] = mapped_column(DateTime)
    # 0. 文件 1. 目录
    folder_type: Mapped[int] = mapped_column(Integer)
    # 视频 音频 图片 文档 其他
    file_category: Mapped[int] = mapped_column(BigInteger, nullable=True)
    # 视频 音频 图片 pdf doc excel txt code zip 其他
    file_type: Mapped[int] = mapped_column(BigInteger, nullable=True)
    # 转码中 转码失败 转码成功
    status: Mapped[int] = mapped_column(BigInteger)
    recovery_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # 0 正常 1 删除 2 回收站
    del_flag: Mapped[int] = mapped_column(Integer, default=enums.DelFlag.EXIST.value)
