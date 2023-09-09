#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[datetime] = None
