build:
	docker-compose build

test:
	docker-compose -f docker-compose.yml -f docker-compose.override.prod.yml -f docker-compose.override.tests.yml up -d --force-recreate

dev: 
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d 

prod:
	docker-compose -f docker-compose.yml -f docker-compose.override.prod.yml up -d 

redis-cli:
	docker-compose exec redis redis-cli

fastapi-console:
	docker-compose exec fastapi python

restore-index:
	docker-compose exec elasticsearch bash -c "/usr/share/elasticsearch/restore.sh"


logs:
	docker-compose logs --follow

stop:
	docker-compose down

remove:
	docker-compose down --remove-orphans

