from abc import ABC, abstractmethod
from typing import Optional
import uuid

from services.es_search import BaseService
from models.base import Base


class AbstractCache(ABC):
    def __init__(self, client):
        self._client = client

    @abstractmethod
    async def create_key_by_id(
        self, id: uuid.UUID, service: BaseService
    ) -> str:
        pass

    @abstractmethod
    async def create_key_by_list(
        self,
        genre: Optional[uuid.UUID],
        query: Optional[str | uuid.UUID],
        sort: str,
        page_number: int,
        page_size: int,
        service: BaseService,
    ) -> str:
        pass

    @abstractmethod
    async def get_list(self, key: str, model: Base):
        pass

    @abstractmethod
    async def get_id(self, key: str, model: Base):
        pass

    @abstractmethod
    async def set_id(self, key: str, data: Base, expire: int):
        pass

    @abstractmethod
    async def set_list(self, key: str, data: list[Base], expire: int):
        pass
