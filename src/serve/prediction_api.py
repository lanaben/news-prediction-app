import pandas as pd
from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the model
model = joblib.load('../../models/news_prediction_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    example_data = {
        'DateTime': [data['DateTime']],
        'Title': [data['Title']],
        'Categories': [data['Categories']],
        'Sentiment': [data['Sentiment']],
        'Keywords': [data['Keywords']]
    }
    example_df = pd.DataFrame(example_data)
    example_df['DateTime'] = pd.to_datetime(example_df['DateTime']).astype('int64') / 10 ** 9
    prediction = model.predict(example_df)
    return jsonify({'prediction': prediction.tolist()})

@app.route('/articles', methods=['GET'])
def get_articles():
    articles_df = pd.read_csv('../../data/raw/articles.csv')
    random_articles = articles_df.sample(5).to_dict(orient='records')
    return jsonify(random_articles)

if __name__ == '__main__':
    app.run(debug=True)
