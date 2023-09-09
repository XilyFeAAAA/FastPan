from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from core.config import settings

# General engine for SQL connection to the backend database
general = create_async_engine(f"mysql+aiomysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_SERVER}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}?charset={settings.MYSQL_CHARSET}")


