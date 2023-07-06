from typing import Optional

from redis.asyncio import Redis

redis: Optional[Redis] = None


# Функция понадобится при внедрении зависимостей
async def get_cache() -> Redis:
    return redis
