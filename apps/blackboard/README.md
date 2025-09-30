# Blackboard Service

Blackboard — общее хранилище фактов и артефактов, доступное всем агентам.
Сервис ведёт событийный лог (event sourcing) и собирает снапшоты состояния в
Postgres, чтобы воркеры могли читать актуальный контекст.

## Роль в архитектуре
- Агент‑исполнитель пишет результаты MCP‑вызовов.
- Аналитик и координатор читают промежуточные данные и принимают решения.
- Верификатор проверяет инварианты по снапшоту Blackboard.

## Основные компоненты
- `blackboard/main.py` — FastAPI‑обёртка (позже появятся маршруты чтения/записи).
- `blackboard/adapters/` — сюда добавляются клиенты для Postgres, NATS и S3.
- Планируется добавить модули `events.py`, `snapshots.py`, `api.py` (см.
  `PROJECT_STRUCTURE.md`).

## Планируемые API
| Метод | Описание |
|-------|----------|
| `POST /api/v1/records` | Атомарная запись фактов с idempotency‑ключом. |
| `GET /api/v1/records/{key}` | Получение версии факта (`key@version`). |
| `GET /api/v1/snapshots/{contract_id}` | Срез состояния по контракту/поддереву. |
| `GET /health` | Health‑check. |
| `GET /metrics` | Prometheus‑метрики (`bb.write_latency_ms`, `bb.conflicts_total`). |

## Конфигурация
| Переменная | Назначение |
|------------|------------|
| `DATABASE_URL` | Postgres для снапшотов (JSONB). |
| `NATS_URL` | Поток событий `bb.events`. |
| `S3_ENDPOINT` и ключи | Хранение крупных артефактов. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Отправка трейсов (`bb.write`, `bb.snapshot`). |
| `BLACKBOARD_RETENTION_DAYS` | Политика хранения событий. |

## Локальный запуск
```bash
cd apps/blackboard
uvicorn blackboard.main:app --reload --port 8082
```
Сервис ожидает, что Postgres и NATS уже доступны (`make up`).

## Наблюдаемость
- Метрики: задержка записи, число конфликтов, размер снапшотов.
- Логи: фиксируйте `contract_id`, `record_key`, `version`, `inputs_hash`.
- Трейсы: связывайте спаны с контрактом и вызовами MCP.

## Следующие шаги
- Реализовать схему событий и сериализацию (см. `docs/design/README.md`).
- Добавить идемпотентность записей по `inputs_hash`.
- Настроить компакцию событий и периодическую сборку снапшотов.
- Покрыть API тестами на гонки (`pytest` + `docker-compose` окружение).
