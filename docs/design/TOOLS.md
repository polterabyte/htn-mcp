# TOOLS.md

**Связанные документы:** [design_doc.md](design_doc.md) • [CONTRACTS.md](CONTRACTS.md) — Регистрация и эксплуатация MCP-серверов

Этот документ описывает, как регистрировать, конфигурировать и эксплуатировать MCP‑серверы, используемые как инструменты листового уровня.

## 1. Регистрация MCP-сервера (шаблон)
```yaml
mcp_server:
  server_id: "render"
  version: "2.1.0"
  transport: "stdio"            # stdio | http
  entrypoint: ["render-server", "--stdio"]
  tools_cache_ttl_s: 300
  limits:
    concurrency: 4
    rate_limit_per_min: 240
    payload_max_kb: 5120
    call_timeout_ms: 15000
  cost_model:
    base_cost: 3.0
    size_factor: { key: "pages", slope: 0.2 }
    latency_penalty_ms: 1000
  security:
    sandbox: { kind: "container", profile: "seccomp-default" }
    network: { allowlist: [] }         # deny-by-default
    secrets: { mounts: ["VAULT://render-api-key"] }
  observability:
    logs: { level: "info", redact: ["secrets", "pii"] }
    metrics: ["p50_ms", "p95_ms", "error_rate", "concurrency_used"]
  warm_pool:
    min: 1
    max: 3
    idle_ttl_s: 120
```

## 2. Операции/инструменты (каталог)
При регистрации выполняется `tools.list`. Пример описания операции:
```yaml
tool:
  fqid: "mcp://render/pdf@2.1.0"
  name: "pdf"
  inputs_schema: "schemas/render_pdf_v2.json"
  outputs_schema: "schemas/render_pdf_out_v2.json"
  idempotent: true
  side_effects: ["disk_write"]
  default_timeouts_ms: { call: 12000 }
```

## 3. Правила совместимости и версий
- Разрешается несколько версий одного `server_id` одновременно.
- Планировщик предпочитает **совместимую по схеме** и наименьшую ожидаемую стоимость.
- Депрекейт: пометить `deprecated_since`, `sunset_at`, миграционный гайд.

## 4. Безопасность
- Сетевой доступ — только к узлам из allowlist, на уровне контейнера и сервера.
- Секреты — из секрет-хранилища, не залогировать; редактирование логов.
- Обязательно указывать `idempotent`; для `side_effects` — описать компенсирующие действия.

## 5. Наблюдаемость
- Логи: `request_id`, `contract_id`, `inputs_hash`, `duration_ms`, `status`, `payload_size`.
- Метрики: `p50/p95`, `error_rate`, `warm_pool_hits`, `timeouts`, `retries`.
- Трейсинг: спаны `mcp.connect`, `mcp.call` c link на контракт.

## 6. Health & Warm Pool
- Healthcheck: периодический `ping` или no-op с backoff.
- Warm pool: поддерживать min‑N процессов для снижения холодного старта.
- Эвиктить и перезапускать воркеры при `error_rate`/`memory_growth`.

## 7. Стоимость и планирование
Формула ожидаемой стоимости (для ранжирования):
```
expected_cost = base_cost + size_factor(key)*size + latency_penalty(latency_ms)
```
Планировщик добавляет штрафы за:
- недавние ошибки (tabu),
- высокую задержку,
- несоответствие транспорту, требуемому контрактом.

## 8. Тестирование и выпуск
- Контрактные тесты: фикстуры входов → выходы по схеме.
- Chaos-тесты: таймауты/ошибки, проверка компенсирующих действий.
- Canary rollout: 5% → 25% → 100% + автооткат по SLO.

## 9. Траблшутинг (шпаргалка)
- `Failed.Timeout`: проверь `call_timeout_ms`, нагрузку, warm pool.
- `Failed.ToolError`: посмотри `error_rate`, логи последних вызовов, включи circuit breaker.
- `Failed.InvariantBreach`: проверь схемы, caps и инварианты в контракте.
- `Failed.Budget`: пересмотри `cost_model` или снизь размер задачи.


_Шаблоны контрактов и политика вызовов MCP описаны в:_ **[CONTRACTS.md](CONTRACTS.md)**.
