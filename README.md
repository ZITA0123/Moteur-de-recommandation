# MovieMood - IMDb Explorer

Une application Streamlit pour explorer les films IMDb et analyser les critiques.

## 🚀 Fonctionnalités

- Recherche de films via l'API IMDb
- Affichage détaillé des informations sur les films
- Visualisation des critiques et des notes
- Interface utilisateur moderne et intuitive
- Graphiques interactifs avec Plotly

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Clé API IMDb (à obtenir sur [IMDb API](https://developer.imdb.com/))

## 🛠️ Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/MovieMood.git
cd MovieMood
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez votre clé API :
   - Créez un fichier `.env` à la racine du projet
   - Ajoutez votre clé API IMDb :
     ```
     IMDB_API_KEY=votre_clé_api_ici
     ```

## 🎮 Utilisation

1. Lancez l'application :
```bash
streamlit run app.py
```

2. Ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8501)

## 📱 Interface

- **Recherche de films** : Entrez un titre de film pour obtenir des résultats détaillés
- **Analyse des critiques** : Visualisez les statistiques et tendances des critiques
- **Menu latéral** : Navigation facile entre les différentes fonctionnalités

## 🔒 Sécurité

- Ne partagez jamais votre clé API IMDb
- Le fichier `.env` est ignoré par Git pour protéger vos informations sensibles

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- Votre nom - Développement initial

## 🙏 Remerciements

- IMDb pour leur API
- Streamlit pour leur excellent framework
- La communauté open source pour leurs contributions 