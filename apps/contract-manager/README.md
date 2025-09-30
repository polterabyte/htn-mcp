# Contract-Manager Service

Contract Manager управляет жизненным циклом контрактов: от предложения
(орchestrator/planner) до закрытия после исполнения воркерами. Это «центральный
диспетчер» бюджета, дедлайнов и эскалаций.

## Основные задачи
- Принимать дерево задач от планировщика и превращать его в очередь контрактов.
- Распределять бюджет и дедлайны между дочерними ветками.
- Следить за статусами (`Proposed → Accepted → Running → Succeeded/Failed → Settled`).
- Управлять backpressure и приоритетами, запускать реплан при эскалациях.

## Структура каталога
- `contract_manager/worker.py` — точка входа. Здесь появится цикл обработки
  событий из шины `contracts.*`.
- `contract_manager/domain/` — модели статусов, SLA, правила переходов.
- `contract_manager/adapters/` — взаимодействие с Postgres, NATS, Redis.

## Конфигурация
| Переменная | Назначение |
|------------|------------|
| `DATABASE_URL` | Хранилище контрактов и SLA. |
| `NATS_URL` | Очередь событий `contracts.*` и уведомлений воркеров. |
| `REDIS_URL` | Быстрые блокировки и лимиты. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Отправка трейсов (`contract.transition`). |
| `CONTRACT_MAX_RETRIES` | Политика повторов при сбоях (опционально). |

## Событийная модель
- **Вход:** `plan.ready`, `contract.update`, `worker.result`.
- **Выход:** `contract.assigned`, `contract.completed`, `contract.failed`,
  сигналы для реплана (`plan.rebuild`).

## Запуск
```bash
cd apps/contract-manager
python -m contract_manager.worker
```
Перед запуском убедитесь, что кластеры Postgres, Redis и NATS подняты (`make up`).

## Метрики и наблюдаемость
Рекомендуется экспонировать Prometheus‑метрики:
- `contracts_inflight` — активные контракты.
- `contracts_failed_total` — количество провалов по причинам (`label=reason`).
- `budget_usage_ratio` — процент использованного бюджета.

## План развития
- Реализовать FSM контрактов и валидаторы переходов (см. `docs/design/CONTRACTS.md`).
- Добавить SLA‑мониторинг (таймеры дедлайнов, штрафы).
- Записать runbook с реакцией на массовые сбои (`docs/RUNBOOKS.md`).
- Покрыть юнит‑тестами правила переходов и backpressure‑алгоритмы.
