import backoff
from elasticsearch import Elasticsearch
from elasticsearch import ConnectionError

from config.logger import get_logger

logger = get_logger(__name__)


@backoff.on_exception(backoff.expo, ConnectionError, logger=logger)
def wait_for_es(es_client_host, es_client_port):
    es_client_host = ":".join([es_client_host, str(es_client_port)])
    es_client = Elasticsearch(hosts=es_client_host, validate_cert=False, use_ssl=False)

    if es_client.info():
        logger.debug("Connection to ElasticSearch is successful!")
