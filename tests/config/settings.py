from typing import Optional

from dotenv import find_dotenv
from pydantic import BaseSettings


class TestSettings(BaseSettings):
    # Настройки Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # Настройки Elasticsearch
    ELASTIC_HOST: str = "elasticsearch"
    ELASTIC_PORT: int = 9200

    # Настройки основного сервиса
    SERVICE_URL: str = "fastapi"

    # Настройки логирования
    LOGGER_FORMATTER: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGER_LEVEL: str = "DEBUG"
    LOGGER_FILE: Optional[str] = "/tests/logs/tests.log"

    class Config:
        env_file = find_dotenv(".env.tests")


test_settings = TestSettings()
