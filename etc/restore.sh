#!/bin/bash

INDEX_NAME="movies"
ELASTIC_NAME="elasticsearch"
ELASTIC_PORT=9200

# Проверяем доступность Elasticsearch
until curl -s -XGET "http://$ELASTIC_NAME:$ELASTIC_PORT" > /dev/null; do
  sleep 5
done

response=$(curl -s -o /dev/null -w "%{http_code}" http://$ELASTIC_NAME:$ELASTIC_PORT/$INDEX_NAME)

# Проверяем наличие индекса
if [[ $response -eq 404 ]]; then
  # Восстанавливаем индекс из снимка
  /usr/bin/curl -XPUT http://$ELASTIC_NAME:$ELASTIC_PORT/_snapshot/backup -H 'Content-Type: application/json' -d '{"type": "fs", "settings":{"location": "/usr/share/elasticsearch/snapshot/"}}'
  /usr/bin/curl -XPOST http://$ELASTIC_NAME:$ELASTIC_PORT/_snapshot/backup/snapshot_1/_restore\?wait_for_completion\=true
fi
