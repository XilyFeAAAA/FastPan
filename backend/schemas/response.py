from typing import Any
from pydantic import BaseModel, Field
from enum import Enum

class codeEnum(int, Enum):
    SUCCESS = 200
    FAIL = 400

class ResponseBase(BaseModel):
    code: codeEnum = Field(description='业务状态码')
    data: Any = Field(default=None, description='数据')
    msg: str | None = Field(default=None, description='提示')

class Response200(ResponseBase):
    code = codeEnum.SUCCESS

class Response400(ResponseBase):
    code = codeEnum.FAIL

class ResponseToken(Response200):
    access_token: str = Field()
    token_type: str = Field(default='bearer')