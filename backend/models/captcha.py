#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from db.base_class import Base


class Captcha(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    captcha_id: Mapped[str] = mapped_column(String(12), nullable=False)
    # 验证码
    captcha_code: Mapped[str] = mapped_column(String(4), nullable=False)
    # 过期时间
    expired_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # 软删除
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
