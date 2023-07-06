import pytest

from tests.data.params_persons import TEST_PARAMS_PERSONS


@pytest.mark.parametrize(
    TEST_PARAMS_PERSONS["test_all_persons_200"]["keys"],
    TEST_PARAMS_PERSONS["test_all_persons_200"]["data"],
)
async def test_all_persons_200(
        make_get_request, query, expected_answer, message
        ):
    # Request data
    body, status = await make_get_request(path=query["path"], query_data=query["data"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert len(body) == expected_answer["length"], message["length"]


@pytest.mark.parametrize(
    TEST_PARAMS_PERSONS["test_search_persons_200"]["keys"],
    TEST_PARAMS_PERSONS["test_search_persons_200"]["data"],
)
async def test_search_persons_200(
        make_get_request, query, expected_answer, message
        ):
    # Request data
    body, status = await make_get_request(path=query["path"], query_data=query["data"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert len(body) == expected_answer["length"], message["length"]


@pytest.mark.parametrize(
    TEST_PARAMS_PERSONS["test_search_persons_404"]["keys"],
    TEST_PARAMS_PERSONS["test_search_persons_404"]["data"],
)
async def test_search_persons_404(
        make_get_request, query, expected_answer, message
        ):
    # Request data
    body, status = await make_get_request(path=query["path"], query_data=query["data"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body["detail"] == expected_answer["detail"], message["detail"]


@pytest.mark.parametrize(
    TEST_PARAMS_PERSONS["test_search_persons_by_id_200"]["keys"],
    TEST_PARAMS_PERSONS["test_search_persons_by_id_200"]["data"],
)
async def test_search_persons_by_id_200(
        make_get_request, query, expected_answer, message
        ):
    # Request data
    body, status = await make_get_request(path=query["path"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body["full_name"] == expected_answer["full_name"], message["full_name"]


@pytest.mark.parametrize(
    TEST_PARAMS_PERSONS["test_search_persons_by_id_404"]["keys"],
    TEST_PARAMS_PERSONS["test_search_persons_by_id_404"]["data"],
)
async def test_search_persons_by_id_404(
        make_get_request, query, expected_answer, message
        ):
    # Request data
    body, status = await make_get_request(path=query["path"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body["detail"] == expected_answer["detail"], message["detail"]


@pytest.mark.parametrize(
    TEST_PARAMS_PERSONS["test_redis_in_persons"]["keys"],
    TEST_PARAMS_PERSONS["test_redis_in_persons"]["data"],
)
async def test_redis_in_persons(
        make_get_request, get_redis, query, expected_answer, message,
        ):
    # Request data
    _, _ = await make_get_request(path=query["path"], query_data=query["data"])
    # Check the response from redis
    redis_client = get_redis
    assert (
        redis_client.exists(query["key_redis"]) == expected_answer["key_redis"]
    ), message["key_redis"]


@pytest.mark.parametrize(
    TEST_PARAMS_PERSONS["test_search_films_by_persons_200"]["keys"],
    TEST_PARAMS_PERSONS["test_search_films_by_persons_200"]["data"],
)
async def test_search_films_by_persons_200(
        make_get_request, query, expected_answer, message
        ):
    # Request data
    body, status = await make_get_request(path=query["path"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert len(body["films"]) == expected_answer["length"], message["length"]


@pytest.mark.parametrize(
    TEST_PARAMS_PERSONS["test_search_films_by_persons_404"]["keys"],
    TEST_PARAMS_PERSONS["test_search_films_by_persons_404"]["data"],
)
async def test_search_films_by_persons_404(
        make_get_request, query, expected_answer, message
        ):
    # Request data
    body, status = await make_get_request(path=query["path"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body["detail"] == expected_answer["detail"], message["detail"]
