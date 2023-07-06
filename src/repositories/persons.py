from pydantic import BaseModel

from models.person import Person

from .abstract_search import AbstractElasticSearchRepository


class PersonsRepository(AbstractElasticSearchRepository):
    @property
    def index_name(self) -> str:
        return "persons"

    @property
    def base_model(self) -> BaseModel:
        return Person
