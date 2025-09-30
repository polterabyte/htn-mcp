# ФАЗА6. Тестирование, наблюдаемость и эксплуатация

6.1 Тестовая пирамида - Сформируй структуру `tests/unit`, `tests/integration`, `tests/e2e`. Настрой `pytest.ini` с общими фикстурами. Подготовь mock-и для NATS и MCP. Обнови CI для поэтапного прогона.
6.2 Юнит-тесты библиотек - Покрой `libs/contracts` и `libs/htn` проверками схем и планирования. Используй `pytest.mark.parametrize` для SLA кейсов. Добавь снапшоты для HTN дерева. [пример: ```python
@pytest.mark.parametrize("status", ["draft", "in_progress", "failed"])
def test_contract_status_transitions(status):
    contract = ContractFactory.build(status=status)
    assert validate_contract(contract)
```]
6.3 Интеграционные сценарии - Создай `tests/integration/test_full_pipeline.py`. Запускай orchestrator, planner и workers в docker-compose. Используй фикстуру для очистки Redis и Postgres. Проверяй публикацию `contract.verified`.
6.4 E2E регрессия - Настрой playwright или httpx сценарии против поднятого стенда. Прогоняй последовательность целей через API. Проверяй корректность плана и артефактов в MinIO. Фиксируй скриншоты Grafana по итогам.
6.5 Наблюдаемость - Расширь `monitoring/` дашборды метриками задержек контрактов и загрузки воркеров. Обнови `otel-collector-config.yaml` для экспорта в Jaeger. Настрой алерты Prometheus по SLA. Документируй runbook реакций.
6.6 Управление логами - Сконфигурируй Loki парсеры для `apps/*`. Добавь структурированные поля contract_id, goal_id, trace_id. Обнови `apps/shared/logging.py` форматтером JSON. Настрой ретеншн и индексацию.
6.7 Эксплуатационные процедуры - Подготовь `docs/OPERATIONS.md` с шагами релиза, отката и миграций. Описывай создание тэгов и выпуск helm chart. Добавь чеклист дежурного инженера.
6.8 План расширений - Сформируй roadmap в `docs/ROADMAP.md` с квартальными целями. Оцени потребность в новых MCP инструментах. Описывай критерии приоритизации фич.
6.9 Финализация QA стратегии - Обнови `docs/QA_STRATEGY.md` сведением о покрытиях и SLA тестов. Включи матрицу рисков и ответственных. Настрой шаблон отчёта о регрессии в `docs/templates/QA_REPORT.md`.
6.10 Актуализация HelloWorld - Расширь `scripts/HelloWorld.py` сценарием end-to-end с оркестратором, планировщиком, контракт-менеджером и воркерами. Запусти `python ./scripts/HelloWorld.py` после обновления мониторинга. Сравни ожидаемый и фактический вывод, сохрани результат проверки в `docs/QA_STRATEGY.md` и приложи выдержку в docstring.
