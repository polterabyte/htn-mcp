# Executor Worker

Executor — воркер, который исполняет листовые задачи, вызывая MCP‑инструменты и
записывая результаты в Blackboard. Он работает по контрактам роли `Executor`
и соблюдает политики безопасности (caps, мандаты MCP).

## Ключевые обязанности
- Получать контракты из шины `contracts.execute`.
- Запускать нужные MCP‑инструменты (HTTP или STDIO) с учётом ограничений.
- Публиковать промежуточные статусы и финальные результаты.
- Отправлять метрики о вызовах, ошибках и задержках.

## Навигация по коду
- `executor/worker.py` — точка входа. Уже поднимает Prometheus‑эндпоинт на 9100.
- `executor/mcp_invoker.py` — базовый инвокер MCP (HTTP/STDIO, circuit breaker).
- `executor/handlers/` — место для обработчиков конкретных контрактов (пока пусто).
- `executor/adapters/` — будущие клиенты Blackboard, Registry и Contract Manager.

## Конфигурация
| Переменная | Назначение |
|------------|------------|
| `ROLE` | Должно быть `EXECUTOR` (используется логированием/метриками). |
| `DATABASE_URL` | Чтение контрактов/истории (опционально). |
| `REDIS_URL` | Кеширование статуса MCP, локи. |
| `NATS_URL` | Подписка на контракты и публикация результатов. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Отправка трейсов вызовов MCP. |
| `MCP_HTTP_MAP`, `MCP_STDIO_MAP` | Конфигурация доступных серверов (JSON/ENV). |

## Запуск
```bash
cd apps/workers/executor
python -m executor.worker
```
Для работы требуется запущенный MCP‑сервер (см. `apps/mcp-http`) и инфраструктура
из `docker-compose.yml` (`make up`).

## Метрики и логи
- `mcp_calls_total{server,tool,status}` — количество вызовов по статусам.
- `mcp_call_duration_seconds{server,tool}` — гистограмма задержек.
- `mcp_call_retries_total` / `mcp_circuit_open` / `mcp_circuit_trips_total` —
  состояние circuit breaker.
- Логи должны содержать `contract_id`, `tool_fqid`, `inputs_hash`.

## Рекомендации по развитию
- Добавить запись результатов в Blackboard и подтверждение Contract Manager'у.
- Реализовать поддержку partial outputs и сохранение артефактов в S3.
- Интегрировать политику ограничений (`mcp_policy` из контрактов).
- Покрыть `mcp_invoker` тестами (моки HTTP и STDIO). Используйте `pytest`.
