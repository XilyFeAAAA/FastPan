# Fundamental
from fastapi import APIRouter, Depends, Body

# Backend
import crud
import models
import utils
from api import deps
from schemas.user import UserCreate, UserUpdate, UserUpdateAuth
from schemas.response import Response200, Response400
from exceptions import user as exception

router = APIRouter()


@router.get("/", response_model=Response200 | Response400)
async def read_users(skip: int = 0, limit: int = 100,
                     current_user: models.User = Depends(deps.get_current_user)):
    """Retrieve users"""
    try:
        users = await crud.user.get_multi(skip, limit)
        return Response200(data={"users": users})
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.post("/", response_model=Response200 | Response400)
async def create_user(user_in: UserCreate):
    """
        Create new user
        1. verify the email checkcode
        2. check whether user with same email exists
        3. db create new user
    """
    try:
        await utils.captcha.validate(user_in.captcha_id, user_in.captcha_code)
        if await crud.user.get_by_email(user_in.email):
            raise exception.UserExist()
        await utils.email.send_register_email(user_in.nickname, user_in.email)
        await crud.user.create(user_in)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.get("/me", response_model=Response200 | Response400)
async def read_user_me(current_user: models.User = Depends(deps.get_current_user)):
    """Get current user"""
    return Response200(data={"user": current_user})


@router.post("/verify-email", response_model=Response200 | Response400)
async def verify_email(email: str, token: str):
    """Verify the email"""
    if not await crud.email.checkToken(email, token):
        return Response400(msg="Invalid token")
    return Response200()


@router.post("/resetPwd", response_model=Response200 | Response400)
async def reset(user_update: UserUpdate):
    """
        Reset the password
        1. 检查验证码
        2. 检查邮箱验证码
        3. 检查用户是否存在
        4. 修改密码
    """
    try:
        await utils.captcha.validate(user_update.captcha_id, user_update.captcha_code)
        await utils.email.validate(user_update.email, user_update.code)
        if await crud.user.get_by_email(user_update.email) is None:
            raise exception.UserNotExist()
        await crud.user.resetPwd(user_update.email, user_update.password)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.post('/resetPwd-auth', response_model=Response200 | Response400)
async def reset_auth(user_update: UserUpdateAuth, current_user: models.User = Depends(deps.get_current_user)):
    try:
        # await crud.user.resetPwd(current_user.email, user_update.password)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.get('/logout', response_model=Response200 | Response400)
async def logout(current_user: models.User = Depends(deps.get_current_user)):
    try:
        await crud.user.active(current_user, False)
        return Response200()
    except Exception as e:
        return Response400(msg=e.__class__.__name__)


@router.get('/active', response_model=Response200 | Response400)
async def active(current_user: models.User = Depends(deps.get_current_user)):
    if current_user.is_active:
        return Response200()
    else:
        return Response400(msg="Inactive user")
