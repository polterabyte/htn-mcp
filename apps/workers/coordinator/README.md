# Coordinator Worker

Coordinator — воркер, который управляет распределением ресурсов между
поддеревьями, реагирует на эскалации и триггерит реплан. Он тесно взаимодействует
с Contract Manager и Planner.

## Функции
- Следить за очередями контрактов и уровнем backpressure.
- Перераспределять бюджет/дедлайны между дочерними ветками.
- Инициировать реплан (`plan.rebuild`) при серьёзных сбоях.
- Собирать агрегированные метрики по прогрессу плана.

## Структура каталога
- `coordinator/worker.py` — точка входа (цикл обработки событий/таймеров).
- `coordinator/adapters/` — сюда добавляются клиенты Contract Manager, Planner,
  Prometheus, Blackboard.

## Конфигурация
| Переменная | Назначение |
|------------|------------|
| `ROLE` | Значение `COORDINATOR`. |
| `NATS_URL` | Очереди `contracts.*`, `plan.*`, `alerts.*`. |
| `REDIS_URL` | Кеш для распределения бюджета и локов. |
| `DATABASE_URL` | Хранилище агрегатов (опционально). |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Трейсы (`coordinator.replan`). |

## Запуск
```bash
cd apps/workers/coordinator
python -m coordinator.worker
```
Перед запуском поднимите инфраструктуру (`make up`).

## Метрики/наблюдаемость
- `coordinator_backpressure_level` — текущий уровень нагрузки.
- `coordinator_replans_total` — количество репланов по причинам.
- `coordinator_budget_slack_ms` — запас по дедлайнам.
Логи должны содержать `goal_id`, `contract_id`, `reason`.

## Дальнейшие шаги
- Реализовать подписку на события Contract Manager (`contract.failed`).
- Добавить алгоритмы backpressure (например, token bucket по ролям).
- Интегрировать уведомления (PagerDuty/Slack) для критических эскалаций.
- Покрыть тестами перераспределение бюджета и дедлайнов.
