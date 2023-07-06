from http import HTTPStatus
from typing import Optional, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from core.config import settings
from models.film import FilmShort, Film
from services.movies import FilmService, get_film_service
from services.redis_cache import CacheRedis, get_cache_service

router = APIRouter()


@router.get("/", response_model=list[FilmShort])
async def all_films(
    genre: Optional[UUID] = None,
    sort: str = "-imdb_rating",
    page_number: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 10,
    film_service: FilmService = Depends(get_film_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> list[FilmShort]:
    """
    Получить все фильмы, также есть возможность фильтрации API
    по id жанра в фильме
    """
    key_cache = cache_service.create_key_by_list(
        genre=genre,
        query=None,
        sort=sort,
        page_number=page_number,
        page_size=page_size,
        service=film_service,
    )

    films = await cache_service.get_list(key=key_cache, model=FilmShort)

    if not films:
        films = await film_service.search_by_genre_name(
            genre, sort, page_number, page_size
        )
        if not films:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=film_service.no_films_error,
            )
        await cache_service.set_list(
            key=key_cache, data=films, expire=settings.CACHE_EXPIRE_IN_SECONDS
        )

    return jsonable_encoder(films)


@router.get("/search", response_model=list[FilmShort])
async def film_search(
    query: str,
    sort: str = "imdb_rating",
    page_number: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 10,
    film_service: FilmService = Depends(get_film_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> list[FilmShort]:
    """
    Найти фильмы в базе данных по
    текстовому поиску.
    """
    key_cache = cache_service.create_key_by_list(
        genre=None,
        query=query,
        sort=sort,
        page_number=page_number,
        page_size=page_size,
        service=film_service,
    )
    films = await cache_service.get_list(key=key_cache, model=FilmShort)

    if not films:
        films = await film_service.search(sort, page_number, page_size, query)
        if not films:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=film_service.search_error,
            )
        await cache_service.set_list(
            key=key_cache, data=films, expire=settings.CACHE_EXPIRE_IN_SECONDS
        )

    return jsonable_encoder(films)


@router.get("/{film_id}", response_model=Film)
async def film_details(
    film_id: UUID,
    film_service: FilmService = Depends(get_film_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> Film:
    """
    Найти фильм в базе данных по его ID.
    """
    key_cache = cache_service.create_key_by_id(
        id=film_id, service=film_service
    )
    film = await cache_service.get_id(key_cache, Film)

    if not film:
        film = await film_service.get(film_id)
        if not film:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=film_service.not_found_error,
            )
        await cache_service.set_id(
            key=key_cache, data=film, expire=settings.CACHE_EXPIRE_IN_SECONDS
        )

    return jsonable_encoder(film.dict(by_alias=True))
