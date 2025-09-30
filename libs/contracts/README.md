# libs/contracts

Библиотека `libs/contracts` содержит общие модели и утилиты для работы с
контрактами между агентами. Её используют оркестратор, Contract Manager,
воркеры и тесты.

## Что здесь будет
- Pydantic‑схемы для контрактов, SLA, deliverables, политик MCP (см.
  `docs/design/CONTRACTS.md`).
- Валидаторы статусов и переходов (`Proposed → ... → Settled`).
- Хелперы для генерации idempotency‑ключей и журналирования.

## Планируемый интерфейс
```python
from libs.contracts.models import Contract, SLA
from libs.contracts.validation import validate_transition
```

## Точки расширения
- Добавляйте новые инварианты/предикаты, если они общие для нескольких сервисов.
- Держите схемы синхронизированными с `schemas/contract.schema.json`.
- Публикуйте пакет во внутренний PyPI, чтобы версии были явными.

## Тесты
Планируется каталог `tests/libs/contracts`. Покрывайте:
- Валидацию схем (позитивные/негативные сценарии).
- FSM переходов статусов.
- Генерацию событий аудита.

## Связанные документы
- `docs/design/CONTRACTS.md`
- `ARCHITECTURE.md` (раздел «Contract Manager»)
