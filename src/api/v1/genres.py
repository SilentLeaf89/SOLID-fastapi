from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from core.config import settings
from models.genre import Genre
from services.genres import GenreService, get_genre_service
from services.redis_cache import CacheRedis, get_cache_service

router = APIRouter()


@router.get("/", response_model=list[Genre])
async def genres_all(
    sort: str = "name",
    page_number: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 10,
    genre_service: GenreService = Depends(get_genre_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> list[Genre]:
    """Получить список всех жанров

    - **sort**: Сортировка по полю (по умолчанию: "name").
    Для сортировки в обратном порядке допускается использовать `-`.
    - **page_number**: Номер текущей страницы (по умолчанию: 1).
    - **page_size**: Количество персон на странице (по умолчанию: 10).
    """
    key_cache = cache_service.create_key_by_list(
        genre=None,
        query=None,
        sort=sort,
        page_number=page_number,
        page_size=page_size,
        service=genre_service,
    )
    genres = await cache_service.get_list(key=key_cache, model=Genre)

    if not genres:
        genres = await genre_service.search(sort, page_number, page_size)
        if not genres:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=genre_service.not_found_error,
            )
        await cache_service.set_list(
            key=key_cache, data=genres, expire=settings.CACHE_EXPIRE_IN_SECONDS
        )

    return jsonable_encoder(genres)


@router.get("/search", response_model=list[Genre])
async def genres_search(
    query: str,
    sort: str = "name",
    page_number: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 10,
    genre_service: GenreService = Depends(get_genre_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> list[Genre]:
    """Найти жанр

    Возвращает список жанров удовлетворяющих критерию

    - **query**: Поисковый запрос
    - **sort**: Сортировка по полю (по умолчанию: "name").
    Для сортировки в обратном порядке допускается использовать `-`.
    - **page_number**: Номер текущей страницы (по умолчанию: 1).
    - **page_size**: Количество персон на странице (по умолчанию: 10).
    """
    key_cache = cache_service.create_key_by_list(
        genre=None,
        query=query,
        sort=sort,
        page_number=page_number,
        page_size=page_size,
        service=genre_service,
    )
    genres = await cache_service.get_list(key=key_cache, model=Genre)

    if not genres:
        genres = await genre_service.search(
            sort, page_number, page_size, query
        )
        if not genres:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=genre_service.not_found_error,
            )
        await cache_service.set_list(
            key=key_cache, data=genres, expire=settings.CACHE_EXPIRE_IN_SECONDS
        )

    return jsonable_encoder(genres)


@router.get("/{genre_id}", response_model=Genre)
async def gendes_details(
    genre_id: UUID,
    genre_service: GenreService = Depends(get_genre_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> Genre:
    """
    Найти жанр по id

    Возвращает один жанр по идентификатору или `Genre not found`

    - **genre_id**: идентификатор жанра
    """
    key_cache = cache_service.create_key_by_id(
        id=genre_id, service=genre_service
    )
    genre = await cache_service.get_id(key_cache, Genre)

    if not genre:
        genre = await genre_service.get(genre_id)
        if not genre:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=genre_service.not_found_error,
            )
        await cache_service.set_id(
            key=key_cache, data=genre, expire=settings.CACHE_EXPIRE_IN_SECONDS
        )

    return jsonable_encoder(genre)
