from .emotion import emotion_bp
from .sentiment import sentiment_bp
from flask import Blueprint

def register_routes(app):
    app.register_blueprint(emotion_bp, url_prefix="/predict")
    app.register_blueprint(sentiment_bp, url_prefix="/predict")
