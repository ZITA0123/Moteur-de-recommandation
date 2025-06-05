import os
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

class SentimentAnalyzer:
    def __init__(self):
        self.vectorizer = CountVectorizer(max_features=5000)
        self.model = LogisticRegression(max_iter=1000)
        self.is_trained = False
        
    def preprocess_text(self, text):
        """Prétraitement basique du texte"""
        if isinstance(text, str):
            return text.lower()
        return ""
        
    def train(self, X_text, y_labels):
        """Entraîne le modèle sur les données fournies"""
        # Prétraitement
        X_processed = [self.preprocess_text(text) for text in X_text]
        
        # Vectorisation
        X_vectorized = self.vectorizer.fit_transform(X_processed)
        
        # Entraînement
        self.model.fit(X_vectorized, y_labels)
        self.is_trained = True
        
    def predict(self, texts):
        """Prédit le sentiment pour une liste de textes"""
        if not self.is_trained:
            raise ValueError("Le modèle doit d'abord être entraîné!")
            
        # Prétraitement
        texts_processed = [self.preprocess_text(text) for text in texts]
        
        # Vectorisation
        X_vectorized = self.vectorizer.transform(texts_processed)
        
        # Prédiction
        predictions = self.model.predict(X_vectorized)
        probabilities = self.model.predict_proba(X_vectorized)
        
        return predictions, probabilities
        
    def save_model(self, model_dir="model"):
        """Sauvegarde le modèle et le vectorizer"""
        if not self.is_trained:
            raise ValueError("Le modèle doit d'abord être entraîné!")
            
        os.makedirs(model_dir, exist_ok=True)
        
        with open(os.path.join(model_dir, "model.pkl"), "wb") as f:
            pickle.dump((self.model, self.vectorizer), f)
        
    def load_model(self, model_dir="model"):
        """Charge un modèle et un vectorizer sauvegardés"""
        model_path = os.path.join(model_dir, "model.pkl")
        
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                self.model, self.vectorizer = pickle.load(f)
            self.is_trained = True
        else:
            raise FileNotFoundError("Modèle non trouvé dans le dossier spécifié") 