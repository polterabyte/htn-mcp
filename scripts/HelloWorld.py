import requests
import json
import uuid

# Согласно docker-compose.yml, Orchestrator доступен на порту 8080
ORCHESTRATOR_URL = "http://localhost:8080/api/v1/goals/"

def submit_hello_world_goal():
    """
    Отправляет простую "hello world" цель в Orchestrator для проверки работоспособности системы.
    """
    goal_id = str(uuid.uuid4())
    print(f"🚀 Отправка тестовой цели в Orchestrator (ID: {goal_id})...")

    # Это гипотетическая структура цели.
    # Возможно, ее нужно будет адаптировать под реальную схему API.
    goal_payload = {
        "id": goal_id,
        "name": "Simple System Check",
        "description": "Простая цель для проверки, что все сервисы запущены и взаимодействуют.",
        "context": {
            "message": "Hello, world!"
        }
    }

    try:
        response = requests.post(
            ORCHESTRATOR_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(goal_payload)
        )

        # Проверяем, что запрос был принят (например, статус 202 Accepted)
        if 200 <= response.status_code < 300:
            print("✅ Цель успешно отправлена в Orchestrator.")
            print(f"   Статус ответа: {response.status_code}")
            print("   Ответ сервера:")
            print(json.dumps(response.json(), indent=2))
            print("\n👀 Теперь можно наблюдать за обработкой цели в логах:")
            print("   make logs")
        else:
            print(f"❌ Оркестратор ответил с ошибкой (Статус: {response.status_code}).")
            print("   Ответ сервера:", response.text)

    except requests.exceptions.ConnectionError:
        print(f"❌ Не удалось подключиться к Orchestrator по адресу: {ORCHESTRATOR_URL}")
        print("   Убедитесь, что все сервисы запущены с помощью команды 'make up'.")
    except Exception as e:
        print(f"🔥 Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    submit_hello_world_goal()