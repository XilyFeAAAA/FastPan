#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from db.base_class import Base


class Share(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    share_id: Mapped[str] = mapped_column(String(20), nullable=False)
    file_id: Mapped[str] = mapped_column(String(20), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    valid_type: Mapped[int] = mapped_column(Integer, nullable=False)
    expired_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    share_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    show_count: Mapped[int] = mapped_column(Integer, default=0)
    # 软删除
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
