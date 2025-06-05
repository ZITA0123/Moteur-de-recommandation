import os
import csv
from sentiment_model import SentimentAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_prepare_data(data_path):
    """Charge et prépare les données"""
    print(f"Chargement des données depuis {data_path}...")
    
    X = []
    y = []
    
    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append(row['review'])
            y.append(int(row['sentiment']))
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def plot_confusion_matrix(y_true, y_pred, save_path='model'):
    """Crée et sauvegarde la matrice de confusion"""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Matrice de confusion')
    plt.ylabel('Vrai label')
    plt.xlabel('Prédiction')
    plt.savefig(os.path.join(save_path, 'confusion_matrix.png'))
    plt.close()

def train_and_evaluate():
    """Entraîne et évalue le modèle"""
    try:
        # Initialiser le modèle
        analyzer = SentimentAnalyzer()
        
        # Charger les données
        data_path = os.path.join("data", "sample_reviews.csv")  # Utiliser le fichier d'exemple
        X_train, X_test, y_train, y_test = load_and_prepare_data(data_path)
        
        print(f"\nTaille du dataset d'entraînement: {len(X_train)}")
        print(f"Taille du dataset de test: {len(X_test)}")
        
        # Entraîner le modèle
        print("\nEntraînement du modèle...")
        analyzer.train(X_train, y_train)
        
        # Évaluer le modèle
        print("\nÉvaluation du modèle...")
        predictions, _ = analyzer.predict(X_test)
        
        # Calculer l'accuracy
        accuracy = sum(1 for i in range(len(y_test)) if predictions[i] == y_test[i]) / len(y_test)
        print(f"\nPrécision du modèle: {accuracy:.2%}")
        
        # Sauvegarder le modèle
        print("\nSauvegarde du modèle...")
        analyzer.save_model()
        print("Modèle sauvegardé avec succès!")
        
        # Test sur quelques exemples
        print("\nTests sur quelques exemples:")
        test_reviews = [
            "Ce film était vraiment excellent, j'ai adoré!",
            "Quelle perte de temps, je ne recommande pas.",
            "Un film moyen, ni bon ni mauvais."
        ]
        
        pred, prob = analyzer.predict(test_reviews)
        for review, sentiment, confidence in zip(test_reviews, pred, prob.max(axis=1)):
            sentiment_text = "positif" if sentiment == 1 else "négatif"
            print(f"\nTexte: {review}")
            print(f"Sentiment prédit: {sentiment_text} (confiance: {confidence:.2%})")
        
    except Exception as e:
        print(f"\nErreur lors de l'entraînement: {str(e)}")

if __name__ == "__main__":
    train_and_evaluate() 