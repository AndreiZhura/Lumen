import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

# Получаем API-ключи из переменных окружения
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
ANAKIN_API_KEY = os.getenv("ANAKIN_API_KEY")
BYLO_API_KEY = os.getenv("BYLO_API_KEY")

def query_model(provider, prompt):
    if provider == "together":
        return query_together(prompt)
    elif provider == "anakin":
        return query_anakin(prompt)
    elif provider == "bylo":
        return query_bylo(prompt)
    else:
        return f"[?? Неизвестный провайдер: {provider}]"

def query_together(prompt):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # пример модели
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.7
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")  # Вывод ошибки от API
    response.raise_for_status()  # Проверка на ошибки
    return response.json()["choices"][0]["text"].strip()


def query_anakin(prompt):
    url = "https://api.anakin.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {ANAKIN_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  # пример модели
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Проверка на ошибки
    return response.json()["choices"][0]["message"]["content"].strip()

def query_bylo(prompt):
    url = "https://api.bylo.ai/v1/generate"
    headers = {
        "Authorization": f"Bearer {BYLO_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 200
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Проверка на ошибки
    return response.json()["text"].strip()
