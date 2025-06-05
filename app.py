import streamlit as st
import pandas as pd
from users import UserManager
from mood_analyzer import MoodAnalyzer

# Configuration de la page
st.set_page_config(
    page_title="MovieMood - Recommandations de Films",
    page_icon="🎬",
    layout="wide"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0 10px;
        margin-bottom: 20px;
    }
    .sidebar-header img {
        width: 50px;
        height: 50px;
    }
    .sidebar-header h1 {
        margin: 0;
        font-size: 24px;
        color: #ff4b4b;
    }
    .mood-input {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #ff3333;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .user-welcome {
        font-size: 0.9em;
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .movie-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid #e0e0e0;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .movie-poster {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .movie-title {
        color: #1f1f1f;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .movie-info {
        color: #666;
        font-size: 0.9em;
        margin-bottom: 10px;
    }
    .movie-rating {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 15px;
    }
    .movie-genre {
        display: inline-block;
        background-color: #f0f2f6;
        color: #666;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    .movie-modal {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        margin: 20px 0;
    }
    .movie-detail-poster {
        width: 100%;
        max-height: 400px;
        object-fit: cover;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .movie-detail-title {
        color: #ff4b4b;
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .movie-detail-info {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des gestionnaires
user_manager = UserManager()
mood_analyzer = MoodAnalyzer()

def sidebar_nav():
    with st.sidebar:
        # En-tête avec logo et titre
        st.markdown(
            """
            <div class="sidebar-header">
                <img src="https://img.icons8.com/clouds/100/cinema-.png" alt="MovieMood Logo"/>
                <h1>MovieMood</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

        # Affichage du statut de connexion
        if st.session_state.get('logged_in', False):
            st.markdown(f"""
            <div class="user-welcome">
                👋 Bienvenue, {st.session_state['username']}!
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚪 Se déconnecter", key="logout_button"):
                st.session_state['logged_in'] = False
                st.session_state['username'] = None
                st.rerun()
        else:
            st.markdown("""
            <div class="user-welcome">
                👋 Mode invité
            </div>
            """, unsafe_allow_html=True)
            st.write("Connectez-vous pour accéder à plus de fonctionnalités!")

        # Menu de navigation
        return st.radio(
            "Navigation",
            ["🏠 Accueil", "👤 Connexion", "📝 Inscription"],
            key="navigation"
        )

def login_form():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.header("👤 Connexion")
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter")
            
            if submit:
                if user_manager.verify_user(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success("Connexion réussie!")
                    st.rerun()
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect")

def register_form():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.header("📝 Inscription")
        with st.form("register_form"):
            new_username = st.text_input("Choisir un nom d'utilisateur")
            new_password = st.text_input("Choisir un mot de passe", type="password")
            confirm_password = st.text_input("Confirmer le mot de passe", type="password")
            
            submit = st.form_submit_button("S'inscrire")
            
            if submit:
                if new_password != confirm_password:
                    st.error("Les mots de passe ne correspondent pas")
                else:
                    success, message = user_manager.register_user(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

def get_movie_poster(movie_title):
    # Dictionnaire des affiches de films
    posters = {
        "La La Land": "https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_.jpg",
        "Inception": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
        "Le Fabuleux Destin d'Amélie Poulain": "https://m.media-amazon.com/images/M/MV5BNDg4NjM1YjMtYmNhZC00MjM0LWFiZmYtNGY1YjA3MzZmODc5XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_.jpg",
        "The Pursuit of Happyness": "https://m.media-amazon.com/images/M/MV5BMTQ5NjQ0NDI3NF5BMl5BanBnXkFtZTcwNDI0MjEzMw@@._V1_.jpg",
        "Inside Out": "https://m.media-amazon.com/images/M/MV5BOTgxMDQwMDk0OF5BMl5BanBnXkFtZTgwNjU5OTg2NDE@._V1_.jpg",
        "The Intouchables": "https://m.media-amazon.com/images/M/MV5BMTYxNDA3MDQwNl5BMl5BanBnXkFtZTcwNTU4Mzc1Nw@@._V1_.jpg",
        "Forrest Gump": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
        "The Shawshank Redemption": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg",
        "Schindler's List": "https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
        "Life is Beautiful": "https://m.media-amazon.com/images/M/MV5BYmJmM2Q4NmMtYThmNC00ZjRlLWEyZmItZTIwOTBlZDQ3NTQ1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
        "The Lion King": "https://m.media-amazon.com/images/M/MV5BYTYxNGMyZTYtMjE3MS00MzNjLWFjNmYtMDk3N2FmM2JiM2M1XkEyXkFqcGdeQXVyNjY5NDU4NzI@._V1_.jpg",
        "Up": "https://m.media-amazon.com/images/M/MV5BMTk3NDE2NzI4NF5BMl5BanBnXkFtZTgwNzE1MzEyMTE@._V1_.jpg",
        "The Notebook": "https://m.media-amazon.com/images/M/MV5BMTk3OTM5Njg5M15BMl5BanBnXkFtZTYwMzA0ODI3._V1_.jpg",
        "Eternal Sunshine of the Spotless Mind": "https://m.media-amazon.com/images/M/MV5BMTY4NzcwODg3Nl5BMl5BanBnXkFtZTcwNTEwOTMyMw@@._V1_.jpg",
        "The Grand Budapest Hotel": "https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_.jpg",
        "Spirited Away": "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZDBhYWQ0NTcxNWRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
        "Dead Poets Society": "https://m.media-amazon.com/images/M/MV5BOGYwYWNjMzgtNGU4ZC00NWQ2LWEwZjUtMzE1Zjc3NjY3YTU1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
        "Good Will Hunting": "https://m.media-amazon.com/images/M/MV5BOTI0MzcxMTYtZDVkMy00NjY1LTgyMTYtZmUxN2M3NmQ2NWJhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
        "The Theory of Everything": "https://m.media-amazon.com/images/M/MV5BMTAwMTU4MDA3NDNeQTJeQWpwZ15BbWU4MDk4NTMxNTIx._V1_.jpg",
        "Wonder": "https://m.media-amazon.com/images/M/MV5BYjFhOWY0OTgtNDkzMC00YWJkLTk1NGEtYWUxNjhmMmQ5ZjYyXkEyXkFqcGdeQXVyMjMxOTE0ODA@._V1_.jpg",
        "Big Hero 6": "https://m.media-amazon.com/images/M/MV5BMDliOTIzNmUtOTllOC00NDU3LWFiNjYtMGM0NDc1YTMxNjYxXkEyXkFqcGdeQXVyNTM3NzExMDQ@._V1_.jpg",
        "The Secret Life of Walter Mitty": "https://m.media-amazon.com/images/M/MV5BODYwNDYxNDk1Nl5BMl5BanBnXkFtZTgwOTAwMTk2MDE@._V1_.jpg",
        "Soul": "https://m.media-amazon.com/images/M/MV5BZGE1MDg5M2MtNTkyZS00MTY5LTg1YzUtZTlhZmM1Y2EwNmFmXkEyXkFqcGdeQXVyNjA3OTI0MDc@._V1_.jpg",
        "The Truman Show": "https://m.media-amazon.com/images/M/MV5BMDIzODcyY2EtMmY2MC00ZWVlLTgwMzAtMjQwOWUyNmJjNTYyXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_.jpg",
        "Cast Away": "https://m.media-amazon.com/images/M/MV5BN2Y5ZTU4YjctMDRmMC00MTg4LWE1M2MtMjk4MzVmOTE4YjkzXkEyXkFqcGdeQXVyNTc1NTQxODI@._V1_.jpg",
        "A Beautiful Mind": "https://m.media-amazon.com/images/M/MV5BMzcwYWFkYzktZjAzNC00OGY1LWI4YTgtNzc5MzVjMDVmNjY0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
        "The Bucket List": "https://m.media-amazon.com/images/M/MV5BMTY2NTg4MjU3MF5BMl5BanBnXkFtZTcwMDc3NjA2MQ@@._V1_.jpg",
        "The Help": "https://m.media-amazon.com/images/M/MV5BMTM5OTMyMjIxOV5BMl5BanBnXkFtZTcwNzU4MjIwNQ@@._V1_.jpg",
        "Little Miss Sunshine": "https://m.media-amazon.com/images/M/MV5BMTgzNTgzODU0NV5BMl5BanBnXkFtZTcwMjEyMjMzMQ@@._V1_.jpg",
        "The Terminal": "https://m.media-amazon.com/images/M/MV5BMTM1MTIwNDM2OF5BMl5BanBnXkFtZTcwNjIxMjQyMw@@._V1_.jpg"
    }
    return posters.get(movie_title, "https://img.icons8.com/clouds/100/cinema-.png")  # Image par défaut si le film n'est pas trouvé

def display_movie_card(movie, col):
    with col:
        card = st.container()
        with card:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{get_movie_poster(movie['movie'])}" class="movie-poster" alt="{movie['movie']}">
                <div class="movie-title">{movie['movie']}</div>
                <div class="movie-rating">⭐ {movie['rating']}/10</div>
                <div class="movie-info">
                    <p>📅 {movie['review_date']}</p>
                    <p>{movie['review_summary']}</p>
                </div>
                <div>
                    {' '.join([f'<span class="movie-genre">{genre.strip()}</span>' for genre in movie['genre'].split(',')])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Voir plus", key=f"btn_{movie['movie']}"):
                st.session_state['selected_movie'] = movie
                st.rerun()

def display_movie_details(movie):
    st.markdown(f"""
    <div class="movie-modal">
        <img src="{get_movie_poster(movie['movie'])}" class="movie-detail-poster" alt="{movie['movie']}">
        <div class="movie-detail-title">{movie['movie']}</div>
        <div class="movie-detail-info">
            <p><strong>Date de sortie:</strong> {movie['review_date']}</p>
            <p><strong>Note:</strong> ⭐ {movie['rating']}/10</p>
            <p><strong>Genres:</strong> {movie['genre']}</p>
        </div>
        <h3>Résumé</h3>
        <p>{movie['review_summary']}</p>
        <h3>Critique détaillée</h3>
        <p>{movie['review_detail']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Retour aux recommandations"):
        st.session_state['selected_movie'] = None
        st.rerun()

def mood_form():
    st.title("🎬 Trouvez le film parfait pour votre humeur!")
    st.write("Laissez-nous vous recommander des films en fonction de votre humeur.")
    
    with st.container():
        st.markdown('<div class="mood-input">', unsafe_allow_html=True)
        mood_text = st.text_area(
            "💭 Comment vous sentez-vous aujourd'hui?",
            placeholder="Décrivez votre humeur en quelques mots...\nPar exemple: Je me sens très heureux et enthousiaste aujourd'hui!",
            height=100
        )
        col1, col2, col3 = st.columns([2,1,2])
        with col2:
            search_button = st.button("🔍 Trouver des films", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if search_button and mood_text:
        # Analyser l'humeur
        mood_category = mood_analyzer.analyze_mood(mood_text)
        mood_info = mood_analyzer.get_mood_info(mood_category)
        
        # Afficher la catégorie d'humeur détectée
        st.success(f"✨ Humeur détectée : {mood_category}")
        st.info(f"🎯 {mood_info['description']}")
        
        try:
            # Charger et filtrer les films
            df = pd.read_csv('movies_data.csv')
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            filtered_df = df[df['rating'] >= mood_info['min_rating']]
            
            if len(filtered_df) > 0:
                st.subheader("🍿 Films recommandés")
                
                # Créer des colonnes pour les films
                cols = st.columns(3)
                
                # Afficher les films en grille
                for idx, movie in filtered_df.head(6).iterrows():
                    with cols[idx % 3]:
                        st.markdown(f"""
                        <div class="movie-card">
                            <img src="{get_movie_poster(movie['movie'])}" class="movie-poster" alt="{movie['movie']}">
                            <div class="movie-title">{movie['movie']}</div>
                            <div class="movie-rating">⭐ {movie['rating']}/10</div>
                            <div class="movie-info">
                                <p>📅 {movie['review_date']}</p>
                                <p>{movie['review_summary']}</p>
                            </div>
                            <div>
                                {' '.join([f'<span class="movie-genre">{genre.strip()}</span>' for genre in movie['genre'].split(',')])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Créer un conteneur pour les détails qui sera initialement caché
                        details_container = st.empty()
                        
                        # Bouton pour afficher/masquer les détails
                        if st.button(f"Voir plus", key=f"btn_{movie['movie']}"):
                            with details_container:
                                st.markdown(f"""
                                <div class="movie-modal">
                                    <img src="{get_movie_poster(movie['movie'])}" class="movie-detail-poster" alt="{movie['movie']}">
                                    <div class="movie-detail-title">{movie['movie']}</div>
                                    <div class="movie-detail-info">
                                        <p><strong>Date de sortie:</strong> {movie['review_date']}</p>
                                        <p><strong>Note:</strong> ⭐ {movie['rating']}/10</p>
                                        <p><strong>Genres:</strong> {movie['genre']}</p>
                                    </div>
                                    <h3>Résumé</h3>
                                    <p>{movie['review_summary']}</p>
                                    <h3>Critique détaillée</h3>
                                    <p>{movie['review_detail']}</p>
                                </div>
                                """, unsafe_allow_html=True)
            else:
                st.warning("Aucun film ne correspond à vos critères pour le moment.")
                
        except FileNotFoundError:
            st.error("Base de données de films non trouvée.")
            st.info("Contactez l'administrateur pour plus d'informations.")
    elif search_button:
        st.warning("📝 Veuillez décrire votre humeur avant de chercher des films.")

def main():
    # Initialiser l'état de la session si nécessaire
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
    if 'selected_movie' not in st.session_state:
        st.session_state['selected_movie'] = None
    
    # Navigation
    selected_page = sidebar_nav()
    
    # Affichage de la page appropriée
    if selected_page == "👤 Connexion":
        login_form()
    elif selected_page == "📝 Inscription":
        register_form()
    else:  # Accueil
        mood_form()  # Afficher directement le formulaire d'humeur

if __name__ == "__main__":
    main() 