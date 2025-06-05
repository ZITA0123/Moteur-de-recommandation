import json
import pandas as pd
from tqdm import tqdm
import sys

def convert_json_to_csv(input_file, output_file):
    print(f"Reading JSON file: {input_file}")
    
    # Read the JSON file line by line to handle large files
    reviews = []
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Assuming the structure has a "root" key with a list of reviews
        if isinstance(data, dict) and "root" in data:
            reviews_data = data["root"]
        else:
            reviews_data = data
            
        for review in tqdm(reviews_data, desc="Processing reviews"):
            reviews.append({
                'review_id': review.get('review_id', ''),
                'movie': review.get('movie', ''),
                'rating': review.get('rating', ''),
                'review_summary': review.get('review_summary', ''),
                'review_detail': review.get('review_detail', ''),
                'review_date': review.get('review_date', '')
            })
    
    print("Converting to DataFrame...")
    df = pd.DataFrame(reviews)
    
    print(f"Saving to CSV: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Successfully converted {len(reviews)} reviews to CSV!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python json_to_csv_converter.py <input_json_file> <output_csv_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_json_to_csv(input_file, output_file) 