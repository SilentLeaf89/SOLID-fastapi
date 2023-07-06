import orjson
import uuid

from functools import lru_cache
from typing import Optional

from fastapi import Depends
from redis.asyncio import Redis

from core.get_logger import logger
from db.redis import get_cache
from models.base import Base, orjson_dumps
from repositories.abstract_cache import AbstractCache
from services.es_search import BaseService
from utils.decorators import redis_backoff


class CacheRedis(AbstractCache):
    def __init__(self, client: Redis):
        self._client = client

    def create_key_by_id(self, id: uuid.UUID, service: BaseService) -> str:
        key_list = [service.repository.index_name, str(id)]
        key = "_".join(key_list)
        return key

    def create_key_by_list(
        self,
        genre: Optional[uuid.UUID],
        query: Optional[str | uuid.UUID],
        sort: str,
        page_number: int,
        page_size: int,
        service: BaseService,
    ) -> str:
        key_list = [
            service.repository.index_name,
            "genre",
            str(genre),
            "query",
            str(query),
            "sort",
            str(sort),
            "p_num",
            str(page_number),
            "p_size",
            str(page_size),
        ]
        key = "_".join(key_list)

        return key

    @redis_backoff
    async def get_list(self, key, model: Base):
        values = await self._client.get(key)
        logger.info("{0} get from redis".format(key))
        if not values:
            return None
        values = orjson.loads(values)
        data = []
        for item in values:
            data.append(model.parse_raw(item))
        return data

    @redis_backoff
    async def get_id(self, key, model: Base):
        data = await self._client.get(key)
        logger.info("{0} get from redis".format(key))
        if not data:
            return None
        data = model.parse_raw(data)
        return data

    @redis_backoff
    async def set_id(self, key, data: Base, expire: int):
        await self._client.set(key, data.json(), expire)
        logger.info("{0} set to redis".format(key))

    @redis_backoff
    async def set_list(self, key: str, data: list[Base], expire: int):
        values = []
        for item in data:
            values.append(item.json())

        await self._client.set(
            key, orjson_dumps(values, default="default"), expire
        )
        logger.info("{0} set to redis".format(key))


@lru_cache
def get_cache_service(
    cache: AbstractCache = Depends(get_cache),
) -> AbstractCache:
    return cache
