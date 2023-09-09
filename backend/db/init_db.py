#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from models import Captcha, User, EmailCode, EmailToken, File, Share
from db.engine import general
import asyncio

models = [Captcha, User, EmailCode, EmailToken, File, Share]


async def init_models():
    async with general.begin() as conn:
        for model in models:
            await conn.run_sync(model.metadata.drop_all)
            await conn.run_sync(model.metadata.create_all)


asyncio.run(init_models())
