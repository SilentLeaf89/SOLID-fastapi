import random
import uuid


movies_data = [
    # Film 1
    {
        "id": "ea9ee6e6-0077-4ad3-b4d6-8701f7222b67",
        "imdb_rating": 8.5,
        "genre": ["Action", "Sci-Fi"],
        "title": "The Star",
        "description": "New World",
        "directors_names": ["Stan"],
        "actors_names": ["Ann"],
        "writers_names": ["Ben", "Howard"],
        "actors": [
            {"id": "4964d362-4ce7-48c1-a718-4b0d4740040b", "full_name": "Ann"},
        ],
        "writers": [
            {"id": "23e06d43-c00d-4b05-82a1-37d70a2eb908", "full_name": "Ben"},
            {"id": "d308b094-81cd-4962-811a-09cab673015e", "full_name": "Howard"},
        ],
        "directors": [
            {"id": "06750970-c75a-4b82-b971-389d6560e430", "full_name": "Stan"}
        ],
    },
    # Film 2
    {
        "id": "8dbdd60b-3068-4365-8979-70b91ed3fada",
        "imdb_rating": 8.5,
        "genre": ["Action", "Sci-Fi"],
        "title": "The Star",
        "description": "New World",
        "directors_names": ["Stan"],
        "actors_names": ["Bob"],
        "writers_names": ["Ben"],
        "actors": [
            {"id": "ecd34ee2-bae0-45c5-a69c-e176b77241bd", "full_name": "Bob"},
        ],
        "writers": [{"id": "23e06d43-c00d-4b05-82a1-37d70a2eb908", "full_name": "Ben"}],
        "directors": [
            {"id": "de9844a7-7a30-488a-be90-6df60c642376", "full_name": "Stan"}
        ],
    },
    # Film 3
    {
        "id": "9e5e9b6a-46aa-48a2-85e7-10ecc5fa0406",
        "imdb_rating": 8.5,
        "genre": ["Action", "Sci-Fi"],
        "title": "The Star",
        "description": "New World",
        "directors_names": ["Ben"],
        "actors_names": ["Ann", "Bob"],
        "writers_names": ["Howard"],
        "actors": [
            {"id": "4964d362-4ce7-48c1-a718-4b0d4740040b", "full_name": "Ann"},
            {"id": "ecd34ee2-bae0-45c5-a69c-e176b77241bd", "full_name": "Bob"},
        ],
        "writers": [
            {"id": "d308b094-81cd-4962-811a-09cab673015e", "full_name": "Howard"},
        ],
        "directors": [
            {"id": "23e06d43-c00d-4b05-82a1-37d70a2eb908", "full_name": "Ben"}
        ],
    },
]


persons_data = [
    {"id": "4964d362-4ce7-48c1-a718-4b0d4740040b", "full_name": "Ann"},
    {"id": "ecd34ee2-bae0-45c5-a69c-e176b77241bd", "full_name": "Bob"},
    {"id": "23e06d43-c00d-4b05-82a1-37d70a2eb908", "full_name": "Ben"},
    {"id": "d308b094-81cd-4962-811a-09cab673015e", "full_name": "Howard"},
    {"id": "06750970-c75a-4b82-b971-389d6560e430", "full_name": "Stan"},
]



# genre count = 14
genres_data = [
  {
    "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
    "name": "Action",
    "description": ""
  },
  {
    "id": "ca124c76-9760-4406-bfa0-409b1e38d200",
    "name": "Biography",
    "description": ""
  },
  {
    "id": "5373d043-3f41-4ea8-9947-4b746c601bbd",
    "name": "Comedy",
    "description": ""
  },
  {
    "id": "6d141ad2-d407-4252-bda4-95590aaf062a",
    "name": "Documentary",
    "description": ""
  },
  {
    "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
    "name": "Fantasy",
    "description": ""
  },
  {
    "id": "fb58fd7f-7afd-447f-b833-e51e45e2a778",
    "name": "Game-Show",
    "description": ""
  },
  {
    "id": "eb7212a7-dd10-4552-bf7b-7a505a8c0b95",
    "name": "History",
    "description": ""
  },
  {
    "id": "56b541ab-4d66-4021-8708-397762bff2d4",
    "name": "Music",
    "description": ""
  },
  {
    "id": "f24fd632-b1a5-4273-a835-0119bd12f829",
    "name": "News",
    "description": ""
  },
  {
    "id": "e508c1c8-24c0-4136-80b4-340c4befb190",
    "name": "Reality-TV",
    "description": ""
  },
  {
    "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
    "name": "Sci-Fi",
    "description": ""
  },
  {
    "id": "2f89e116-4827-4ff4-853c-b6e058f71e31",
    "name": "Sport",
    "description": ""
  },
  {
    "id": "526769d7-df18-4661-9aa6-49ed24e9dfd8",
    "name": "Thriller",
    "description": ""
  },
  {
    "id": "c020dab2-e9bd-4758-95ca-dbe363462173",
    "name": "War",
    "description": ""
  },
]


TEST_DATA = {
    "movies": movies_data,
    "persons": persons_data,
    "genres": genres_data
}