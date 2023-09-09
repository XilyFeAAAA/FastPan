#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import random

import aiosmtplib
import aiofiles
import crud
from core.security import create_token
from core.config import settings
from jinja2 import Template
from typing import Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import timedelta
from exceptions import email as exception


async def validate(email: str, code: str) -> None:
    """
        Verify checkcode
        1. check whether the email corresponds
        2. check the expired time
    """
    email_record = await crud.email.checkCode(email, code)
    if not email_record:
        raise exception.EmailNotExist()


async def send_email(
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment: Dict[str, Any] = {},
) -> None:
    # 创建带有HTML内容的邮件消息对象
    message = MIMEMultipart('related')
    message['Subject'] = Template(subject_template).render(environment)
    message['From'] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    message['To'] = email_to

    html = Template(html_template).render(environment)
    html_part = MIMEText(html, 'html')
    message.attach(html_part)

    # 设置SMTP服务器选项
    smtp_options = {
        'hostname': settings.SMTP_HOST,
        'port': settings.SMTP_PORT,
        'use_tls': settings.SMTP_TLS,
    }
    if settings.SMTP_USER:
        smtp_options['username'] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options['password'] = settings.SMTP_PASSWORD

    # 异步连接SMTP服务器并发送邮件
    async with aiosmtplib.SMTP(**smtp_options) as smtp:
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        await smtp.send_message(message)


async def send_register_email(nickname: str, email_to: str) -> None:
    """
        发送注册验证邮件
        1. 生成验证token
        2. 存储到db
        3. 渲染模板 + 发送邮件
    """
    verify_token_expires = timedelta(minutes=settings.VERIFY_TOKEN_EXPIRE_MINUTIES)
    token = await create_token(0, verify_token_expires)
    await crud.email.createToken(email_to, token)
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Register email"
    async with aiofiles.open(r"E:\coding\全栈\fastpan\backend\email-templates\register_email.html", mode='r') as f:
        template_str = await f.read()
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "username": nickname,
            "token": token
        }
    )


async def send_code_email(email_to: str):
    """
        1. 随机生成验证码
        2. 储存入emailCode表
        3. 发送邮件
    """
    verify_code_expires = timedelta(minutes=settings.VERIFY_CODE_EXPIRE_MINUTIES)
    code = "".join(random.choices("0123456789", k=4))
    await crud.email.createCode(email_to, code, verify_code_expires)
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Captcha email"
    async with aiofiles.open(r"E:\coding\全栈\fastpan\backend\email-templates\code_email.html", mode='r') as f:
        template_str = await f.read()
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "code": code
        }
    )
