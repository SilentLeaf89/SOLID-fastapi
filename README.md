Продолжение работы над [API-FastAPI](https://github.com/SilentLeaf89/API-FastAPI) , начало командной работы.

Применил SOLID на cache (Redis).

Функциональные тесты на /genres.


## Как проверить?

- Проверить все ручки через Swagger: Запустите prod приложение командой `make prod`.

- Проверить все тесты `pytest`, подробнее в файле [tests/README.md](tests/README.md).

### Swagger

При запуске сервера через `make dev ` или `make prod`, swagger доступен по данному пути:

http://127.0.0.1/api/openapi

### минимальные требования для запуска проекта

- необходимо наличие утилиты make

#### установка `make` на macOS

```
brew install make
```

#### установка `make` на deb-операционные системы

```
apt install make
```

### для **dev**

- смонтирован том со снепшотом индекса elasticsearch
- есть скрипт восстановления индекса
- elasticsearch доступен на локальной машине по сокету `127.0.0.1:9200`
- redis доступен на локальной машине по сокету `127.0.0.1:6379`
- папка с исходниками смонтирована в контейнер fastapi и при изменении uvicorn перезапускает сервер
- fastapi доступен на локальной машине по сокету `127.0.0.1:80`

```
make dev
```

### восстановление индекса elasticsearch можно выполнить после запуска контейнеров командой только в **dev** режиме:

```
make restore-index
```

### для **prod**

- на локальной машине доступен только контейнер nginx по сокету `127.0.0.1:80`

```
make prod
```

### остановка всех запущенных контейнеров:

```
make stop
```

### другие команды доступные для дебага:

#### консоль redis-cli:

```
make redis-cli
```

#### консоль python в контейнере fastapi:

```
make fastapi-console
```

---

### просмотр всех логов в tail режиме (выход ctrl+c или command+c):

```
make logs
```

---

### Я не хочу использовать `make`

#### запус проекта **dev** без `make`:

```
docker-compose up -d
```

#### восстановление идекса в **dev** режиме

```
docker-compose exec elasticsearch bash -c "/usr/share/elasticsearch/restore.sh"
```

#### запуск **prod** режима проекта без `make`

```
docker-compose -f docker-compose.yml -f docker-compose.override.prod.yml up -d
```

#### остановка всех контейнеров

```
docker-compose down
```

# Проектная работа 5 спринта

В папке **tasks** ваша команда найдёт задачи, которые необходимо выполнить во втором спринте модуля "Сервис Async API".

Как и в прошлом спринте, мы оценили задачи в стори поинтах.

Вы можете разбить эти задачи на более маленькие, например, распределять между участниками команды не большие куски задания, а маленькие подзадачи. В таком случае не забудьте зафиксировать изменения в issues в репозитории.

**От каждого разработчика ожидается выполнение минимум 40% от общего числа стори поинтов в спринте.**
