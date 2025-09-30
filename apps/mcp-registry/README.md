# MCP Registry Service

MCP Registry — сервис, который хранит информацию о доступных MCP‑серверах и
их инструментах. Он отвечает за discovery, health‑чеки и управление warm‑pool
процессов `stdio`‑транспорта.

## Назначение
- Регистрировать MCP‑серверы (`server_id`, `version`, транспорт, ограничения).
- Кешировать результат `tools.list` и схемы входов/выходов.
- Следить за здоровьем серверов и открывать/закрывать circuit breaker.
- Управлять пулом прогретых stdio‑процессов (минимизировать холодный старт).

## Структура кода
- `mcp_registry/main.py` — FastAPI + метрики Prometheus (gauges warm‑pool).
- `mcp_registry/warm_pool.py` — заглушка для менеджера пулов.
- `mcp_registry/adapters/` — клиенты для Postgres/Redis/NATS (пока пустые).

## API/интерфейсы (планируемые)
| Метод | Описание |
|-------|----------|
| `POST /api/v1/servers` | Зарегистрировать новый MCP‑сервер. |
| `GET /api/v1/servers` | Список серверов и их версий. |
| `GET /api/v1/servers/{id}/tools` | Список инструментов и JSON‑схем. |
| `POST /api/v1/servers/{id}/health` | Обновить heartbeat/health‑статус. |
| `GET /metrics` | Prometheus‑метрики (`mcp_stdio_pool_*`, `mcp_registry_circuit_open`). |

## Конфигурация
| Переменная | Назначение |
|------------|------------|
| `DATABASE_URL` | Реестр серверов и схем (Postgres). |
| `REDIS_URL` | Быстрый кеш схем и warm‑pool статус. |
| `NATS_URL` | События о регистрации/состоянии (`mcp.registry.*`). |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Отправка трейсов (`mcp.registry`). |
| `MCP_WARM_POOL_MIN`, `MCP_WARM_POOL_MAX` | Границы для stdio‑пула. |

## Локальный запуск
```bash
cd apps/mcp-registry
uvicorn mcp_registry.main:app --reload --port 8081
```
Локальные переменные окружения можно взять из `docker-compose.yml`.

## Метрики
В `main.py` уже объявлены gauges:
- `mcp_stdio_pool_size{server}` — размер пула.
- `mcp_stdio_pool_busy{server}` — занятые воркеры.
- `mcp_stdio_spawns_total{server}` — количество запусков stdio‑процессов.
- `mcp_registry_circuit_open{server}` — состояние circuit breaker.

## TODO
- Добавить хранилище (Postgres) и CRUD для серверов/инструментов.
- Реализовать health‑пинги и автоматическое закрытие circuit breaker.
- Написать документацию по формату регистрации (`docs/design/TOOLS.md`).
