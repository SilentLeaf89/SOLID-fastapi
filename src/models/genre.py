from pydantic import Field
from uuid import UUID

from models.base import Base


class Genre(Base):
    id: UUID = Field(alias="uuid")
    name: str
    description: str = ""

    @staticmethod
    def get_search_fields() -> list[str]:
        return [
            "name",
            "name.raw",
            "description",
        ]

    @staticmethod
    def get_sort_fields() -> dict[str, str]:
        return {
            "name": "name.raw",
            "description": "description",
        }
