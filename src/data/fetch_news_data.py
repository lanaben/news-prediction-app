from datetime import datetime, timedelta

import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()
apiKey = os.getenv("API_KEY")

if not apiKey:
    raise ValueError("API_KEY environment variable is not set")

yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y-%m-%d")

url = "https://newsapi.ai/api/v1/article/getArticles"

payload = {
    "query": {
        "$query": {
            "$and": [
                {
                    "conceptUri": "http://en.wikipedia.org/wiki/Technology"
                },
                {
                    "dateStart": date_str,
                    "dateEnd": date_str,
                    "lang": "eng"
                }
            ]
        },
        "$filter": {
            "isDuplicate": "skipDuplicates"
        }
    },
    "resultType": "articles",
    "articlesSortBy": "date",
    "includeArticleSocialScore": True,
    "includeArticleConcepts": True,
    "includeArticleCategories": True,
    "apiKey": apiKey
}

response = requests.post(url, json=payload)

print(f"Response status code: {response.status_code}")
print(f"Response content: {response.text}")

if response.text.strip() == "":
    print("The API returned an empty response.")
    exit(1)

try:
    data = response.json()
except requests.exceptions.JSONDecodeError as e:
    print(f"Failed to decode JSON response: {e}")
    exit(1)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, '..', '..', 'data')
csv_file_path = os.path.join(DATA_DIR, "raw", "articles.csv")

with open(csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    articles = data.get("articles", {}).get("results", [])

    for article in articles:
        first_category_label = ""
        if article.get("categories", []):
            category_label = article.get("categories", [])[0].get("label", "")
            if category_label:
                first_category_label = category_label.split("/")[1]

        csv_writer.writerow([
            article.get("dateTime", ""),
            article.get("title", ""),
            first_category_label,
            article.get("sentiment", ""),
            article.get("relevance", "")
        ])

print("Data saved to", csv_file_path)
