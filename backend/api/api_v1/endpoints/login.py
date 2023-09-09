# Fundamental
from fastapi import APIRouter, Depends, HTTPException
from typing import Any
import crud
from schemas.user import UserLoginInfo as loginInfoSchemas
from schemas.token import Token as tokenSchemas
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from core import security
from core.config import settings


router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_validated:
        raise HTTPException(status_code=405, detail="Invalidate user")
    await crud.user.active(user, True)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": await security.create_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "info": loginInfoSchemas(**user.__dict__)
    }
