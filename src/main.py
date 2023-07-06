import uvicorn
from elasticsearch import AsyncElasticsearch
from contextlib import asynccontextmanager
from elasticsearch.exceptions import ElasticsearchException
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from redis.exceptions import RedisError

from api.v1 import films, genres, persons
from core.config import settings
from core.exceptions import (
    redis_connection_exception_handler,
    es_connection_exception_handler,
)
from db import elastic, redis
from services.redis_cache import CacheRedis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = CacheRedis(
        Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    )
    elastic.es = AsyncElasticsearch(
        hosts=[f"{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}"]
    )
    yield
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=settings.PROJECT_NAME,
    # Адрес документации в красивом интерфейсе
    docs_url="/api/openapi",
    # Адрес документации в формате OpenAPI
    openapi_url="/api/openapi.json",
    # Можно сразу сделать небольшую оптимизацию сервиса
    # и заменить стандартный JSON-сереализатор на более шуструю версию,
    # написанную на Rust
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])


@app.exception_handler(RedisError)
async def redis_exception(request, exc):
    return await redis_connection_exception_handler(request, exc)


@app.exception_handler(ElasticsearchException)
async def elastic_exception(request, exc):
    return await es_connection_exception_handler(request, exc)


if __name__ == "__main__":
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
