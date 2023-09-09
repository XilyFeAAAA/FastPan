from models import Share as shareModel
from datetime import datetime, timedelta
from core.config import settings
import enums
import utils
import crud


async def create_share_url(fileId: str, userId: str, valid_type: int, code: str) -> str:
    curDate = datetime.now()
    share_id = utils.file.generate_random_string(settings.SHARE_ID_LENGTH)
    expire_time = None
    if valid_type != enums.ShareValidType.FOREVER.value:
        # 有过期时间
        expire_time = curDate + timedelta(days=valid_type)
    await crud.share.add(share_id, fileId, userId, valid_type, expire_time, curDate, code)
    return settings.SHARE_BASE_URL + share_id


async def getShareList(skip: int, limit: int, userId: int):
    shares = await crud.share.get_multi(skip, limit, userId)
    files = []
    for share in shares:
        files.append(await crud.file.get_by_id(share.file_id, userId))
    return shares, files
