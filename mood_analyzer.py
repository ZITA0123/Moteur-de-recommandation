import string

class MoodAnalyzer:
    def __init__(self):
        # Liste des mots vides en français
        self.stop_words = set([
            'le', 'la', 'les', 'un', 'une', 'des', 'ce', 'ces', 'sa', 'ses',
            'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
            'et', 'ou', 'mais', 'donc', 'car', 'si',
            'dans', 'sur', 'sous', 'avec', 'sans', 'pour',
            'de', 'du', 'des', 'au', 'aux',
            'être', 'avoir', 'faire',
            'suis', 'es', 'est', 'sommes', 'êtes', 'sont',
            'ai', 'as', 'a', 'avons', 'avez', 'ont'
        ])

        self.mood_categories = {
            'Happy': {
                'keywords': ['heureux', 'content', 'joyeux', 'ravi', 'excité', 'enthousiaste', 'optimiste',
                           'bien', 'super', 'génial', 'formidable', 'excellent', 'positif', 'motivé',
                           'sourire', 'rire', 'amusé', 'enchanté', 'plaisir', 'joie'],
                'genres': ['Comédie', 'Animation', 'Aventure', 'Musical'],
                'min_rating': 7.0,
                'description': "Des films joyeux et inspirants pour maintenir votre bonne humeur!"
            },
            'Sad': {
                'keywords': ['triste', 'déprimé', 'mélancolique', 'nostalgique', 'malheureux', 'seul',
                           'déprime', 'mal', 'peine', 'souffre', 'douleur', 'chagrin', 'perdu',
                           'désespéré', 'abattu', 'découragé', 'sombre', 'vide'],
                'genres': ['Drame', 'Romance', 'Biographie'],
                'min_rating': 8.0,
                'description': "Des films émouvants et profonds qui vous aideront à transformer votre tristesse en espoir."
            },
            'Neutral': {
                'keywords': ['normal', 'calme', 'tranquille', 'stable', 'ordinaire', 'régulier',
                           'moyen', 'équilibré', 'neutre', 'indifférent', 'serein'],
                'genres': ['Documentaire', 'Aventure', 'Science-fiction'],
                'min_rating': 7.5,
                'description': "Des films captivants qui vous feront voyager et réfléchir."
            },
            'Motivated': {
                'keywords': ['motivé', 'déterminé', 'ambitieux', 'confiant', 'fort', 'prêt',
                           'énergique', 'dynamique', 'volontaire', 'courageux', 'persévérant'],
                'genres': ['Biographie', 'Sport', 'Inspiration', 'Motivation'],
                'min_rating': 7.0,
                'description': "Des films inspirants qui renforceront votre motivation!"
            },
            'Thoughtful': {
                'keywords': ['pensif', 'réfléchi', 'curieux', 'intrigué', 'contemplatif',
                           'philosophique', 'intellectuel', 'mystérieux', 'profond',
                           'songeur', 'méditatif', 'introspectif'],
                'genres': ['Science-fiction', 'Mystère', 'Psychologique', 'Histoire'],
                'min_rating': 7.5,
                'description': "Des films qui stimuleront votre réflexion et votre imagination."
            },
            'Romantic': {
                'keywords': ['amoureux', 'romantique', 'passionné', 'tendre', 'sentimental',
                           'amour', 'séduisant', 'sensuel', 'affectueux', 'attaché',
                           'épris', 'aimant', 'charmé', 'attiré'],
                'genres': ['Romance', 'Comédie romantique', 'Drame romantique'],
                'min_rating': 7.0,
                'description': "Des films romantiques qui feront vibrer votre cœur."
            },
            'Tired': {
                'keywords': ['fatigué', 'épuisé', 'las', 'endormi', 'somnolent', 'exténué',
                           'repos', 'dormir', 'sommeil', 'calme', 'tranquille', 'paisible'],
                'genres': ['Animation', 'Comédie légère', 'Famille'],
                'min_rating': 7.0,
                'description': "Des films légers et relaxants parfaits pour se détendre."
            },
            'Stressed': {
                'keywords': ['stressé', 'anxieux', 'inquiet', 'tendu', 'nerveux', 'agité',
                           'préoccupé', 'angoissé', 'sous pression', 'débordé'],
                'genres': ['Comédie', 'Animation', 'Famille', 'Aventure'],
                'min_rating': 7.5,
                'description': "Des films divertissants qui vous aideront à vous détendre et à oublier votre stress."
            }
        }

    def preprocess_text(self, text):
        # Convertir en minuscules
        text = text.lower()
        # Supprimer la ponctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Tokenization simple par espace
        tokens = text.split()
        # Supprimer les stop words
        tokens = [token for token in tokens if token not in self.stop_words]
        return tokens

    def analyze_mood(self, text):
        if not text:
            return 'Neutral'  # Humeur par défaut
            
        tokens = self.preprocess_text(text)
        
        # Calculer les scores pour chaque catégorie d'humeur
        scores = {}
        for category, data in self.mood_categories.items():
            # Score basé sur la présence exacte des mots-clés
            exact_matches = sum(1 for token in tokens if token in data['keywords'])
            # Score basé sur la présence partielle des mots-clés (pour les variations)
            partial_matches = sum(1 for token in tokens for keyword in data['keywords'] 
                                if keyword in token and token != keyword)
            # Le score exact compte plus que le score partiel
            scores[category] = exact_matches * 2 + partial_matches

        # Afficher les scores pour le débogage
        print("Scores d'humeur:", scores)
        
        # Trouver la catégorie avec le score le plus élevé
        if not scores or max(scores.values()) == 0:
            return 'Neutral'  # Catégorie par défaut si aucune correspondance
        
        best_category = max(scores.items(), key=lambda x: x[1])[0]
        return best_category

    def get_mood_info(self, category):
        return self.mood_categories.get(category, self.mood_categories['Neutral']) 