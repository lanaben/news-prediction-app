import pandas as pd
from keybert import KeyBERT
import os

raw_data_path = "../../data/raw/articles.csv"
raw_df = pd.read_csv(raw_data_path)

kw_model = KeyBERT()

raw_df['Keywords'] = raw_df['Title'].apply(lambda x: ", ".join([keyword[0] for keyword in kw_model.extract_keywords(x)]))

processed_data_dir = "../../data/processed"
os.makedirs(processed_data_dir, exist_ok=True)
processed_data_path = os.path.join(processed_data_dir, "articles_with_keywords.csv")

raw_df.to_csv(processed_data_path, index=False)

print("Data saved to", processed_data_path)
