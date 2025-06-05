from transformers import pipeline

# Chargement du modèle fine-tuné
sentiment_classifier = pipeline(
    "text-classification",
    model="classification_model_88_percent",
    tokenizer="classification_model_88_percent",
)


def get_sentiment(text):
    prediction = sentiment_classifier(text)[0]
    label = prediction["label"]

    if label == "LABEL_1":
        sentiment = "positif"
    else :
        sentiment = "négatif"
 

    return {
        "sentiment": sentiment
    }
