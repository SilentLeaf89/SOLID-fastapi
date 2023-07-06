settings_schema = {
    "refresh_interval": "1s",
    "analysis": {
        "filter": {
            "english_stop": {"type": "stop", "stopwords": "_english_"},
            "english_stemmer": {"type": "stemmer", "language": "english"},
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english",
            },
            "russian_stop": {"type": "stop", "stopwords": "_russian_"},
            "russian_stemmer": {"type": "stemmer", "language": "russian"},
        },
        "analyzer": {
            "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer",
                ],
            }
        },
    },
}


movies_schema = {
    "settings": settings_schema,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                    "id": {"type": "keyword"},
                },
            },
            "actors_names": {"type": "text", "analyzer": "ru_en"},
            "description": {"type": "text", "analyzer": "ru_en"},
            "directors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                    "id": {"type": "keyword"},
                },
            },
            "directors_names": {"type": "text", "analyzer": "ru_en"},
            "genre": {"type": "keyword"},
            "id": {"type": "keyword"},
            "imdb_rating": {"type": "float"},
            "title": {
                "type": "text",
                "fields": {"raw": {"type": "keyword"}},
                "analyzer": "ru_en",
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                    "id": {"type": "keyword"},
                },
            },
            "writers_names": {"type": "text", "analyzer": "ru_en"},
        },
    },
}


persons_schema = {
    "settings": settings_schema,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "full_name": {
                "type": "text",
                "fields": {"raw": {"type": "keyword"}},
                "analyzer": "ru_en",
            },
            "id": {"type": "keyword"},
        },
    },
}

genres_schema = {
    "settings": settings_schema,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "description": {"type": "text", "analyzer": "ru_en"},
            "id": {"type": "keyword"},
            "name": {
                "type": "text",
                "fields": {"raw": {"type": "keyword"}},
                "analyzer": "ru_en",
            },
        },
    },
}

TEST_SCHEMAS = {
    "movies": movies_schema,
    "persons": persons_schema,
    "genres": genres_schema,
}
