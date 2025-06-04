const OMDB_API_KEY = "TA_CLE_OMDB"; // Remplace par ta vraie clé OMDb

// Appel backend pour recommandations basées sur l'émotion
function getRecommendations() {
  const mood = document.getElementById('mood').value;
  fetch(`http://localhost:8000/recommend?mood=${encodeURIComponent(mood)}`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('suggestions');
      container.innerHTML = '';
      data.forEach(async film => {
        const poster = await fetchPoster(film.title);
        const card = `<div class="film-card">
          <h3>${film.title}</h3>
          <img src="${poster}" alt="${film.title}" />
          <p>Note IMDb : ${film.imdb_score}</p>
        </div>`;
        container.innerHTML += card;
      });
    })
    .catch(err => console.error('Erreur reco:', err));
}

// Appel backend pour analyse de critique
function analyzeReview() {
  const review = document.getElementById('user-review').value;
  fetch('http://localhost:8000/analyze-review', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ review: review })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById('review-result').innerHTML = `
        <p>Sentiment : ${data.sentiment}</p>
        <h4>Films similaires :</h4>
        <ul>${data.recommended.map(f => `<li>${f.title}</li>`).join('')}</ul>
      `;
    })
    .catch(err => console.error('Erreur analyse:', err));
}

// Récupération d'affiche depuis OMDb
function fetchPoster(title) {
  return fetch(`https://www.omdbapi.com/?t=${encodeURIComponent(title)}&apikey=${OMDB_API_KEY}`)
    .then(res => res.json())
    .then(data => data.Poster || '')
    .catch(() => '');
}

// Exemple de wordclouds (données fictives)
document.addEventListener('DOMContentLoaded', () => {
  WordCloud(document.getElementById('wordcloud-positive'), {
    list: [['magnifique', 20], ['intense', 15], ['génial', 10]]
  });
  WordCloud(document.getElementById('wordcloud-negative'), {
    list: [['lent', 18], ['décevant', 12], ['vide', 9]]
  });
});
