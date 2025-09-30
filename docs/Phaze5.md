# ФАЗА5. Ролевые воркеры и инструменты

5.1 Ролевой анализ - Определи обязанности Analyst, Coordinator, Executor и Verifier. Сопоставь их с типами контрактов и SLA. Зафиксируй требуемые события NATS и записи в Blackboard. Подготовь таблицу распределения ролей в `docs/WORKERS.md`.
5.2 Очереди контрактов - Настрой подписку Analyst на `contracts.analysis`. Настрой Coordinator на `contracts.coordination`. Задай префетч и auto-ack в `apps/workers/*/config.py`. Проверь идемпотентность обработчиков.
5.3 Аналитический обработчик - Реализуй функцию `handle_analysis_contract` в `apps/workers/analyst/service.py`. Добавь парсинг входных данных и вызов HTN ядра. Возвращай список подзадач для Contract Manager. [пример: ```python
def handle_analysis_contract(contract: Contract) -> list[SubTask]:
    plan = htn_builder.expand(contract.payload)
    return [SubTask.from_node(node) for node in plan.children]
```]
5.4 Координация команд - Добавь в `apps/workers/coordinator/service.py` обработку зависимостей. Распределяй дочерние контракты по ролям и проверяй бюджет ветки. Публикуй событие `contract.assigned` для каждого исполнителя. Логируй trace_id и версию плана.
5.5 Инструменты исполнителя - Подключи MCP Registry в `apps/workers/executor/tools.py`. Реализуй адаптер для HTTP и STDIO инструментов. Кэшируй схемы ввода, проверяй соответствие контракту. [пример: ```python
client = registry.get_client(tool_name)
result = client.invoke(payload)
contract_manager.report_step(contract.id, result)
```]
5.6 Проверка результатов - Создай в `apps/workers/verifier/validator.py` функции `validate_artifact` и `validate_metrics`. Используй JSON Schema и пользовательские чекеры. Публикуй `contract.verified` либо `contract.failed`. Фиксируй причину отказа.
5.7 Работа с Blackboard - Определи слой `blackboard_client` в `libs/infra/blackboard.py`. Добавь методы `append_fact`, `get_state` и `lock_section`. Гарантируй атомарность через Redis. Документируй формат записей.
5.8 Реестр инструментов - Оформи YAML `configs/tools.yaml` с описанием MCP серверов. Обнови `apps/mcp-http` для отдачи `/tools/catalog`. Реализуй в воркерах загрузку каталога при старте. Обнови README для интеграции новых инструментов.
5.9 Телеметрия воркеров - Расширь `apps/workers/*/telemetry.py` метриками `worker_contracts_total` и `worker_errors_total`. Добавь OTEL спаны `worker.process`. Включи логи с полями contract_id, role и tool. Настрой предупреждения Grafana.
5.10 Интеграционные тесты - Напиши `tests/integration/test_worker_pipeline.py`. Смоделируй полный поток от Analyst до Verifier. Используй фиктивные MCP серверы и Blackboard. Проверяй публикацию событий и записи контрактов.
5.11 Документация и обучение - Обнови `docs/WORKERS.md` и `docs/MCP_INTEGRATION.md`. Добавь последовательности действий для каждой роли. Включи схемы потоков событий. Создай обучающий пример с тестовым контрактом.
5.12 Актуализация HelloWorld - Дополни `scripts/HelloWorld.py` сценарием с Analyst, Executor и Verifier. Запусти `python ./scripts/HelloWorld.py` после сборки контейнеров. Сравни ожидаемый и фактический вывод, приложи выдержку в docstring. Зафиксируй результат проверки в `docs/QA_STRATEGY.md`.
