from config.settings import test_settings
from functional.utils.wait_for_es import wait_for_es
from functional.utils.wait_for_redis import wait_for_redis

if __name__ == "__main__":
    wait_for_es(
        es_client_host=test_settings.ELASTIC_HOST,
        es_client_port=test_settings.ELASTIC_PORT,
    )
    wait_for_redis(redis_client_host=test_settings.REDIS_HOST)
