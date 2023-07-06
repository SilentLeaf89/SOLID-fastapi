import json
from elasticsearch import Elasticsearch
from redis import Redis

from tests.config.settings import test_settings
from tests.data.es_data import TEST_DATA
from tests.data.es_schemas import TEST_SCHEMAS

# Specify pytest plugins for other fixtures
pytest_plugins = ["tests.fixtures.redis",
                  "tests.fixtures.requests"]

def start_elastic_client():
    # Start the client
    es_client = Elasticsearch(
        hosts=test_settings.ELASTIC_HOST,
        validate_cert=False,
        use_ssl=False
    )
    return es_client


def empty_elastic(es_client: Elasticsearch):
    # Delete existing indices in elastic if they exist
    for index in TEST_SCHEMAS.keys():
        if es_client.indices.exists(index=index):
            es_client.indices.delete(index=index)


def create_indices_elastic(es_client: Elasticsearch):
    for index, schema in TEST_SCHEMAS.items():
        es_client.indices.create(index=index, body=schema)


def insert_data_elastic(es_client: Elasticsearch):
    for index, data in TEST_DATA.items():
        bulk_query = []
        for row in data:
            bulk_query.extend(
                [
                    json.dumps({"index": {"_index": index, "_id": row["id"]}}),
                    json.dumps(row),
                ]
            )

            str_query = "\n".join(bulk_query) + "\n"

            response = es_client.bulk(str_query, refresh=True)

            if response["errors"]:
                raise Exception(response)


def stop_elastic_client(es_client: Elasticsearch):
    es_client.close()



def start_redis():
    return Redis(
        host=test_settings.REDIS_HOST,
        port=test_settings.REDIS_PORT
        )

def pytest_configure():
    # Start elastic client
    es_client = start_elastic_client()

    # Delete existing movies index
    empty_elastic(es_client)

    # Create indices
    create_indices_elastic(es_client)

    # Insert data
    insert_data_elastic(es_client)

    # Stop elastic client
    stop_elastic_client(es_client)

    # Start redis client
    redis_client = start_redis()

    # Delete all keys in redis
    redis_client.flushall()

    # Close redis client
    redis_client.close()


def pytest_unconfigure():
    # Start elastic client
    es_client = start_elastic_client()

    # Delete existing movies index
    empty_elastic(es_client)

    # Stop elastic client
    stop_elastic_client(es_client)

    # Start redis client
    redis_client = start_redis()

    # Delete all keys in redis
    redis_client.flushall()

    # Close redis client
    redis_client.close()
