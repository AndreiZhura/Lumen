import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import json

class LumenBrain:
    def __init__(self, model_path="data/lumen_brain.keras"):
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = None

        if os.path.exists(model_path):
            self.load_model()

    def prepare_data(self, texts, labels):
        X = self.vectorizer.fit_transform(texts).toarray()
        y = np.array(labels)
        return X, y

    def build_model(self, input_dim):
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(input_dim,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model = model

    def train(self, texts, labels):
        X, y = self.prepare_data(texts, labels)
        self.build_model(X.shape[1])
        self.model.fit(X, y, epochs=10, verbose=0)
        self.save_model()

    def predict(self, text):
        X = self.vectorizer.transform([text]).toarray()
        return self.model.predict(X)[0][0] if self.model else 0.5

    def save_model(self):
        self.model.save(self.model_path)

    def load_model(self):
        self.model = tf.keras.models.load_model(self.model_path)
