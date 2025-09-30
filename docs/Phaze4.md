# ФАЗА4. Управление контрактами

4.1 Анализ текущей модели - Изучи `libs/contracts` и схемы `schemas/contract.schema.json`. Зафиксируй все статусы, причины отказов и поля SLA. Оцени текущие переходы и отсутствие таймеров. Подготовь список пробелов для согласования.
4.2 Проектирование FSM - Определи таблицу переходов статусов и событий. Согласуй допустимые действия для каждого исполнителя. Определи таймеры ожидания и лимиты бюджета. Задокументируй диаграмму состояний в `docs/CONTRACT_FSM.md`.
4.3 Бэкенд FSM - Реализуй класс `ContractStateMachine` в `apps/contract-manager/contract_manager/domain/fsm.py`. Определи методы `apply(event, contract)` и проверки условий. Используй Enum-статусы и исключения `InvalidTransition`. [пример: ```python
class ContractStateMachine:
    def apply(self, event: ContractEvent, contract: Contract) -> Contract:
        handler = self._handlers[(contract.status, event.type)]
        return handler(contract, event)
```]
4.4 Таймеры дедлайнов - Добавь обработку `sla_deadline` и `budget_expiration`. Используй `asyncio.create_task` для отслеживания. При превышении публикуй `contract.timeout`. Сохраняй отметку в БД с точным временем.
4.5 Расчёт бюджетов - Внедри сервис `BudgetChecker` в `apps/contract-manager/contract_manager/services/budget.py`. Сравни фактические траты со значением `contract.budget`. Поддержи конфиг `MAX_BUDGET_OVERHEAD`. При нарушении инициируй событие `contract.budget_exceeded`.
4.6 Блокировки Redis - Используй `libs/infra/locks` для эксклюзивных операций. Оборачивай критические участки `async with redis_lock("contract:{id}")`. Настрой TTL и повторные попытки. Добавь метрики использования.
4.7 События контракта - Определи структуру событий `contract.created`, `contract.started`, `contract.completed`, `contract.failed`. Расположи сериализаторы в `apps/contract-manager/contract_manager/events.py`. Обеспечь совместимость с существующими воркерами.
4.8 Интеграция с Orchestrator - Добавь подписку на `plan.ready` и создание корневых контрактов. Пропиши преобразование плановых узлов в контракты. Обнови API для запроса статуса контракта. Убедись в идемпотентности повторных событий.
4.9 Обработка ошибок - Реализуй повторное применение событий при сбоях NATS. Добавь DLQ через `contract.deadletter`. Логируй stacktrace и trace_id. Настрой алерты Prometheus по числу повторов.
4.10 Репланирование - Создай обработчик `handle_timeout` в `apps/contract-manager/contract_manager/handlers/replan.py`. При `contract.timeout` публикуй `plan.rebuild` с контекстом узла. Документируй стратегию в `docs/REPLAN.md`.
4.11 Эскалации - Реализуй переходы в статус `escalated` при превышении SLA. Уведомляй координатора через `contract.escalated`. Записывай причину и ссылку на исходное событие. Создай шаблон уведомления в `docs/templates/escalation.md`.
4.12 Второй подрядчик - Настрой стратегию выбора резервного воркера. Добавь таблицу `contract_substitutions` в Postgres. Реализуй сервис `assign_backup_worker`. Обеспечь проверку занятости и бюджета.
4.13 Журналирование - Включи структурированные логи в `apps/contract-manager/contract_manager/logging.py`. Фиксируй статус, событие, исполнителя и trace_id. Настрой вывод в Loki через стандартный формат JSONL.
4.14 Метрики и трассы - Расширь `apps/contract-manager/contract_manager/telemetry.py` счетчиками `contract_transitions_total`, `contract_timeout_total`. Добавь OTEL-span `contract.process`. Экспортируй метрики в Prometheus.
4.15 Интеграционные тесты - Разработай `tests/integration/test_contract_fsm.py`. Проверь корректность переходов, блокировок и повторного назначения. Используй фейковый Redis и NATS. Валидируй публикацию `plan.rebuild`.
4.16 Документация - Обнови `docs/CONTRACT_MANAGER.md` описанием FSM, таймеров и эскалаций. Включи таблицу переходов и пример контракта. Опиши процесс резервного назначения.
4.17 Актуализация HelloWorld - Допиши `scripts/HelloWorld.py`, чтобы выводить создание контракта, переходы статусов и реплан. Добавь ожидаемый вывод и фактический лог в docstring. Запусти `python ./scripts/HelloWorld.py`, сравни результаты и задокументируй совпадение в `docs/QA_STRATEGY.md`.

