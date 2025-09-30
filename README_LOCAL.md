# Локальный запуск и деплой

## Docker Compose
1. Установи Docker и Docker Compose.
2. В корне: `make up` — поднимет Postgres, Redis, NATS, MinIO, OTEL, и заглушки сервисов.
3. Логи: `make logs`. Остановка и очистка: `make down`.
4. Обнови образы `orchestrator` и `htn-worker` на свои.

## Helm
1. `cd helm`
2. `helm install htn .` — установит оркестратор и базовые воркеры.
3. Настрой `values.yaml` (URL'ы БД/очередей/хранилищ, образы).
4. Масштабируй воркеров через `replicaCount`.

## Схемы
В каталоге `/schemas` — JSON Schema для контрактов, MCP‑policy и инвариантов.
