import os
from logging import config as logging_config

from core.logger import LOGGING

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = "movies"

    # Настройки Redis
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379

    # Настройки Elasticsearch
    ELASTIC_HOST: str = "127.0.0.1"
    ELASTIC_PORT: int = 9200

    # Корень проекта
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # срок жизни кэша редиса
    CACHE_EXPIRE_IN_SECONDS: int = 3600

    # максимальное количество возвращаемых из elasticsearch элементов
    MAX_BULK_QUERY_SIZE: int = 1000

    # максимальное время для повторения восстановления с redis и с elasticsearch
    BACKOFF_MAX_TIME: int = 30

    class Config:
        env_file = ".env"


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

settings = Settings()
