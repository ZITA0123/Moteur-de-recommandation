import os
import json
import csv
from tqdm import tqdm

def convert_json_to_csv():
    """Convertit le fichier JSON en CSV"""
    input_file = os.path.join('.kaggle', 'part-01.json')
    output_file = os.path.join('data', 'reviews.csv')
    
    print(f"Conversion de {input_file} en CSV...")
    
    try:
        # Créer le dossier data s'il n'existe pas
        os.makedirs('data', exist_ok=True)
        
        # Compter le nombre de lignes pour la barre de progression
        print("Comptage des lignes...")
        with open(input_file, 'rb') as f:
            total_lines = sum(1 for _ in f)
        print(f"Nombre total de lignes à traiter : {total_lines}")
        
        # Initialiser les compteurs
        processed = 0
        errors = 0
        
        # Ouvrir les fichiers et commencer la conversion
        with open(input_file, 'r', encoding='utf-8') as fin, \
             open(output_file, 'w', newline='', encoding='utf-8') as fout:
            
            # Créer le writer CSV
            writer = csv.writer(fout, quoting=csv.QUOTE_ALL)
            # Écrire l'en-tête
            writer.writerow(['text', 'sentiment'])
            
            # Traiter chaque ligne avec une barre de progression
            for line in tqdm(fin, total=total_lines, desc="Conversion en cours"):
                try:
                    # Charger les données JSON
                    data = json.loads(line.strip())
                    
                    # Si c'est une liste, traiter chaque élément
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                text = item.get('text', '').replace('\n', ' ').replace('\r', ' ')
                                sentiment = item.get('sentiment', '').lower()
                                if text and sentiment:
                                    writer.writerow([text, sentiment])
                                    processed += 1
                    # Si c'est un dictionnaire, traiter directement
                    elif isinstance(data, dict):
                        text = data.get('text', '').replace('\n', ' ').replace('\r', ' ')
                        sentiment = data.get('sentiment', '').lower()
                        if text and sentiment:
                            writer.writerow([text, sentiment])
                            processed += 1
                
                except json.JSONDecodeError as e:
                    errors += 1
                    continue
                except Exception as e:
                    errors += 1
                    print(f"\nErreur lors du traitement d'une ligne: {str(e)}")
                    continue
        
        # Afficher les statistiques
        print("\nConversion terminée!")
        print(f"Critiques traitées avec succès: {processed}")
        print(f"Erreurs rencontrées: {errors}")
        print(f"Fichier CSV créé: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors de la conversion: {str(e)}")
        return False

if __name__ == "__main__":
    convert_json_to_csv() 