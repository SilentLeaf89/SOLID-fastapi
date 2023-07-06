from abc import ABC
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from repositories.abstract_search import AbstractRepository


class BaseService(ABC):
    """
    Базовый класс для сервисов с бизнес логикой
    """

    def __init__(
        self,
        repository: AbstractRepository,
    ) -> None:
        self.repository = repository

    async def search(
        self,
        sort: str,
        page_number: int,
        page_size: int,
        query: str = None,
    ) -> Optional[list[BaseModel]] | None:
        result = await self.repository.search(
            sort, page_number, page_size, query
        )
        return result

    async def get(self, id: UUID) -> Optional[BaseModel] | None:
        result = await self.repository.get(id)
        return result
