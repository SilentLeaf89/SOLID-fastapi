from http import HTTPStatus

test_all_films = [
    (
        {"path": "/api/v1/films/", "data": {"page_size": 1000}},
        {"length": 3, "status": HTTPStatus.OK},
        {
            "status": "Status of response is unsuccessful!",
            "length": "The results of getting all persons are incorrect!",
        },
    ),
    (
        {"path": "/api/v1/films/", "data": {"page_size": 1}},
        {"length": 1, "status": HTTPStatus.OK},
        {
            "status": "Status of response is unsuccessful!",
            "length": "The results of getting all persons are incorrect!",
        },
    ),
]

test_search_films_200 = [
    (
        {
            "path": "/api/v1/films/search/",
            "data": {"query": "The Star", "page_size": 4},
        },
        {"status": HTTPStatus.OK, "length": 3},
        {
            "status": "Status of response is unsuccessful!",
            "length": "The results of search are incorrect!",
        },
    ),
]

test_search_films_404 = [
    # Test search with pagination when there is no data
    (
        {
            "path": "/api/v1/films/search/",
            "data": {"query": "The Star", "page_size": 4, "page_number": 2},
        },
        {"status": HTTPStatus.NOT_FOUND, "detail": "Matching films are not found"},
        {
            "status": "Status of response is unsuccessful!",
            "detail": "The message of search is incorrect!",
        },
    ),
    (
        {
            "path": "/api/v1/films/search/",
            "data": {"query": "Mashed potato", "page_size": 4},
        },
        {"status": HTTPStatus.NOT_FOUND, "detail": "Matching films are not found"},
        {
            "status": "Status of response is unsuccessful!",
            "detail": "The message of search is incorrect!",
        },
    ),
]

test_search_films_by_id_200 = [
    (
        {"path": "/api/v1/films/ea9ee6e6-0077-4ad3-b4d6-8701f7222b67"},
        {"status": HTTPStatus.OK, "title": "The Star"},
        {
            "status": "Status of response is incorrect!",
            "title": "The results of search are incorrect!",
        },
    ),
]

test_search_films_by_id_404 = [
    (
        {"path": "/api/v1/films/ea9ee6e6-0077-4ad3-b4d6-8701f7222b68"},
        {"status": HTTPStatus.NOT_FOUND, "detail": "Film not found"},
        {
            "status": "Status of response is incorrect!",
            "detail": "The message of search is incorrect!",
        },
    ),
]

test_redis_in_films = [
    (
        {
            "path": "/api/v1/films/search/",
            "data": {"query": "The Star", "page_size": 2},
            "key_redis": "movies_genre_None_query_The Star_sort_imdb_rating_p_num_1_p_size_2",
        },
        {"key_redis": True},
        {"key_redis": "The data does not exist in Redis after the endpoint execution!"},
    )
]

TEST_PARAMS_FILMS = {
    "test_all_films": {
        "keys": "query, expected_answer, message",
        "data": test_all_films,
    },
    "test_search_films_200": {
        "keys": "query, expected_answer, message",
        "data": test_search_films_200,
    },
    "test_search_films_404": {
        "keys": "query, expected_answer, message",
        "data": test_search_films_404,
    },
    "test_search_films_by_id_200": {
        "keys": "query, expected_answer, message",
        "data": test_search_films_by_id_200,
    },
    "test_search_films_by_id_404": {
        "keys": "query, expected_answer, message",
        "data": test_search_films_by_id_404,
    },
    "test_redis_in_films": {
        "keys": "query, expected_answer, message",
        "data": test_redis_in_films,
    },
}
