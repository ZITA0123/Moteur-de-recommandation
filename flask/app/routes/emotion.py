from flask import Blueprint, request, jsonify
from app.services.emotion_model import get_emotion
from app.utils.text_cleaner import prepare_text_for_emotion

emotion_bp = Blueprint("emotion", __name__)

@emotion_bp.route("/emotion", methods=["POST"])
def emotion():
    data = request.get_json()
    text = data.get("text", "")
    prediction = get_emotion(text)
    return jsonify(prediction)
