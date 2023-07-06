from abc import ABC, abstractmethod, abstractproperty
from typing import Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from utils.decorators import es_backoff

from models.base import Base


class AbstractRepository(ABC):
    @abstractproperty
    def index_name(self) -> str:
        pass

    @abstractproperty
    def base_model(self) -> Base:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> Optional[Base]:
        raise NotImplemented()

    @abstractmethod
    async def search(self, query: str, sort: str) -> Optional[list[Base]]:
        raise NotImplemented()


class AbstractElasticSearchRepository(AbstractRepository):
    def __init__(self, es_client: AsyncElasticsearch) -> None:
        self.es_client = es_client

    def _get_sort(
        self,
        sort: str,
    ) -> dict[str, list[str]]:
        """
        реализация для эластика
        вернуть dict с условием сортировки который
        позднее будет добавлен в основной body

        Parameters
        ----------
        sort : str
            Строка содержащее поле по которому будет
            производиться сортировка, если первый элемент
            строки `-` то используется сортировка по убыванию

        Returns
        -------
        dict[str, list[str]]
            словарь ключ которого sort, а значение массив
            содержащий критерий сортировки
            {"sort": ["field.raw": {"order": "asc"}]}
        """
        result = {"sort": []}
        field = sort
        cond = "asc"
        model_fields = self.base_model.get_sort_fields()
        if sort.startswith("-"):
            field = sort[1:]
            cond = "desc"
        if field in model_fields.keys():
            result["sort"].append({model_fields.get(field): {"order": cond}})
            return result
        result["sort"].append("_score")
        return result

    @es_backoff
    async def search(
        self,
        sort: str,
        page_number: int,
        page_size: int,
        query: str = None,
    ) -> Optional[list[Base]]:
        """получить результаты данных по поиску во всех полях индекса

        Args:
            sort (str): Сортировка по существующему полю, по возрастанию
                        или по убыванию например ?sort=-name отсортирует
                        по убыванию названия
            page_number (int): номер страницы
            page_size (int): размер страницы
            query (str): текст который необходимо найти

        Returns:
            Optional[list[BaseModel]]: массив Pydantic моделей, если
                            хотя бы одинэлемент был найден или None
        """
        page = (page_number - 1) * page_size
        query_body = {"match_all": {}}
        if query:
            query_body = {
                "multi_match": {
                    "query": query,
                    "fuzziness": "AUTO",
                    "fields": self.base_model.get_search_fields(),
                }
            }
        body = {
            "from": page,
            "query": query_body,
            "size": page_size,
        }
        if sort:
            sort_body = self._get_sort(sort)
            body.update(sort_body)

        data = await self.es_client.search(
            index=self.index_name,
            body=body,
        )
        data = data["hits"]["hits"]
        if len(data) > 0:
            return [self.base_model(**item["_source"]) for item in data]
        return None

    @es_backoff
    async def get(self, id: UUID) -> Optional[Base]:
        """Получить данные из индекса по uuid

        Args:
            id (UUID): идентификатор записи

        Returns:
            Optional[BaseModel]: Pydantic модель, если
                                элемент был найден или None
        """
        try:
            data = await self.es_client.get(self.index_name, id)
        except NotFoundError:
            return None
        return self.base_model(**data["_source"])
