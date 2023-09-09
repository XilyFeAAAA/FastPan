from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import schemas
from core.config import settings


async def create_token(subject: str, expires_delta: timedelta = None):
    """生成JWT令牌"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"exp": expire, "sub": str(subject)}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return str(token)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def check_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.token.TokenPayload(**payload)
        if datetime.utcnow() > token_data.exp.astimezone(timezone.utc).replace(tzinfo=None):
            token_data = None
        return token_data
    except jwt.InvalidSignatureError as e:
        print('Invalid signature:', e)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """哈希加密"""
    return pwd_context.hash(password)


