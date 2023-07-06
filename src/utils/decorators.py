import backoff
import functools

from elasticsearch.exceptions import ElasticsearchException
from redis.exceptions import RedisError

from core.config import settings


def redis_backoff(func):
    @functools.wraps(func)
    @backoff.on_exception(
        backoff.expo, RedisError, max_time=settings.BACKOFF_MAX_TIME
    )
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper


def es_backoff(func):
    @functools.wraps(func)
    @backoff.on_exception(
        backoff.expo,
        ElasticsearchException,
        max_time=settings.BACKOFF_MAX_TIME,
    )
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper
