from flask import Blueprint, request, jsonify
from app.services.sentiment_model import get_sentiment
from app.utils.text_cleaner import clean_text

sentiment_bp = Blueprint("sentiment", __name__)

@sentiment_bp.route("/sentiment", methods=["POST"])
def sentiment():
    data = request.get_json()
    text = data.get("text", "")
    prediction = get_sentiment(text)
    return jsonify(prediction)
