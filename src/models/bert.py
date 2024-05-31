import pandas as pd
from keybert import KeyBERT
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, '..', '..', 'data')
raw_data_path = os.path.join(DATA_DIR, "raw", "articles.csv")
processed_data_path = os.path.join(DATA_DIR, "processed", "articles_with_keywords.csv")

raw_df = pd.read_csv(raw_data_path)

kw_model = KeyBERT()

raw_df['Keywords'] = raw_df['Title'].apply(lambda x: ", ".join([keyword[0] for keyword in kw_model.extract_keywords(x)]))

raw_df.to_csv(processed_data_path, index=False)

print("Data saved to", processed_data_path)
