from typing import Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from functools import lru_cache

from db.elastic import get_elastic
from models.film import FilmShort
from models.person import PersonRole
from repositories.movies import MoviesRepository
from repositories.persons import PersonsRepository

from .es_search import BaseService


class PersonService(BaseService):
    """Сервис для поиска персон"""

    not_found_error = "Persons not found"

    def __init__(
        self, repository: PersonsRepository, movie_repository: MoviesRepository
    ) -> None:
        super().__init__(repository)
        self.movie_repository = movie_repository

    async def search_roles_by_person_name(
        self, sort: str, page_number: int, page_size: int, query: str = None
    ) -> Optional[list[PersonRole]]:
        persons = await self.repository.search(
            sort, page_number, page_size, query
        )
        if not persons:
            return None
        result = []
        for person in persons:
            person_movie = await self.movie_repository.search_by_person(person)
            result.append(person_movie)
        return result

    async def search_roles_by_person_id(
        self, person_id: UUID
    ) -> Optional[PersonRole]:
        person = await self.repository.get(person_id)
        if not person:
            return None
        result = await self.movie_repository.search_by_person(person)
        return result

    async def search_films_by_person_id(
        self, sort: str, page_number: int, page_size: int, person_id: UUID
    ) -> Optional[FilmShort]:
        person = await self.repository.get(person_id)
        if not person:
            return None
        result = await self.movie_repository.search_films_by_person(
            sort, page_number, page_size, person
        )
        return result


@lru_cache
def get_person_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    repository = PersonsRepository(elastic)
    movie_repository = MoviesRepository(elastic)
    return PersonService(repository, movie_repository)
