# CONTRACTS.md

**Связанные документы:** [design_doc.md](design_doc.md) • [TOOLS.md](TOOLS.md) — Шаблоны и регламент контрактов

Этот документ регламентирует **контракты** между агентами в многоагентной системе (HTN + роли) с инструментами в виде **MCP-серверов**.

## 1. Цели контрактов
- Формализовать ожидания (цели, артефакты, SLA).
- Задать ограничения доступа к контексту (Blackboard caps).
- Описать допустимые MCP-вызовы и лимиты.
- Обеспечить трассируемость и воспроизводимость.

## 2. Жизненный цикл контракта
**Proposed → Accepted → Running → Succeeded | Failed{Timeout|Budget|NoPlan|InvariantBreach|ToolError} → Settled**

- `Proposed`: сформирован родителем, ещё без ресурсов.
- `Accepted`: дочерний агент принял; ресурсы забронированы.
- `Running`: активные вызовы инструментов.
- `Succeeded`: все deliverables подтверждены верификатором.
- `Failed.*`: завершено с ошибкой; указан diagnostics.
- `Settled`: ресурсы освобождены, метрики/логи зафиксированы.

## 3. Минимальный шаблон контракта (YAML)
```yaml
contract:
  id: "uuid"
  parent_id: "uuid"
  goal:
    name: "build_report"
    params:
      date: "2025-09-29"
  role: "Executor"   # Analyst | Executor | Verifier | Coordinator
  sla:
    budget: 20.0            # условные единицы
    deadline: "2025-09-29T20:30:00Z"
    depth: 3
    helpers_max: 1
  deliverables:
    - "pdf_path"
  verify:
    predicate: "predicates.report_exists"
    invariants:
      - "invariants.no_external_net"
      - "invariants.outputs_schema_valid"
  blackboard_caps:
    read: ["raw_data", "template", "clean_data"]
    write: ["pdf_path", "logs.report"]
  mcp_policy:
    allow: ["mcp://render/pdf@^2", "mcp://db/query@>=1 <3"]
    deny: ["mcp://net/*"]
    transport: ["stdio"]
    timeouts: { connect_ms: 2000, call_ms: 15000 }
    retries: { max: 1, backoff_ms: 500 }
    concurrency: 2
  retries:
    max: 1
    backoff_ms: 300
  on_fail:
    escalate: true
    emit:
      - "diagnostics.last_error"
```

## 4. Расширенный шаблон (с частичными результатами/потоками)
```yaml
contract:
  id: "uuid"
  goal: { name: "transcribe_and_summarize", params: { audio_id: "a1" } }
  role: "Executor"
  sla: { budget: 50, deadline: "2025-09-29T21:00:00Z", depth: 4 }
  deliverables: ["transcript", "summary"]
  partials:
    min_before_deadline_ms: 10000         # требуем минимум результата заранее
    keys: ["transcript@v>=1"]
  mcp_policy:
    allow: ["mcp://asr/transcribe@^3", "mcp://nlp/summarize@^1"]
    transport: ["http"]
    timeouts: { connect_ms: 1500, call_ms: 60000 }
    retries: { max: 2, backoff_ms: 800 }
    concurrency: 1
  blackboard_caps:
    read: ["audio", "language"]
    write: ["transcript", "summary", "metrics.asr"]
  verify:
    predicate: "predicates.summary_covers_topics"
    invariants:
      - "invariants.no_pii_leak"
      - "invariants.schema_valid('transcript_schema_v2')"
      - "invariants.length_within('summary', 1200)"
```

## 5. Правила верификации
- **Predicate** — чистая функция над снимком Blackboard (scope контракта).
- **Invariants** — проверки неизменных свойств (безопасность/схема/границы). Примеры:
  - `invariants.no_external_net`: в логе MCP-вызовов отсутствуют неразрешённые сетевые хосты.
  - `invariants.outputs_schema_valid`: все записи имеют валидные JSON-схемы.
  - `invariants.no_overwrite_foreign_keys`: запись вне white-list недопустима.

## 6. Диагностика и метрики
- **Diagnostics**: последняя ошибка инструмента, состояние circuit breaker, список попыток с таймстампами.
- **Метрики контракта**: `tools_invoked`, `budget_used`, `p95_call_ms`, `replans`, `partial_progress%`.

## 7. RACI и эскалации
- **Responsible** — назначенный агент по контракту.
- **Accountable** — родительский агент.
- **Consulted** — верификатор.
- **Informed** — соседи по зависимостям/оркестратор.
- Эскалация при `Failed.Timeout | Budget | InvariantBreach` — реплан на уровень выше, перераспределение бюджета.

## 8. Политика ретраев и табу
- Ретрай инструмента допускается, если `tool.is_idempotent=true` и входы неизменны.
- Табу-лист: после `Failed.ToolError` (>=N за окно) данный инструмент/сервер исключается из выбора на T минут.

## 9. Пример статусов ошибок
- `Failed.Timeout`: превышён `sla.deadline` или `mcp_policy.timeouts.call_ms`.
- `Failed.Budget`: `budget_used > sla.budget`.
- `Failed.NoPlan`: исчерпаны методы HTN без валидного плана.
- `Failed.InvariantBreach`: нарушены инварианты/схемы/caps.
- `Failed.ToolError`: MCP вернул `internal_error`/`rate_limited` после всех ретраев.


_Подробнее про MCP‑серверы и их регистрацию см.:_ **[TOOLS.md](TOOLS.md)**.
