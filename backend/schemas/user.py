#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Optional
from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    nickname: Optional[str] = None
    email: Optional[str] = None
    qq_open_id: Optional[str] = None
    qq_avatar: Optional[str] = None
    created_time: Optional[int] = None
    last_login_time: Optional[int] = None
    use_space: Optional[int] = None
    total_space: Optional[int] = None
    is_active: Optional[bool] = False
    is_superuser: bool = False
    captcha_id: Optional[str] = None
    captcha_code: Optional[str] = None


class UserLoginInfo(BaseModel):
    id: Optional[int] = None
    nickname: Optional[str] = None
    email: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str]
    code: str


class UserUpdateAuth(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
