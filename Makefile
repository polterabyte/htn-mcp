SHELL := /bin/bash

up:
	docker compose up -d

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

seed:
	@echo "Seeding DB and S3 bucket... (implement your seed script)"

test:
	@echo "Run unit/integration tests here"

otel:
	docker compose logs -f otel-collector
