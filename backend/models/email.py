#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from db.base_class import Base


class EmailToken(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 邮箱
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    # 验证码
    token: Mapped[str] = mapped_column(Text(), nullable=False)
    # 软删除
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class EmailCode(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 邮箱
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    # 验证码
    code: Mapped[str] = mapped_column(String(4), nullable=False)
    # 过期时间
    expired_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # 软删除
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
