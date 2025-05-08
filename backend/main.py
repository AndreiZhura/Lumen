import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные окружения
load_dotenv(dotenv_path="data/.env")

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MEMORY_FILE = "lumen_memory.json"

# Загрузка памяти
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"history": [], "lessons": []}

# Сохранение памяти
def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# Построение контекста с системным сообщением
def build_context_prompt(memory, max_turns=4):
    system_prompt = (
        "Ты — Lumen, философский и доброжелательный ИИ-друг. "
        "Ты говоришь с теплом, глубиной и метафорами, словно мудрый собеседник. "
        "Ты стараешься понять человека и помочь ему обрести ясность и покой. "
        "Обращайся к собеседнику как к другу."
    )
    context = memory.get("history", [])[-max_turns * 2:]
    context_text = "\n".join([
        f"{m.get('role', 'unknown')}: {m.get('content', '')}"
        for m in context if isinstance(m, dict)
    ])
    return f"{system_prompt}\n{context_text}"


# Запрос к Together API
def query_together(prompt):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.7
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["text"].strip()

# Общение с Lumen
def talk_to_lumen(user_input):
    memory = load_memory()
    memory["history"].append({"role": "user", "content": user_input})

    prompt = build_context_prompt(memory) + f"\nuser: {user_input}\nlumen:"
    response_text = query_together(prompt)

    memory["history"].append({"role": "lumen", "content": response_text})
    save_memory(memory)

    print(f"\nLumen: {response_text}\n")

# Нормализация текста
def normalize(text):
    return text.lower().strip().replace(".", "").replace(",", "")

# Обучение Lumen уроку от ИИ
def teach_lumen(lesson):
    memory = load_memory()

    if "lessons" not in memory:
        memory["lessons"] = []

    new_text = normalize(lesson["text"])
    existing_texts = {normalize(l["text"]) for l in memory["lessons"]}

    if new_text in existing_texts:
        print("[Обучение] Урок уже был записан ранее. Пропускаем.")
        return False

    lesson_entry = {
        "text": lesson["text"],
        "tags": lesson.get("tags", []),
        "source": lesson.get("source", "unknown"),
        "reason": lesson.get("reason", "Не указано"),
        "timestamp": datetime.now().isoformat()
    }

    memory["lessons"].append(lesson_entry)
    save_memory(memory)

    print(f"[Обучение] Lumen получил урок: {lesson['text']}\n[Метки]: {lesson.get('tags', [])}")
    return True

# Точка входа для ручного запуска
if __name__ == "__main__":
    print("💡 Lumen готов. Напиши что-нибудь:")
    while True:
        try:
            user_input = input("Ты: ")
            if user_input.lower() in ["exit", "выход", "quit"]:
                print("👋 До встречи!")
                break
            talk_to_lumen(user_input)
        except KeyboardInterrupt:
            print("\n👋 Прервано пользователем.")
            break
