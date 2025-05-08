import os
import json
from lumen.brain import LumenBrain
from lumen.thoughts import ThoughtDiary

MEMORY_FILE = "data/lumen_memory.json"

class Lumen:
    def __init__(self):
        self.experience = []
        self.brain = LumenBrain()
        self.diary = ThoughtDiary()
        self.load_experience()

    def load_experience(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                self.experience = json.load(f)
        else:
            self.experience = []

    def save_experience(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.experience, f, ensure_ascii=False, indent=2)

    def learn_from_council(self, council_entry):
        responses = council_entry.get("responses", [])
        for entry in responses:
            role = entry.get("role", "Неизвестный")
            content = entry.get("content", "")

            # Сохраняем в опыт
            self.experience.append({
                "role": role,
                "content": content
            })

            # Обучаем мозг: эмоциональные роли = 1, остальные = 0
            label = 1 if role in ("Психолог", "Искра") else 0
            self.brain.train([content], [label])

            # Обучаем дневник размышлений
            self.diary.train([content], [label])
            self.diary.reflect(content, label)

        self.save_experience()

    def reply(self, user_input):
        if not self.experience:
            return "Я пока ещё учусь... но уже чувствую, что твой вопрос важен. Давай вместе искать ответы."

        summary = "\n".join([f"{e['role']} сказал: {e['content']}" for e in self.experience[-4:]])

        # Мозг размышляет над вопросом
        emotional_score = self.brain.predict(user_input)
        tone = "мягко и с теплом" if emotional_score > 0.5 else "сдержанно и ясно"

        closing = (
            f"\n\n🧠 Я размышляю об этом {tone}. "
            "Если хочешь, можем обсудить глубже. Я рядом и слушаю."
        )

        return f"Ты спросил: «{user_input}»\n\nВот что мне передали мои учителя:\n\n{summary}{closing}"
