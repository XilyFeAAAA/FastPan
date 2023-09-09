#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
# Fundanmental
import random
from crud import captcha
from captcha.image import ImageCaptcha
from exceptions import captcha as exception


async def validate(captcha_id: str, captcha_code: str) -> None:
    """
        Verify checkcode
        1. check whether the email corresponds
        2. check the expired time
    """
    captcha_record = await captcha.check(captcha_id, captcha_code)
    if not captcha_record:
        raise exception.CaptchaNotExist()


async def create_captcha(timestamp: int) -> str:
    """创建验证码，仅返回id"""
    random.seed(timestamp)
    letters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    captcha_id = "".join(random.choices(letters, k=8))
    captcha_code = "".join(random.choices(letters, k=4))
    await captcha.create(captcha_id, captcha_code)
    return captcha_id


async def generate_captcha(captcha_id: str) -> bytes:
    """Generate checkcode"""
    captcha_code = await captcha.query(captcha_id)
    image = ImageCaptcha(width=160, height=40, font_sizes=[30])
    captcha_image = image.generate(captcha_code)
    return captcha_image.getvalue()
