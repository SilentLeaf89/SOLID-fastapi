from http import HTTPStatus



test_all_genres_200 = [
    (
        {
            "path": "/api/v1/genres/",
            "data": {"page_number": 1, "page_size": 27}
        },
        {
            "length": 14,
            "status": HTTPStatus.OK
        },
        {
            "length": "The results of getting all genres are incorrect!",
            "status": "Status of response is unsuccessful!",
        },
    ),
    (
        {
            "path": "/api/v1/genres/",
            "data": {"page_number": 2, "page_size": 13}
        },
        {
            "length": 1,
            "status": HTTPStatus.OK,
        },
        {
            "length": "The results of getting all genres are incorrect!",
            "status": "Status of response is unsuccessful!",
        },
    ),
]

test_all_genres_404 = [
    (
        {
            "path": "/api/v1/genres/",
            "data": {"page_number": 4, "page_size": 10}
        },
        {
            "status": HTTPStatus.NOT_FOUND,
            "detail": "Genres not found"
        },
        {
            "status": "Status of response is incorrect!",
            "detail": "The message of search is incorrect!",
        },
    ),
]

test_all_genres_422 = [
    (
        {
            "path": "/api/v1/genres/",
            "data": {"page_number": -5, "page_size": 10}
        },
        {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY
        },
        {
            "detail": "Validation didn't work"
        }
    ),
    (
        {
            "path": "/api/v1/genres/",
            "data": {"page_number": 2, "page_size": -3}
        },
        {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY
        },
        {
            "detail": "Validation didn't work"
        }
    ),
    (
        {
            "path": "/api/v1/genres/",
            "data": {"page_number": -1, "page_size": -1}
        },
        {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY
        },
        {
            "detail": "Validation didn't work"
        }
    ),
    (
        {
            "path": "/api/v1/genres/",
            "data": {"page_number": 0, "page_size": 0}
        },
        {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY
        },
        {
            "detail": "Validation didn't work"
        }
    ),
]

test_search_genres_200 = [
    (
        {
            "path": "/api/v1/genres/search/",
            "data": {"query": "Documentary", "page_size": 1},
        },
        {
            "status": HTTPStatus.OK,
            "length": 1
        },
        {
            "status": "Status of response is unsuccessful!",
            "length": "The results of search are incorrect!",
        }
    ),
]

test_search_genres_404 = [
    (
        {
            "path": "/api/v1/genres/search/",
            "data": {"query": "Eqvilibrium", "page_size": 1},
        },
        {
            "status": HTTPStatus.NOT_FOUND,
            "detail": "Genres not found"
        },
        {
            "status": "Status of response is incorrect!",
            "detail": "The message of search is incorrect!",
        },
    ),
    (
        {
            "path": "/api/v1/genres/search/",
            "data": {"query": "Action", "page_number": 2},
        },
        {
            "status": HTTPStatus.NOT_FOUND,
            "detail": "Genres not found"
        },
        {
            "status": "Status of response is unsuccessful!",
            "detail": "The message of search is incorrect!",
        },
    ),
]

test_search_genres_422 = [
    (
        {
            "path": "/api/v1/genres/search/",
            "data": {"query": "Documentary", "page_number": -2},
        },
        {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY
        },
        {
            "detail": "Validation didn't work"
        }
    ),
    (
        {
            "path": "/api/v1/genres/search/",
            "data": {"uuid": ""},
        },
        {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY
        },
        {
            "detail": "Validation didn't work"
        }
    ),
]

test_search_genres_by_id_200 = [
    (
        {
            "path": "/api/v1/genres/ca124c76-9760-4406-bfa0-409b1e38d200",
        },
        {
            "status": HTTPStatus.OK,
            "name": "Biography"
        },
        {
            "status": "Status of response is incorrect!",
            "name": "The results of search are incorrect!",
        },
    ),
]

test_search_genres_by_id_404 = [
    (
        {
            "path": "/api/v1/genres/ea9ee6e6-0077-4ad3-b4d6-8701f7222b67"
        },
        {
            "status": HTTPStatus.NOT_FOUND,
            "detail": "Genres not found"
        },
        {
            "status": "Status of response is incorrect!",
            "detail": "The results of search are incorrect!",
        },
    ),
]

test_redis_genres = [
    (
        {
            "path": "/api/v1/genres/",
            "key_redis": "genres_genre_None_query_None_sort_name_p_num_1_p_size_10",
        },
        {
            "key_redis": True
        },
        {
            "key_redis": "The data does not exist in Redis after the endpoint execution!"
        },
    )
]


TEST_PARAMS_GENRES = {
    "test_all_genres_200": {
        "keys": "query, expected_answer, message",
        "data": test_all_genres_200,
    },
    "test_all_genres_404": {
        "keys": "query, expected_answer, message",
        "data": test_all_genres_404,
    },
    "test_all_genres_422": {
        "keys": "query, expected_answer, message",
        "data": test_all_genres_422,
    },
    "test_search_genres_200": {
        "keys": "query, expected_answer, message",
        "data": test_search_genres_200,
    },
    "test_search_genres_404": {
        "keys": "query, expected_answer, message",
        "data": test_search_genres_404,
    },
    "test_search_genres_422": {
        "keys": "query, expected_answer, message",
        "data": test_search_genres_422,
    },
    "test_search_genres_by_id_200": {
        "keys": "query, expected_answer, message",
        "data": test_search_genres_by_id_200,
    },
    "test_search_genres_by_id_404": {
        "keys": "query, expected_answer, message",
        "data": test_search_genres_by_id_404,
    },
    "test_redis_genres": {
        "keys": "query, expected_answer, message",
        "data": test_redis_genres,
    },
}
