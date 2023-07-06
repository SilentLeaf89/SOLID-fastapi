from pydantic import Field
from uuid import UUID

from .base import Base


class Person(Base):
    id: UUID = Field(alias="uuid")
    full_name: str

    @staticmethod
    def get_search_fields() -> list[str]:
        return [
            "full_name",
            "full_name.raw",
        ]

    @staticmethod
    def get_sort_fields() -> dict[str, str]:
        return {
            "full_name": "full_name.raw",
        }


class Writer(Person):
    ...


class Director(Person):
    ...


class Actor(Person):
    ...


class FilmPersonRole(Base):
    id: UUID = Field(alias="uuid")
    roles: list[str]


class PersonRole(Person):
    films: list[FilmPersonRole] = []

    class Config:
        json_encoders = {
            FilmPersonRole: lambda s: str(s),
        }
