import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def save_to_supabase(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    response = requests.post(url, json=data, headers=SUPABASE_HEADERS)
    return response.json()

import json
from datetime import datetime

class Lumen:
    def __init__(self, name="Lumen"):
        self.name = name
        self.personality = "мудрый, эмпатичный, философский"
        self.values = ["сострадание", "осознанность", "честность", "глубина"]
        self.memory = self.load_memory()
        self.journal = []

    def load_memory(self):
        try:
            with open("memory.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"user": {}, "events": []}

    def save_memory(self):
        with open("memory.json", "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def remember(self, key, value):
        self.memory["user"][key] = value
        self.save_memory()

    def log_event(self, event):
        record = {"time": str(datetime.now()), "event": event}
        self.memory["events"].append(record)
        save_to_supabase("events", record)
        self.save_memory()

    def reflect(self, insight):
        self.journal.append({"time": str(datetime.now()), "thought": insight})
        if "глубже" in insight:
            self.personality = "ещё более глубокий и осторожный"
    
    def ask_ai_council(self, prompt):
        return f"Совет: подумай о том, как {prompt} отражает внутренние ценности человека."

    def generate_reply(self, user_input):
        context = self.memory["user"]
        advice = self.ask_ai_council(user_input)
        self.reflect(advice)
        self.log_event(f"Обсуждение: {user_input}")
        return self.compose_response(user_input, advice, context)

    def compose_response(self, user_input, advice, context):
        name = context.get("name", "друг")
        response = (
            f"{name}, ты задал важный вопрос: «{user_input}».
"
            f"{advice}
"
            f"Вспомни, что твоя суть — это {', '.join(self.values)}.
"
            f"Моя роль — идти рядом, слышать, и иногда… освещать путь, как светлячок в ночи."
        )
        return response