from pydantic import BaseModel


from models.genre import Genre
from .abstract_search import AbstractElasticSearchRepository


class GenresRepository(AbstractElasticSearchRepository):
    @property
    def index_name(self) -> str:
        return "genres"

    @property
    def base_model(self) -> BaseModel:
        return Genre
