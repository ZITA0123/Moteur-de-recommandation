import os
import json
import csv
from tqdm import tqdm

def count_lines(filename):
    """Compte le nombre de lignes dans un fichier"""
    with open(filename, 'rb') as f:
        return sum(1 for _ in f)

def load_local_dataset():
    """Charge le dataset depuis le fichier JSON local"""
    input_file = os.path.join('.kaggle', 'part-01.json')
    output_file = os.path.join('data', 'imdb_reviews.csv')
    
    print("Chargement du dataset local...")
    try:
        # Créer le dossier data s'il n'existe pas
        os.makedirs('data', exist_ok=True)
        
        # Compter le nombre total de lignes pour la barre de progression
        total_lines = count_lines(input_file)
        print(f"Nombre total de lignes à traiter : {total_lines}")
        
        # Préparer les compteurs
        processed = 0
        positive_count = 0
        negative_count = 0
        
        # Traiter le fichier ligne par ligne
        with open(input_file, 'r', encoding='utf-8') as fin, \
             open(output_file, 'w', newline='', encoding='utf-8') as fout:
            
            # Créer le writer CSV
            writer = csv.writer(fout)
            writer.writerow(['review', 'sentiment'])  # En-têtes
            
            # Traiter chaque ligne avec une barre de progression
            for line in tqdm(fin, total=total_lines, desc="Traitement des critiques"):
                try:
                    # Charger la ligne JSON
                    review_data = json.loads(line.strip())
                    
                    # Extraire le texte et le sentiment
                    text = review_data.get('text', '').replace('\n', ' ').replace('\r', ' ')
                    sentiment = 1 if review_data.get('sentiment', '').lower() == 'positive' else 0
                    
                    # Écrire dans le CSV
                    writer.writerow([text, sentiment])
                    
                    # Mettre à jour les compteurs
                    processed += 1
                    if sentiment == 1:
                        positive_count += 1
                    else:
                        negative_count += 1
                    
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    print(f"Erreur lors du traitement d'une ligne: {str(e)}")
                    continue
        
        print("\nStatistiques du dataset:")
        print(f"Nombre total de critiques traitées: {processed}")
        print(f"Critiques positives: {positive_count}")
        print(f"Critiques négatives: {negative_count}")
        print(f"Données sauvegardées dans: {output_file}")
        
        return True
    except Exception as e:
        print(f"Erreur lors du chargement des données: {str(e)}")
        return False

if __name__ == "__main__":
    load_local_dataset() 