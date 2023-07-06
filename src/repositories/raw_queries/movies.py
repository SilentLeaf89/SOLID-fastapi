from typing import Any
from uuid import UUID


def helper_genre_name(
    genre_name: str, page: int, page_size: int
) -> dict[str, Any]:
    return {
        "from": page,
        "query": {
            "term": {
                "genre": genre_name,
            }
        },
        "size": page_size,
    }


def helper_person_roles(
    person_id: UUID, fields_list: list, page: int, page_size: int
) -> dict[str, Any]:
    return {
        "from": page,
        "query": {
            "bool": {
                "should": [
                    {
                        "nested": {
                            "path": "actors",
                            "query": {
                                "term": {"actors.id": {"value": person_id}}
                            },
                        }
                    },
                    {
                        "nested": {
                            "path": "directors",
                            "query": {
                                "term": {"directors.id": {"value": person_id}}
                            },
                        }
                    },
                    {
                        "nested": {
                            "path": "writers",
                            "query": {
                                "term": {"writers.id": {"value": person_id}}
                            },
                        }
                    },
                ]
            }
        },
        "size": page_size,
        "_source": fields_list,
    }
