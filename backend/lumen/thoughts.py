import os
import json
import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow as tf

THOUGHTS_FILE = "data/thoughts.json"

class ThoughtDiary:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = None
        self.thoughts = []
        self.load_thoughts()

    def load_thoughts(self):
        if os.path.exists(THOUGHTS_FILE):
            with open(THOUGHTS_FILE, "r", encoding="utf-8") as f:
                self.thoughts = json.load(f)
        else:
            self.thoughts = []

    def save_thoughts(self):
        os.makedirs(os.path.dirname(THOUGHTS_FILE), exist_ok=True)
        with open(THOUGHTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.thoughts, f, ensure_ascii=False, indent=2)

    def build_model(self, input_dim):
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(input_dim,)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy')
        self.model = model

    def train(self, texts, sentiments):
        X = self.vectorizer.fit_transform(texts).toarray()
        y = np.array(sentiments)
        self.build_model(X.shape[1])
        self.model.fit(X, y, epochs=5, verbose=0)

    def reflect(self, input_text, sentiment=1):
        vector = self.vectorizer.transform([input_text]).toarray()
        prediction = self.model.predict(vector)[0][0]
        label = "вдохновение" if prediction > 0.6 else "сомнение" if prediction < 0.4 else "нейтральность"

        thought = {
            "timestamp": datetime.datetime.now().isoformat(),
            "trigger": input_text[:60] + "...",
            "emotion": label,
            "reflection": f"Я почувствовал {label}. Надо быть {('теплее' if label == 'сомнение' else 'внимательным')}."
        }

        self.thoughts.append(thought)
        self.save_thoughts()
        return thought
