import pytest

from tests.data.params_genres import TEST_PARAMS_GENRES


@pytest.mark.parametrize(
    TEST_PARAMS_GENRES["test_all_genres_200"]["keys"],
    TEST_PARAMS_GENRES["test_all_genres_200"]["data"],
)
async def test_all_genres_200(
        make_get_request, query, expected_answer, message,
        ):
    # Request data
    body, status = await make_get_request(
        path=query["path"], query_data=query["data"]
    )
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert len(body) == expected_answer["length"], message["length"]


@pytest.mark.parametrize(
    TEST_PARAMS_GENRES["test_all_genres_404"]["keys"],
    TEST_PARAMS_GENRES["test_all_genres_404"]["data"],
)
async def test_all_genres_404(
        make_get_request, query, expected_answer, message,
        ):
    # Request data
    body, status = await make_get_request(
        path=query["path"], query_data=query["data"]
    )
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body["detail"] == expected_answer["detail"], message["detail"]


@pytest.mark.parametrize(
    TEST_PARAMS_GENRES["test_all_genres_422"]["keys"],
    TEST_PARAMS_GENRES["test_all_genres_422"]["data"],
)
async def test_all_genres_422(
        make_get_request, query, expected_answer, message,
        ):
    # Request data
    _, status = await make_get_request(
        path=query["path"], query_data=query["data"]
    )
    # Check the response
    assert status == expected_answer["status"], message["detail"]


@pytest.mark.parametrize(
    TEST_PARAMS_GENRES["test_search_genres_200"]["keys"],
    TEST_PARAMS_GENRES["test_search_genres_200"]["data"],
)
async def test_search_genres_200(
        make_get_request, query, expected_answer, message,
        ):
    # Request data
    body, status = await make_get_request(
        path=query["path"], query_data=query["data"]
    )
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert len(body) == expected_answer["length"], message["length"]


@pytest.mark.parametrize(
    TEST_PARAMS_GENRES["test_search_genres_404"]["keys"],
    TEST_PARAMS_GENRES["test_search_genres_404"]["data"],
)
async def test_search_genres_404(
        make_get_request, query, expected_answer, message,
        ):
    # Request data
    body, status = await make_get_request(
        path=query["path"], query_data=query["data"]
    )
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body["detail"] == expected_answer["detail"], message["detail"]


@pytest.mark.parametrize(
    TEST_PARAMS_GENRES["test_search_genres_422"]["keys"],
    TEST_PARAMS_GENRES["test_search_genres_422"]["data"],
)
async def test_search_genres(
        make_get_request, query, expected_answer, message,
        ):
    # Request data
    _, status = await make_get_request(
        path=query["path"], query_data=query["data"]
    )
    # Check the response
    assert status == expected_answer["status"], message["detail"]


@pytest.mark.parametrize(
    TEST_PARAMS_GENRES["test_search_genres_by_id_200"]["keys"],
    TEST_PARAMS_GENRES["test_search_genres_by_id_200"]["data"],
)
async def test_search_genres_by_id_200(
        make_get_request, query, expected_answer, message,
        ):
    # Request data
    body, status = await make_get_request(path=query["path"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body["name"] == expected_answer["name"], message["name"]


@pytest.mark.parametrize(
    TEST_PARAMS_GENRES["test_search_genres_by_id_404"]["keys"],
    TEST_PARAMS_GENRES["test_search_genres_by_id_404"]["data"],
)
async def test_search_genres_by_id_404(
        make_get_request, query, expected_answer, message,
        ):
    # Request data
    body, status = await make_get_request(path=query["path"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body["detail"] == expected_answer["detail"], message["detail"]


@pytest.mark.parametrize(
    TEST_PARAMS_GENRES["test_redis_genres"]["keys"],
    TEST_PARAMS_GENRES["test_redis_genres"]["data"],
)
async def test_redis_genres(
        make_get_request, get_redis, query, expected_answer, message,
        ):
    redis_client = get_redis
    # Request data
    _, _ = await make_get_request(path=query["path"])
    # Check the response
    assert (
        redis_client.exists(query["key_redis"]) == expected_answer["key_redis"]
    ), message["key_redis"]
