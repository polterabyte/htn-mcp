# libs/mcp

`libs/mcp` объединяет общие структуры и клиенты для работы с MCP‑сервером.
Библиотека нужна и оркестратору, и Executor, и Registry.

## Основные компоненты (план)
- Парсер FQID (`mcp://server/tool@version`).
- Клиенты для HTTP/STDIO транспорта с единым интерфейсом.
- Политики таймаутов, ретраев и circuit breaker.
- Типы и схемы для `tools.list`, `call` и health‑эндпоинтов.

## Пример использования
```python
from libs.mcp.fqid import parse_fqid
from libs.mcp.client import MCPClient
```

## Расширение
- Добавляйте адаптеры для новых транспортов (gRPC и т. п.).
- Храните cost‑модели инструментов здесь, чтобы Planner и Executor
  использовали одну реализацию.
- Интегрируйте экспорт метрик (`mcp_calls_total`, `mcp_latency_seconds`).

## Тестирование
Рекомендуется покрывать интеграционными тестами с моковым MCP‑сервером
(`apps/mcp-http`). Используйте фикстуры для HTTP и STDIO сценариев.

## Документация
- `docs/design/TOOLS.md`
- `ARCHITECTURE.md` (раздел «MCP Registry & Invoker»)
