# ФАЗА3. Оркестратор и планировщик

3.1 Изучение требований - Прочитай `ARCHITECTURE.md` и `docs/RealizationPlane.md` для понимания потоков целей. Уточни формат события `plan.request`. Зафиксируй вопросы к команде и согласуй SLA для построения плана.
3.2 Pydantic-схемы целей - Создай `GoalRequest` и `GoalResponse` в `apps/orchestrator/orchestrator/api/models.py`. Добавь поля `goal_id`, `description`, `constraints`. Настрой алиасы под JSON. [пример: ```python
class GoalRequest(BaseModel):
    goal_id: UUID = Field(alias="id")
    description: str
    constraints: dict[str, Any] = Field(default_factory=dict)
```]
3.3 Валидация входа - Допиши эндпоинт `POST /api/v1/goals` в `apps/orchestrator/orchestrator/api/routes.py`. Проверяй обязательные поля и ограничения по длине. Возвращай 422 при ошибке. Пропиши unit-тесты в `tests/api/test_goals.py`.
3.4 Обогащение цели - Добавь генерацию `created_at`, `sla_seconds`, `trace_id`. Используй `uuid4()` и `datetime.utcnow()`. Приложи вычисление дедлайна `deadline = created_at + timedelta(seconds=sla_seconds)`.
3.5 Публикация события - Реализуй `publish_plan_request(goal: GoalRequest)` в `apps/orchestrator/orchestrator/services/publisher.py`. Формируй структуру `{"subject": "plan.request", "data": goal_dict}`. Используй клиент NATS из `libs/infra/events`.
3.6 Логирование и трассировка - Обнови middleware, чтобы оборачивать обработку цели в span `goal.accept`. Логируй `goal_id`, SLA и размеры payload. Включи запись в `otel` и Prometheus `Counter`.
3.7 Ответ API - Верни JSON `{ "status": "queued", "goal_id": str(goal_id) }`. Укажи HTTP 202. Сохрани цель в Postgres через репозиторий `apps/orchestrator/orchestrator/storage/goals.py`.
3.8 Планировщик подписчик - Настрой `apps/planner/planner/main.py` слушать `plan.request`. Используй асинхронного подписчика NATS. Сохраняй события в таблицу `planner_goal_events`.
3.9 Построение дерева - Создай функцию `build_plan(goal: GoalPayload, methods: list[Method])`. Расширяй корневую задачу, добавляй дочерние узлы. Обрабатывай ограничения из `constraints`. [пример: ```python
plan = Plan.from_goal(goal)
while plan.has_open_tasks():
    task = plan.next_task()
    method = heuristics.pick(task, methods)
    plan.apply(method)
```]
3.10 Сохранение состояния - После расчёта плана сохраняй `PlanSnapshot` в Postgres. Выгружай JSON-представление в таблицу `planner_plans`. Добавь индексы по `goal_id` и статусу.
3.11 Публикация результатов - Отправляй `plan.ready` с данными плана и дедлайном. Включи список задач и связанный `trace_id`. Подготовь адаптер для обратной совместимости с существующими воркерами.
3.12 Телеметрия - Добавь метрики `planner_build_duration_seconds` и `planner_failed_total`. Обнови `apps/planner/planner/telemetry.py`. Включи логи на уровни INFO и WARNING при тайм-аутах.
3.13 Обработка ошибок - Реализуй retry с экспоненциальной задержкой при недоступности NATS. Ловите `ValidationError` и публикуйте `plan.failed`. Сохраняйте причину в журнале.
3.14 Интеграционные тесты - Напиши сценарий в `tests/integration/test_goal_to_plan.py`. Используй `asyncio` и фейки NATS. Проверяй, что на `plan.request` появляется `plan.ready` и запись в БД.
3.15 Документация - Обнови `docs/ORCHESTRATOR.md` и `docs/PLANNER.md`. Описывай новые эндпоинты, формат событий и поля плана. Добавь диаграмму последовательности.
3.16 Актуализация HelloWorld - Измени `scripts/HelloWorld.py`, чтобы отправлять HTTP POST на `/api/v1/goals` и выводить ответы `plan.ready`. Обнови docstring ожидаемым выводом. Сохрани пример журнала в `docs/HelloWorldLogs/phase3.txt`.
3.17 Контрольный прогон - Выполни `python ./scripts/HelloWorld.py` после деплоя Оркестратора и Планировщика. Сравни фактический вывод с ожидаемым. Зафиксируй результат в `docs/QA_STRATEGY.md` и приложи ссылку на лог.
