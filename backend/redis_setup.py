import aioredis
import asyncio
redis = None


async def connect_redis():
    global redis
    redis = await aioredis.Redis(host="127.0.0.1", port=6379, db=3, encoding="utf-8")
    print(f"redis成功--->>{redis}")


asyncio.run(connect_redis())
