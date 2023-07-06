from http import HTTPStatus



test_all_persons_200 = [
    (
        {"path": "/api/v1/persons/", "data": {"page_size": 1000}},
        {"length": 5, "status": HTTPStatus.OK},
        {
            "status": "Status of response is unsuccessful!",
            "length": "The results of getting all persons are incorrect!",
        },
    )
]



test_search_persons_200 = [
    (
        {"path": "/api/v1/persons/search/", "data": {"query": "Ben", "page_size": 4}},
        {"status": HTTPStatus.OK, "length": 1},
        {
            "status": "Status of response is unsuccessful!",
            "length": "The results of search are incorrect!",
        },
    ),
]

test_search_persons_404 = [
    (
        {
            "path": "/api/v1/persons/search/",
            "data": {"query": "Abrakadabra", "page_size": 4},
        },
        {"status": HTTPStatus.NOT_FOUND, "detail": "Persons not found"},
        {
            "status": "Status of response is unsuccessful!",
            "detail": "The message of search is incorrect!",
        },
    ),
]


test_search_persons_by_id_200 = [
    (
        {"path": "/api/v1/persons/4964d362-4ce7-48c1-a718-4b0d4740040b"},
        {"status": HTTPStatus.OK, "full_name": "Ann"},
        {
            "status": "Status of response is incorrect!",
            "full_name": "The results of search are incorrect!",
        },
    ),
]

test_search_persons_by_id_404 = [
    (
        {"path": "/api/v1/persons/4964d362-4ce7-48c1-a718-4b0d4740041b"},
        {"status": HTTPStatus.NOT_FOUND, "detail": "Persons not found"},
        {
            "status": "Status of response is incorrect!",
            "detail": "The message of failed search is incorrect!",
        },
    ),
]

test_redis_in_persons = [
    (
        {
            "path": "/api/v1/persons/search/",
            "data": {"query": "Ben", "page_size": 5},
            "key_redis": "persons_genre_None_query_Ben_sort_full_name_p_num_1_p_size_5",
        },
        {"key_redis": True},
        {"key_redis": "The data does not exist in Redis after the endpoint execution!"},
    )
]

test_search_films_by_persons_200 = [
    (
        {"path": "/api/v1/persons/4964d362-4ce7-48c1-a718-4b0d4740040b"},
        {"status": HTTPStatus.OK, "length": 2},
        {
            "status": "Status of response is incorrect!",
            "length": "The length of the response is incorrect!",
        },
    ),
]

test_search_films_by_persons_404 = [
    (
        {"path": "/api/v1/persons/4964d362-4ce7-48c1-a718-4b0d4740041b"},
        {"status": HTTPStatus.NOT_FOUND, "detail": "Persons not found"},
        {
            "status": "Status of response is incorrect!",
            "detail": "The message of failed search is incorrect!",
        },
    ),
]

TEST_PARAMS_PERSONS = {
    "test_all_persons_200": {
        "keys": "query, expected_answer, message",
        "data": test_all_persons_200,
    },
    "test_search_persons_200": {
        "keys": "query, expected_answer, message",
        "data": test_search_persons_200,
    },
    "test_search_persons_404": {
        "keys": "query, expected_answer, message",
        "data": test_search_persons_404,
    },
    "test_search_persons_by_id_200": {
        "keys": "query, expected_answer, message",
        "data": test_search_persons_by_id_200,
    },
    "test_search_persons_by_id_404": {
        "keys": "query, expected_answer, message",
        "data": test_search_persons_by_id_404,
    },
    "test_redis_in_persons": {
        "keys": "query, expected_answer, message",
        "data": test_redis_in_persons,
    },
    "test_search_films_by_persons_200": {
        "keys": "query, expected_answer, message",
        "data": test_search_films_by_persons_200,
    },
    "test_search_films_by_persons_404": {
        "keys": "query, expected_answer, message",
        "data": test_search_films_by_persons_404,
    },
}
