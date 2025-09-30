# Verifier Worker

Verifier — воркер, отвечающий за проверку результатов по контрактам. Он
подтверждает, что deliverables удовлетворяют предикатам и инвариантам, прежде
чем контракт будет закрыт.

## Обязанности
- Подписываться на контракты `contracts.verify` и события от Executor.
- Загружать факты из Blackboard и выполнять проверки (`predicate`, `invariants`).
- Возвращать статус (`verified`/`rejected`) в Contract Manager.
- Логировать причины отказа для отладки и аудита.

## Структура
- `verifier/worker.py` — точка входа.
- `verifier/adapters/` — клиенты Blackboard, Contract Manager, Registry.
- Планируется модуль `checks/` с библиотекой инвариантов.

## Конфигурация
| Переменная | Назначение |
|------------|------------|
| `ROLE` | Значение `VERIFIER`. |
| `DATABASE_URL` | История проверок/аудит. |
| `NATS_URL` | Очереди результатов воркеров и запросы на проверку. |
| `REDIS_URL` | Кеш схем и инвариантов. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Трейсы (`verifier.check`). |

## Запуск
```bash
cd apps/workers/verifier
python -m verifier.worker
```
Требуется доступ к Blackboard и Contract Manager (поднимите `make up`).

## Метрики/наблюдаемость
- `verifier_checks_total{result}` — число проверок по статусам.
- `verifier_latency_seconds` — время проверки.
- `verifier_invariant_failed_total{invariant}` — счётчик нарушений.

## Роадмап
- Реализовать библиотеку инвариантов (например, `no_external_net`).
- Добавить поддержку JSON Schema валидации результатов.
- Прописать runbook на случай массовых отказов (`docs/RUNBOOKS.md`).
- Покрыть тестами критичные предикаты (property‑tests).
