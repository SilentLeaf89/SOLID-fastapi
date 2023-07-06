from typing import Optional
from uuid import UUID
from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models.film import FilmShort
from repositories.movies import MoviesRepository
from repositories.genres import GenresRepository
from .es_search import BaseService


class FilmService(BaseService):
    """Сервис для поиска фильмов"""

    not_found_error = "Film not found"
    search_error = "Matching films are not found"
    no_films_error = "No films in index"

    def __init__(
        self, repository: MoviesRepository, genre_repository: GenresRepository
    ) -> None:
        super().__init__(repository)
        self.genre_repository = genre_repository

    async def search_by_genre_name(
        self, genre: UUID | None, sort: str, page_number: int, page_size: int
    ) -> Optional[list[FilmShort]]:
        if not genre:
            result = await self.repository.search(sort, page_number, page_size)
            return result
        genre_item = await self.genre_repository.get(genre)
        result = await self.repository.search_by_genre_name(
            sort, page_number, page_size, genre_item.name
        )
        return result


@lru_cache
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    repository = MoviesRepository(elastic)
    genre_repository = GenresRepository(elastic)
    return FilmService(repository, genre_repository)
