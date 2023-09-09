#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from datetime import timedelta
from pathlib import Path
import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = 7070
    API_V1_STR: str = "/api/v1"
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    VERIFY_CODE_EXPIRE_MINUTIES: int = 30
    VERIFY_TOKEN_EXPIRE_MINUTIES: int = 30
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SERVER_NAME: str = "FastPan"
    SERVER_HOST: str = "127.0.0.1"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    PROJECT_NAME: str = "FastPan"
    VERSION: str = "1.0.0"
    SENTRY_DSN: Optional[HttpUrl] = None

    MYSQL_SERVER: str = "127.0.0.1"
    MYSQL_PORT: str = "3306"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_DB: str = "fastpan"
    MYSQL_CHARSET: str = "utf8mb4"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 465
    SMTP_HOST: Optional[str] = "smtp.qq.com"
    SMTP_USER: Optional[str] = "邮箱"
    SMTP_PASSWORD: Optional[str] = "邮箱令牌"
    EMAILS_FROM_EMAIL: Optional[str] = "邮箱"
    EMAILS_FROM_NAME: Optional[str] = "Fastpan Official"

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/email-templates"
    EMAILS_ENABLED: bool = False

    Crypt_SCHEMAS: str = "bcrypt"

    WORK_DIR: Path = Path(os.getcwd())
    AVATAR_FOLDER: Path = WORK_DIR / "avatars"
    AVATAR_SUFFIX: str = "jpg"
    DEFAULT_AVATAR: str = "default.png"

    FILE_BASE_FOLDER: Path = WORK_DIR / 'file'
    FILE_TEMP_FOLDER: Path = FILE_BASE_FOLDER / 'temps'
    FILE_SAVE_FOLDER: Path = FILE_BASE_FOLDER / 'files'
    FILE_CUTTING_FOLDER: Path = FILE_BASE_FOLDER / 'cutting'
    FILEID_LENGTH: int = 10
    RENAME_LENGTH: int = 5
    TS_NAME: str = "index.ts"
    M3U8_NAME: str = "index.m3u8"

    DOWNLOAD_LINK_LENGTH: int = 50

    COVER_IMAGE_SUFFIX: str = ".png"
    COVER_LENGTH: int = 150

    REDIS_KEY_DOWNLOAD: str = "fastpan::download"
    REDIS_KEY_EXPIRE_TIMEDELTA: timedelta = timedelta(minutes=5)

    SHARE_ID_LENGTH: int = 20
    SHARE_BASE_URL: str = f"http://{HOST}:{PORT}/api/v1/share/"

    class Config:
        case_sensitive = True


settings = Settings()
