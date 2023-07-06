from pydantic import Field
from typing import Optional
from uuid import UUID

from models.base import Base

from .person import Writer, Director, Actor


class FilmShort(Base):
    id: UUID = Field(alias="uuid")
    title: str
    imdb_rating: Optional[float]

    @staticmethod
    def get_search_fields() -> list[str]:
        return [
            "title",
            "title.raw",
            "description",
        ]

    @staticmethod
    def get_sort_fields() -> dict[str, str]:
        return {
            "title": "title.raw",
            "imdb_rating": "imdb_rating",
            "description": "description",
        }


class Film(FilmShort):
    description: str
    genre: list[str]
    actors: list[Actor]
    writers: list[Writer]
    directors: list[Director]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]

    class Config:
        json_encoders = {
            Actor: lambda s: str(s),
            Writer: lambda s: str(s),
            Director: lambda s: str(s),
        }
