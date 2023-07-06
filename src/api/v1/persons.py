from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from core.config import settings
from models.film import FilmShort
from models.person import Person, PersonRole
from services.persons import PersonService, get_person_service
from services.redis_cache import CacheRedis, get_cache_service

router = APIRouter()


# такую ручку тоже не просят
@router.get("/", response_model=list[Person])
async def persons_all(
    sort: str = "name",
    page_number: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 10,
    person_service: PersonService = Depends(get_person_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> list[Person]:
    """Получить список всеx персон.

    - **sort**: Сортировка по полю (по умолчанию: "name").
    Для сортировки в обратном порядке допускается использовать `-`.
    - **page_number**: номер текущей страницы (по умолчанию: 1).
    - **page_size**: количество персон на странице (по умолчанию: 10).
    """
    key_cache = cache_service.create_key_by_list(
        genre=None,
        query=None,
        sort=sort,
        page_number=page_number,
        page_size=page_size,
        service=person_service,
    )
    persons = await cache_service.get_list(key=key_cache, model=Person)

    if not persons:
        persons = await person_service.search(sort, page_number, page_size)
        if not persons:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=person_service.not_found_error,
            )
        await cache_service.set_list(
            key=key_cache,
            data=persons,
            expire=settings.CACHE_EXPIRE_IN_SECONDS,
        )

    return jsonable_encoder(persons)


@router.get("/search", response_model=list[PersonRole])
async def persons_search(
    query: str,
    sort: str = "full_name",
    page_number: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 10,
    person_service: PersonService = Depends(get_person_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> list[PersonRole]:
    """Найти персону

    Возвращает список персон удовлетворяющих критерию

    - **query**: Поисковый запрос
    - **sort**: Сортировка по полю (по умолчанию: "full_name").
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
        service=person_service,
    )
    persons = await cache_service.get_list(key=key_cache, model=PersonRole)

    if not persons:
        persons = await person_service.search_roles_by_person_name(
            sort, page_number, page_size, query
        )
        if not persons:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=person_service.not_found_error,
            )
        await cache_service.set_list(
            key=key_cache,
            data=persons,
            expire=settings.CACHE_EXPIRE_IN_SECONDS,
        )

    return jsonable_encoder(persons)


@router.get("/{person_id}", response_model=PersonRole)
async def persons_details(
    person_id: UUID,
    person_service: PersonService = Depends(get_person_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> PersonRole:
    """Найти персону по id

    Возвращает одну персону по ее идентификатору или `Person not found`

    - **person_id**: идентификатор персоны
    """
    key_cache = cache_service.create_key_by_id(
        id=person_id, service=person_service
    )
    person = await cache_service.get_id(key_cache, PersonRole)
    if not person:
        person = await person_service.search_roles_by_person_id(person_id)
        if not person:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=person_service.not_found_error,
            )
        await cache_service.set_id(
            key=key_cache, data=person, expire=settings.CACHE_EXPIRE_IN_SECONDS
        )

    return jsonable_encoder(person)


@router.get("{person_id}/film", response_model=list[FilmShort])
async def person_film(
    person_id: UUID,
    sort: str = "imdb_rating",
    page_number: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 10,
    person_service: PersonService = Depends(get_person_service),
    cache_service: CacheRedis = Depends(get_cache_service),
) -> list[FilmShort]:
    """получить список фильмов по идентификатору персоны

    - **person_id**: id персоны
    - **sort**: Сортировка по полю (по умолчанию: "name").
    Для сортировки в обратном порядке допускается использовать `-`.
    - **page_number**: Номер текущей страницы (по умолчанию: 1).
    - **page_size**: Количество персон на странице (по умолчанию: 10).
    """
    key_cache = cache_service.create_key_by_list(
        genre=None,
        query=person_id,
        sort=sort,
        page_number=page_number,
        page_size=page_size,
        service=person_service,
    )
    films = await cache_service.get_list(key=key_cache, model=FilmShort)

    if not films:
        films = await person_service.search_films_by_person_id(
            sort, page_number, page_size, person_id
        )
        if not films:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=person_service.not_found_error,
            )
        await cache_service.set_list(
            key=key_cache, data=films, expire=settings.CACHE_EXPIRE_IN_SECONDS
        )

    return jsonable_encoder(films)
