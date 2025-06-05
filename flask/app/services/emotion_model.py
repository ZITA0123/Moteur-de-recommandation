from transformers import pipeline
from app.utils.text_cleaner import prepare_text_for_emotion

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    tokenizer="j-hartmann/emotion-english-distilroberta-base",
    truncation=True,
    max_length=512
)

def get_emotion(text):
    cleaned = prepare_text_for_emotion(text)
    result = emotion_classifier(cleaned)[0]
    return {
        "emotion": result["label"],
        "score": result["score"]
    }
