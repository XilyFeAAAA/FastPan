#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import String, BigInteger, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from db.base_class import Base


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 昵称
    nickname: Mapped[str] = mapped_column(String(100), nullable=False)
    # 邮箱
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    # qq开放邮箱
    qq_open_id: Mapped[str] = mapped_column(String(100), nullable=True)
    # qq头像地址
    qq_avatar: Mapped[str] = mapped_column(String(100), nullable=True)
    # md5密码
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    # 创建时间
    created_time: Mapped[int] = mapped_column(BigInteger, nullable=False)
    # 最后一次登陆时间
    last_login_time: Mapped[int] = mapped_column(BigInteger, nullable=False)
    # 使用空间
    use_space: Mapped[int] = mapped_column(BigInteger)
    # 总空间
    total_space: Mapped[int] = mapped_column(BigInteger)
    # 是否验证
    is_validated: Mapped[bool] = mapped_column(Boolean, default=False)
    # 是否在线
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    # 是否为sa
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    # 软删除
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
