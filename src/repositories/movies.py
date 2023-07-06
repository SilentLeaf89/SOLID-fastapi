from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from elasticsearch import NotFoundError

from core.config import settings
from models.film import FilmShort, Film
from models.person import Person, PersonRole, FilmPersonRole
from utils.decorators import es_backoff

from .abstract_search import AbstractElasticSearchRepository
from .raw_queries.movies import helper_genre_name, helper_person_roles


class MoviesRepository(AbstractElasticSearchRepository):
    @property
    def index_name(self) -> str:
        return "movies"

    @property
    def base_model(self) -> BaseModel:
        return FilmShort

    @es_backoff
    async def get(self, id: UUID) -> Optional[Film]:
        """Получить данные из индекса по uuid

        Args:
            id (UUID): идентификатор записи

        Returns:
            Optional[Film]: Pydantic модель, если
                            элемент был найден или None
        """
        try:
            data = await self.es_client.get(self.index_name, id)
        except NotFoundError:
            return None
        return Film(**data["_source"])

    @es_backoff
    async def search_by_genre_name(
        self,
        sort: str,
        page_number: int,
        page_size: int,
        genre_name: str,
    ) -> Optional[list[FilmShort]]:
        """поиск фильма по имени жанра

        Args:
            sort (str): поле сортировки
            page_number (int): номер страницы
            page_size (int): размер страницы ответа
            genre_name (str): имя жанра

        Returns:
            Optional[list[FilmShort]]: массив информации
                                по фильму - сокращенный
        """
        page = (page_number - 1) * page_size
        body = helper_genre_name(genre_name, page, page_size)
        if sort:
            sort_body = self._get_sort(sort)
            body.update(sort_body)

        data = await self.es_client.search(
            index=self.index_name,
            body=body,
        )
        data = data["hits"]["hits"]
        if len(data) > 0:
            return [FilmShort(**item["_source"]) for item in data]
        return None

    def _extract_role(self, person_name: str, data_item: dict) -> list[str]:
        """извлечь массив ролей в которые персона выполняет в фильме

        Args:
            person_name (str): имя персоны
            data_item (dict): массив данных по фильму

        Returns:
            list[str]: список ролей ["actor", "writer"]
        """
        roles = {
            "directors_names": "director",
            "actors_names": "actor",
            "writers_names": "writer",
        }
        result = set()
        for role_array in roles.keys():
            if person_name in data_item[role_array]:
                result.add(roles.get(role_array))
        return list(result)

    @es_backoff
    async def search_by_person(
        self,
        person_item: Person,
    ) -> Optional[PersonRole]:
        """найти фильмы по персоне

        Args:
            person_item (Person): модель персоны

        Returns:
            Optional[PersonRole]: необходимая для ответа модель -
                содержащая список фильмов с ролями по персоне
        """
        body = helper_person_roles(
            person_item.id,
            [
                "id",
                "directors_names",
                "actors_names",
                "writers_names",
            ],
            0,
            settings.MAX_BULK_QUERY_SIZE,
        )
        data = await self.es_client.search(
            index=self.index_name,
            body=body,
        )
        data = data["hits"]["hits"]
        result = PersonRole(**person_item.dict())
        if len(data) == 0:
            return None

        for data_item in data:
            data = data_item["_source"]
            film_info = FilmPersonRole(
                uuid=data.get("id"),
                roles=self._extract_role(person_item.full_name, data),
            )
            result.films.append(film_info)
        return result

    @es_backoff
    async def search_films_by_person(
        self, sort: str, page_number: int, page_size: int, person_item: Person
    ) -> Optional[list[FilmShort]]:
        """получить список фильмов с рейтингами по персоне

        Args:
            sort (str): поле сортировки
            page_number (int): номер страницы
            page_size (int): размер страницы ответа
            person_item (Person): объект персоны

        Returns:
            Optional[list[FilmShort]]: массив фильмов - сокращенная модель
        """
        page = (page_number - 1) * page_size
        body = helper_person_roles(
            person_item.id,
            [
                "id",
                "title",
                "imdb_rating",
            ],
            page,
            page_size,
        )
        if sort:
            sort_body = self._get_sort(sort)
            body.update(sort_body)

        data = await self.es_client.search(
            index=self.index_name,
            body=body,
        )
        data = data["hits"]["hits"]
        if len(data) > 0:
            return [FilmShort(**item["_source"]) for item in data]
        return None
