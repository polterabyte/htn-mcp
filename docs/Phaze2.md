# ФАЗА2. Общие библиотеки и доменные модели

2.1 Анализ требований - Изучи `docs/RealizationPlane.md` и `ARCHITECTURE.md`, чтобы понять границы ответственности библиотек. Сверь используемые термины с `schemas/contract.schema.json`. Зафиксируй выявленные артефакты в рабочем журнале. Обнови backlog задач для команды.
2.2 Аудит текущего кода - Просмотри содержимое `libs/contracts` и `libs/htn`. Выпиши существующие классы и точки расширения. Отметь устаревшие структуры для переработки. Подготовь список удаляемых зависимостей.
2.3 Подготовка схем - Синхронизируй JSON-схемы контрактов с доменными требованиями. Добавь поля SLA, дедлайнов и ссылок на родительские задачи. Проверь совместимость схемы с текущими воркерами. Задокументируй изменения в `schemas/README.md`.
2.4 Базовые модели контрактов - Создай `ContractBase` с атрибутами идентификатора, типа и параметров. Определи типы с использованием `typing.Literal` для критичных полей. Настрой автоматическое заполнение временных отметок. Добавь метод `to_event()` для публикации в NATS. [пример: ```python
class ContractBase(BaseModel):
    id: UUID
    kind: Literal["analysis", "execution", "verification"]
    payload: dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def to_event(self) -> dict[str, Any]:
        return {"subject": f"contract.{self.kind}.created", "data": self.model_dump()}
```]
2.5 SLA и дедлайны - Расширь модели полями `sla_seconds` и `deadline`. Добавь метод `is_overdue(now: datetime)` для проверки нарушений. Введи перечисление причин задержек. Обнови сериализацию в `to_event()`.
2.6 Валидация по JSON Schema - Реализуй функцию `validate_contract(contract: ContractBase)`. Подключи `jsonschema.Draft202012Validator` и кешируй схемы. Бросай `ContractValidationError` с указанием пути и причины. Обнови обработку ошибок в логике публикации. [пример: ```python
def validate_contract(contract: ContractBase) -> None:
    validator = Draft202012Validator(loaded_schema)
    errors = sorted(validator.iter_errors(contract.model_dump()), key=str)
    if errors:
        raise ContractValidationError(path="/".join(map(str, errors[0].path)), message=errors[0].message)
```]
2.7 Маппинг статусов - Определи перечисление `ContractStatus` с состояниями `pending`, `in_progress`, `done`, `failed`, `timeout`. Добавь метод `from_event(event: dict[str, Any])`. Сопоставь статусы со SLA-метками. Обеспечь обратную совместимость с существующими событиями.
2.8 Документация контрактов - Обнови `docs/CONTRACTS.md`, включив новые поля и примеры событий. Описывай каждый статус и причину эскалации. Добавь таблицу переходов. Приложи ссылку на валидационную функцию.
2.9 Ядро HTN - Создай в `libs/htn` структуры `TaskNode`, `Method` и `Plan`. Задай атрибуты приоритета, бюджета и глубины. Добавь методы `expand()` и `is_applicable(context)`. Распиши обработку ошибок планирования.
2.10 Загрузка методов - Реализуй загрузчик, который читает YAML/JSON методы из `apps/planner/planner/methods`. Кешируй результаты и слушай изменения файлов. Добавь валидацию входных данных с помощью Pydantic-моделей. [пример: ```python
def load_methods(path: Path) -> list[Method]:
    return [Method.model_validate_json(p.read_text()) for p in path.glob("*.json")]
```]
2.11 Эвристики и бюджет - Реализуй стратегию выбора метода на основе бюджета, глубины и приоритета. Добавь функцию `estimate_cost(task: TaskNode)` и обнови `Plan.schedule()`. Гарантируй, что выбор устойчив к временным ошибкам. Логируй принятые решения в стандартный логгер.
2.12 Юнит-тесты библиотек - Напиши тесты `pytest` для `libs/contracts` и `libs/htn`. Покрой сценарии успешной валидации и ошибок. Добавь тесты на реплан при превышении бюджета. Пропиши фикстуры для моков NATS. [пример: ```python
def test_validate_contract_raises_on_invalid_payload():
    contract = ContractBase(id=uuid4(), kind="analysis", payload={})
    with pytest.raises(ContractValidationError):
        validate_contract(contract)
```]
2.13 Интеграция с сервисами - Обнови `apps/planner` и `apps/contract-manager` для использования новых моделей. Проверь совместимость сериализации и событий. Настрой трансформацию старых контрактов через адаптеры. Внеси изменения в конфигурацию CI.
2.14 Документация HTN - Добавь раздел в `docs/HTN_CORE.md`, описывающий новые структуры и алгоритмы. Включи диаграмму последовательности. Дополни глоссарий терминов. Сошлись на тесты в `pytest` отчёте.
2.15 Актуализация HelloWorld - Расширь `scripts/HelloWorld.py`, чтобы отражать новые поля контрактов и базовый HTN-план. Опиши ожидаемый вывод в docstring. Сохрани изменения и обнови `docs/HelloWorldLogs/README.md`. [пример: ```python
print("HTN Plan Budget:", plan.total_budget)
```]
2.16 Контрольный прогон - Запусти `python ./scripts/HelloWorld.py` после обновления библиотек. Сравни вывод со встроенным ожиданием. Сохрани фактический лог в `docs/HelloWorldLogs/phase2.txt`. Задокументируй результат в `docs/QA_STRATEGY.md`. [пример: ```bash
python ./scripts/HelloWorld.py > docs/HelloWorldLogs/phase2.txt
```]
2.17 Итоги фазы - Обнови статус ФАЗЫ2 в `docs/RealizationPlane.md`. Сформируй pull request с ссылками на тесты и логи. Проведи ревью с командой и учти замечания. Подготовь план перехода к ФАЗЕ3.
