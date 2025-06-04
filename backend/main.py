from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()

# Autoriser le frontend à accéder au backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/recommend")
def recommend(mood: str):
    # Simulation de films en fonction d'une humeur
    return [
        {"title": "Inception", "imdb_score": 8.8},
        {"title": "Inside Out", "imdb_score": 8.1}
    ]

class Review(BaseModel):
    review: str

@app.post("/analyze-review")
def analyze_review(data: Review):
    # Simulation de sentiment + recommandations
    return {
        "sentiment": "Positif (82%)",
        "recommended": [
            {"title": "The Pursuit of Happyness"},
            {"title": "La La Land"}
        ]
    }
