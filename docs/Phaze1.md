# ФАЗА1. Старт и инфраструктура

1.1 Проверка инструментов - Установи Docker Desktop и Docker Compose плагин. Убедись, что Python 3.11+ и Make доступны в терминале. Запусти `docker --version` и `python --version`, чтобы проверить установку.
1.2 Клонирование репозитория - Склонируй проект `htn-mcp` из корпоративного Git. Перейди в папку `htn-mcp` перед следующими шагами. Настрой upstream, если планируешь пушить изменения.
1.3 Настройка конфигурации - Создай файл `.env` на основе `README_LOCAL.md`. Заполни переменные для Postgres, Redis, MinIO, NATS. Проверь, что секреты сохранены локально, а не в Git. [пример: ```bash
cp .env.example .env
```]
1.4 Подготовка docker-compose - Просмотри `docker-compose.yml`, чтобы понять сервисы. Убедись, что порты 8080, 9090, 3000, 3100, 8222, 9001 свободны. Добавь при необходимости override файл для локальных путей. [пример: ```yaml
# docker-compose.override.yml
services:
  orchestrator:
    environment:
      - LOG_LEVEL=debug
```]
1.5 Старт инфраструктуры - Выполни `make up`, чтобы поднять стек. Дождись статуса `healthy` для Postgres, Redis, MinIO и NATS. Проверь логи `docker compose ps` и `docker compose logs -f orchestrator`.
1.6 Первичная диагностика - Подключись к Postgres через `psql` и выполни `\l`, чтобы увидеть базы. Проверь доступ к MinIO через http://localhost:9001. Убедись, что NATS отвечает по `docker compose exec nats-server nats-server --version`.
1.7 Черновик CI/CD - Создай GitHub Actions workflow `.github/workflows/ci.yml` с линтами и тестами. Добавь шаги для `pytest`, `ruff` или `flake8`, а также артефакты логов. Сохрани временную матрицу только для основного Python.
1.8 Документация QA - Обнови `docs/QA_STRATEGY.md`, описав локальный запуск `make up`, `pytest`, сбор артефактов. Добавь раздел по перезапуску контейнеров и очистке данных. Подготовь ссылку на CI.
1.9 Актуализация HelloWorld - Открой `scripts/HelloWorld.py` и добавь отражение новых сервисов инфраструктуры. Обнови текст ожиданий внутри скрипта. Сохрани изменения в Git и задокументируй причину.
1.10 Контрольный прогон - Запусти `python ./scripts/HelloWorld.py` после старта сервисов. Сохрани фактический вывод в `docs/HelloWorldLogs/phase1.txt`. Сравни с ожидаемым выводом внутри скрипта и зафиксируй совпадение в `docs/QA_STRATEGY.md`. [пример: ```bash
python ./scripts/HelloWorld.py > docs/HelloWorldLogs/phase1.txt
```]
1.11 Итоги фазы - Сформируй отчёт о выполнении задач ФАЗЫ1 в `docs/RealizationPlane.md`. Обнови чек-лист и статусы. Подготовь pull request с ссылками на логи и CI.
