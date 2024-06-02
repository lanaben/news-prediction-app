import pandas as pd
from flask import Flask, request, jsonify
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mlflow_tracking_uri = os.getenv("MLFLOW_URL")

if not mlflow_tracking_uri:
    raise ValueError("MLFLOW_URL environment variable not set. Please check your .env file.")

mlflow.set_tracking_uri(mlflow_tracking_uri)

# Set the experiment name where the model is stored
experiment_name = "news_prediction_model_metrics"

# Load the model from MLflow registry
model_name = "news_prediction_model"

def load_model():
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name)
    model_uri = f"models:/{model_name}/Production"
    loaded_model = mlflow.sklearn.load_model(model_uri)
    return loaded_model

# Load the model
model = load_model()

#TODO: endpoint for models, experiments, metrics

# def print_models_info(mv):
#     for m in mv:
#         print(f"name: {m.name}")
#         print(f"latest version: {m.version}")
#         print(f"run_id: {m.run_id}")
#         print(f"current_stage: {m.current_stage}")
#
# # Get all model versions and their corresponding experiments
# client = MlflowClient()
# models = client.get_latest_versions(model_name, stages=None)
# print_models_info(models)
# print("--")
#
# all_experiments = client.search_experiments()
# print(all_experiments)
#
# all_runs = mlflow.search_runs(search_all_experiments=True)
# import pandas as pd
#
# # Set display option to show all columns
# pd.set_option('display.max_columns', None)
#
# # Now print the DataFrame
# print(all_runs)
#
# try:
#     # Save DataFrame to a CSV file
#     all_runs.to_csv('all_runs.csv', index=False)
#     print("File saved successfully.")
# except Exception as e:
#     print(f"An error occurred while saving the file: {e}")

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
