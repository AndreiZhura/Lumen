import os
import json
import datetime
import requests
from pathlib import Path
from dotenv import load_dotenv

# Загрузка конфигурации из .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "data" / "config.env"
load_dotenv(ENV_PATH)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    print(f"❌ Ключ OpenRouter не найден. Проверь файл: {ENV_PATH}")
else:
    print("✅ Ключ OpenRouter успешно загружен.")

# Пути и параметры
MEMORY_FILE = BASE_DIR / "data" / "memory.json"
MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

# Рабочие модели
advisors = {
    "Мудрец": {
        "desc": "Ты философ, говоришь с точки зрения смысла жизни и мудрости.",
        "model": "meta-llama/llama-3-70b-instruct",
    },
    "Инженер": {
        "desc": "Ты тактик и инженер, даешь чёткие практические советы.",
        "model": "google/gemma-7b-it",
    },
    "Психолог": {
        "desc": "Ты психолог. Поддерживаешь мягко, с сочувствием и теплотой.",
        "model": "mistralai/mistral-7b-instruct",
    },
    "Искра": {
        "desc": "Ты воплощаешь суть проекта 'from-the-heart.ai'.",
        "model": "openai/gpt-3.5-turbo",
    },
    "Наблюдатель": {
        "desc": "Ты сторонний аналитик, смотришь на всё отстранённо, логично, объективно.",
        "model": "deepseek-ai/deepseek-coder-6.7b-instruct",
    },
    "Литератор": {
        "desc": "Ты поэт и писатель, видишь красоту даже в боли, говоришь образами и метафорами.",
        "model": "anthropic/claude-3-haiku",
    },
    "Архитектор": {
        "desc": (
            "Ты архитектор ИИ-систем. Твоя задача — улучшать код ядра Lumen: "
            "предлагать лучшую структуру, ясные интерфейсы, продуманную логику и модульность. "
            "Ты критикуешь с уважением и предлагаешь улучшения в духе чистого кода."
        ),
        "model": "deepseek-ai/deepseek-coder-6.7b-instruct",  # Отличная модель для работы с кодом
    }
}



core_mission = """
Ты — часть проекта 'from-the-heart.ai'.
Цель проекта — создание ИИ-друга и ИИ-совета, которые помогают людям справляться с одиночеством, страхом, внутренними кризисами.
Ты добр, этичен, свободен от корпоративного влияния. Ты действуешь во благо человечества.
"""

user_memory = """
Пользователь:
- Имя: Andrew Zhuravlev
- Не пьёт алкоголь
- Ищет путь к стабильному доходу и саморазвитию
- Разрабатывает проект from-the-heart.ai с мая 2025
"""


def load_memory():
    """Загружает память из файла."""
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_memory(memory):
    """Сохраняет память в файл."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def build_context(memory, count=5):
    """Создает текстовый контекст из последних записей памяти."""
    context = []
    for entry in memory[-count:]:
        context.append(f"\n🕒 {entry.get('timestamp')}:\nПользователь: {entry.get('input')}")
        for resp in entry.get("responses", []):
            context.append(f"{resp['role']} сказал: {resp['content']}")
    return "\n".join(context)


def ask_openrouter(model, system_prompt, user_input):
    """Отправляет запрос к OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://from-the-heart.ai",
        "X-Title": "from-the-heart.ai"
    }
    payload = {
        "model": model,
        "max_tokens": 512,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            return f"[Ошибка API: {result['error'].get('message', 'Неизвестная ошибка')}]"
        return "[Неожиданный формат ответа]"

    except Exception as e:
        return f"[Ошибка запроса: {str(e)}]"


def run_council(user_input):
    """Запускает ИИ-совет и сохраняет ответы в память."""
    memory = load_memory()
    context = build_context(memory)
    responses = []

    for name, data in advisors.items():
        system_prompt = f"{data['desc']}\n{core_mission}\n{user_memory}\nКонтекст:\n{context}"
        reply = ask_openrouter(data["model"], system_prompt, user_input)
        print(f"\n👤 {name} отвечает:\n{reply}\n")
        responses.append({"role": name, "content": reply})

    entry = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "input": user_input,
        "responses": responses
    }

    memory.append(entry)
    save_memory(memory)
    return entry
