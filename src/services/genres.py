from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from functools import lru_cache

from db.elastic import get_elastic
from repositories.genres import GenresRepository

from .es_search import BaseService


class GenreService(BaseService):
    """Сервис для поиска жанров"""

    not_found_error = "Genres not found"


@lru_cache
def get_genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    repository = GenresRepository(elastic)
    return GenreService(repository)
