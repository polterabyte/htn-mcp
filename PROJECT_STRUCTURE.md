# PROJECT_STRUCTURE.md — Структура проекта (прод-уровень)

Ниже — рекомендация по структуре рабочего репозитория многоагентной системы с HTN‑планированием, ролями, контрактами и MCP‑инструментами. Структура рассчитана на **реальную реализацию**, без моков.

```
.
├── apps/
│   ├── orchestrator/                 # Внешний API/шлюз. План/инициация, публикация контрактов
│   │   ├── app/
│   │   │   ├── api/                 # FastAPI роуты: goals, plans, admin/tools
│   │   │   ├── services/            # Прикладная логика (создание плана, валидация SLA, аутентификация)
│   │   │   ├── adapters/            # Клиенты: NATS/Kafka, Redis, Postgres, S3/MinIO, Vault
│   │   │   ├── domain/              # Pydantic-схемы: Goal, SLA, Contract (shared-версия)
│   │   │   ├── config.py            # Конфиг (env + pydantic)
│   │   │   ├── main.py              # Bootstrap FastAPI
│   │   │   └── __init__.py
│   │   ├── migrations/              # Alembic миграции
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── planner/                      # HTN-планировщик и репланер
│   │   ├── app/
│   │   │   ├── engine/              # HTN ядро: методы, пред/постусловия, селектор, tabu
│   │   │   ├── methods/             # Каталог методов декомпозиции (по доменам/целям)
│   │   │   ├── policies/            # Политики ролей и стратегии выбора
│   │   │   ├── adapters/            # Подписки из шины, публикация контрактов
│   │   │   ├── domain/              # Общие типы плана/узлов, статусы
│   │   │   ├── config.py
│   │   │   └── worker.py            # entrypoint воркера-планировщика
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── contract-manager/             # ЖЦ контрактов, аллокация бюджета/дедлайнов, backpressure
│   │   ├── app/
│   │   │   ├── service.py           # Правила переходов статусов, эскалации, ретраи
│   │   │   ├── scheduler.py         # Очереди, приоритеты, квоты per-role/per-tenant
│   │   │   ├── adapters/
│   │   │   ├── domain/
│   │   │   ├── config.py
│   │   │   └── worker.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── mcp-registry/                 # Реестр MCP: discovery, схемы, health, warm-pool stdio
│   │   ├── app/
│   │   │   ├── registry.py          # CRUD серверов/версий, кеш tools.list
│   │   │   ├── health.py            # Heartbeat/healthchecks, circuit-breaker
│   │   │   ├── warm_pool.py         # Пул stdio-процессов
│   │   │   ├── adapters/
│   │   │   ├── api.py               # Админ-интерфейсы для регистрации/инспекции
│   │   │   ├── config.py
│   │   │   └── main.py              # опционально HTTP API
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── blackboard/                   # Event-sourced слой + снапшоты
│   │   ├── app/
│   │   │   ├── events.py            # Модели событий, сериализация
│   │   │   ├── snapshots.py         # Сборка снапшотов в PG (JSONB)
│   │   │   ├── api.py               # Сервис чтения/запросов с версионированием
│   │   │   ├── adapters/
│   │   │   ├── config.py
│   │   │   └── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── workers/                      # Ролевые воркеры (Executor/Analyst/Verifier/Coordinator)
│   │   ├── executor/
│   │   │   ├── app/
│   │   │   │   ├── invoker/         # Вызовы MCP (http/stdio), ретраи, таймауты, CB
│   │   │   │   ├── handlers/        # Имплементация листовых действий и glue к Blackboard
│   │   │   │   ├── adapters/
│   │   │   │   ├── config.py
│   │   │   │   └── worker.py
│   │   │   ├── Dockerfile
│   │   │   ├── requirements.txt
│   │   │   └── README.md
│   │   ├── analyst/
│   │   ├── verifier/
│   │   └── coordinator/
│   │
│   └── admin-api/                    # (Опционально) общий админ-интерфейс и UI
│
├── libs/                             # Общие библиотеки (без зависимостей от apps)
│   ├── contracts/                    # Модели контрактов, SLA, валидация (pydantic/JSON Schema)
│   ├── htn/                          # Общие структуры плана/узлов/методов
│   ├── mcp/                          # FQID, парсинг, клиенты, политики
│   ├── infra/                        # Клиенты Postgres/Redis/NATS/S3, ретраи, конфиг
│   └── utils/                        # Логи, трейсинг, метрики, хелперы
│
├── schemas/                          # Официальные JSON Schema (контракты, mcp_policy, инварианты)
├── migrations/                       # Общие SQL миграции (если не в apps/*/migrations)
├── charts/                           # Helm чарты (монорепо) — orchestrator, workers, mcp-registry, blackboard
├── deployments/                      # K8s манифесты/оверлеи (если без Helm), kustomize
├── docker/                           # Базовые Dockerfile/скрипты, entrypoints
├── scripts/                          # Служебные скрипты CI/CD, генерация схем, сидинг
├── ops/                              # Terraform/Ansible, Vault policies, сетевые политики
├── configs/                          # Конфиги по окружениям (dev/stage/prod), otel, logging
├── docs/                             # Документация (design, architecture, runbooks, SLO, threat model)
│   ├── design_doc.md
│   ├── ARCHITECTURE.md
│   ├── CONTRACTS.md
│   ├── TOOLS.md
│   ├── RUNBOOKS.md                   # Операционные инструкции и плейбуки инцидентов
│   ├── QA_STRATEGY.md                # Тест-стратегия и чек-листы
│   └── SECURITY.md                   # Модель угроз, политика секретов, аудит
│
├── tests/                            # Тесты: unit/property/contract/integration/e2e
│   ├── unit/
│   ├── property/
│   ├── contract/                     # Контрактные тесты MCP-инструментов и инвариантов
│   ├── integration/                  # NATS/Blackboard/PG связки
│   └── e2e/                          # Полные сценарии: goal → plan → execute → verify
│
├── .github/                          # CI/CD (Actions): lint/test/build/publish/deploy
│   ├── workflows/
│   └── ISSUE_TEMPLATE/
│
├── Makefile                          # Сборка, линт, тесты, локальный ап
├── docker-compose.yml                # Локальное окружение
├── pyproject.toml                    # Общие линтеры/форматтеры (ruff, black, mypy)
└── README.md
```

## Назначение и содержание ключевых папок

### apps/
Прикладные сервисы. Каждый — самостоятельный deployable. Содержит свой `Dockerfile`, `requirements.txt`, миграции и README с API/портами/переменными окружения.
- **orchestrator**: HTTP API, аутентификация (OIDC), валидация входа, запись планов/контрактов в БД, публикация событий в шину.
- **planner**: HTN-движок, методы декомпозиции, селектор по ожидаемой стоимости, репланер.
- **contract-manager**: жизненный цикл контрактов, аллокатор бюджета/дедлайнов, очереди, preemption, backpressure.
- **mcp-registry**: учёт MCP-серверов/версий, discovery (`tools.list`), кеш схем, health & warm-pool для stdio.
- **blackboard**: event-sourced слой (JetStream/Kafka) + снапшоты (Postgres JSONB), API чтения/истории.
- **workers**: реализации ролей:
  - **executor**: Invoker MCP (http/stdio), транзакционные записи в Blackboard, компенсации.
  - **analyst**: применение HTN-методов, разметка поддеревьев, подготовка контрактов.
  - **verifier**: предикаты/инварианты, аудит и отчёты.
  - **coordinator**: распределение квот, эскалации, реплан-триггеры.

### libs/
Переиспользуемые модули без внешних зависимостей от приложений. Единый источник типов/утилит: контракты, HTN, MCP‑адресация, клиенты инфраструктуры, общие ретраи/логирование/трейсинг. Пакеты версионируются и публикуются в ваш внутренний PyPI/Artifacts Registry.

### schemas/
Канонические JSON Schema для контрактов, MCP‑policy, инвариантов. Используются валидацией на входе (API) и в воркерах.

### charts/ и deployments/
Helm‑чарты или «голые» манифесты K8s для сервисов. Разделение values по окружениям (dev/stage/prod), секреты — через Vault/SealedSecrets.

### docs/
Центр знаний: дизайн‑документация, архитектура, регламенты, runbooks, модель угроз, тест‑стратегия. Описывает и обновляется вместе с кодом.

### tests/
Полный пирог тестов: от unit/property до e2e. Контрактные тесты для MCP‑инструментов гарантируют совместимость при обновлениях.

## Обязательные стандарты для всех сервисов
- **Observability**: OpenTelemetry (trace_id в логах), Prometheus‑метрики, структурные логи (JSON).
- **Безопасность**: только mTLS внутри кластера, секреты из Vault, политика минимально необходимых прав (capabilities/caps).
- **Стабильность**: circuit breaker на внешние вызовы, экспоненциальные ретраи с джиттером, таймауты по умолчанию.
- **Схемы и версии**: каждая публичная сущность версионируется (`vN`), миграции совместимы вперёд/назад, canary‑rollout + автооткат по SLO.
- **Качество**: линтеры (ruff/black), типизация (mypy/pyright), coverage thresholds, pre‑commit hooks.
- **Документация**: README в каждой папке сервиса с описанием назначения, переменных окружения и команд запуска.

## Границы и интерфейсы
- **Шина событий**: топики `contracts.*`, `plans.*`, `mcp.*`, `bb.events`. Форматы сообщений документируются в `docs/` и валидируются JSON Schema.
- **Blackboard API**: gRPC/HTTP для чтения снапшотов/истории и транзакционных записей (через воркеры).
- **MCP Registry API**: админские методы регистрации/обследования серверов; политики доступа (RBAC).

## Кто владеет чем (ownership)
- **Orchestrator & Contract‑manager** — команда Core Orchestration.
- **Planner & Analyst Worker** — команда Planning.
- **Executor & MCP Registry** — команда Execution.
- **Blackboard** — команда Data/Infra.
- **Shared libs/schemas** — архитектурный совет, через RFC‑процедуру.

---

Эта структура масштабируется: можно выделять монорепо/полирепо, добавлять новые роли/сервисы без перестройки основ. Главное — держать границы чистыми, схемы стабильными и документацию рядом с кодом.
