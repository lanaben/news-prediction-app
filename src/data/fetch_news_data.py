import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()
apiKey = os.getenv("API_KEY")

url = "https://newsapi.ai/api/v1/article/getArticles"

payload = {
    "query": {
        "$query": {
            "$and": [
                {
                    "conceptUri": "http://en.wikipedia.org/wiki/Technology"
                },
                {
                    "dateStart": "2024-05-28",
                    "dateEnd": "2024-05-28",
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

data = response.json()

csv_file_path = "../../data/raw/articles.csv"
with open(csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    articles = data.get("articles", {}).get("results", [])

    for article in articles:
        first_category_label = ""
        if article.get("categories", []):
            category_label = article.get("categories", [])[0].get("label", "")
            if category_label:
                first_category_label = category_label.split("/")[1]  # Get the first word after 'dmoz/'

        csv_writer.writerow([
            article.get("dateTime", ""),
            article.get("title", ""),
            first_category_label,
            article.get("sentiment", ""),
            article.get("relevance", "")
        ])

print("Data saved to", csv_file_path)
