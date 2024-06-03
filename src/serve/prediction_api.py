import json

import pandas as pd
from flask import Flask, request, jsonify, send_file
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import os
import logging
from dotenv import load_dotenv

REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'reports')
TESTING_REPORT = os.path.join(REPORTS_DIR, 'test_results.json')
VALIDATION_REPORT = os.path.join(REPORTS_DIR, 'validation_report.txt')

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

mlflow_tracking_uri = os.getenv("MLFLOW_URL")
if not mlflow_tracking_uri:
    raise ValueError("MLFLOW_URL environment variable not set. Please check your .env file.")
mlflow.set_tracking_uri(mlflow_tracking_uri)
experiment_name = "news_prediction_model_metrics"
model_name = "news_prediction_model"
client = MlflowClient()

def load_model():
    mlflow.set_experiment(experiment_name)
    model_uri = f"models:/{model_name}/Production"
    loaded_model = mlflow.sklearn.load_model(model_uri)
    return loaded_model

model = load_model()

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

@app.route('/latest-models', methods=['GET'])
def get_model_production():
    stage = request.args.get('stage', 'Production')
    models = client.get_latest_versions(model_name, stages=[stage])
    model_info = [{'name': m.name, 'version': m.version, 'run_id': m.run_id, 'current_stage': m.current_stage} for m in models]
    return jsonify(model_info)

@app.route('/models', methods=['GET'])
def get_models_all():
    stage = request.args.get('stage', None)
    if stage:
        models = client.search_model_versions(f"name='{model_name}' and current_stage='{stage}'")
    else:
        models = client.search_model_versions(f"name='{model_name}'")

    model_info = [{'name': m.name, 'version': m.version, 'run_id': m.run_id, 'current_stage': m.current_stage} for m in models]
    return jsonify(model_info)

@app.route('/change_model_stage', methods=['POST'])
def change_model_stage():
    data = request.get_json()
    model_name = data['model_name']
    version = data['version']
    new_stage = data['new_stage']

    try:
        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=new_stage
        )
        return jsonify(
            {'message': f'Model {model_name} version {version} transitioned to {new_stage} stage successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/experiments', methods=['GET'])
def get_experiments():
    experiments = client.search_experiments()
    experiment_info = [{'experiment_id': exp.experiment_id, 'name': exp.name, 'artifact_location': exp.artifact_location, 'lifecycle_stage': exp.lifecycle_stage} for exp in experiments]
    return jsonify(experiment_info)

@app.route('/runs', methods=['GET'])
def get_runs():
    experiment_id = request.args.get('experiment_id', None)
    if experiment_id:
        runs = mlflow.search_runs(experiment_ids=[experiment_id])
    else:
        runs = mlflow.search_runs(search_all_experiments=True)
    runs_info = runs.to_dict(orient='records')
    return jsonify(runs_info)

@app.route('/testing', methods=['GET'])
def get_results():
    if os.path.exists(TESTING_REPORT) and os.stat(TESTING_REPORT).st_size != 0:
        with open(TESTING_REPORT, 'r') as f:
            results = json.load(f)
        return jsonify(results)
    else:
        return jsonify({'error': 'No results available'})

@app.route('/validation', methods=['GET'])
def get_validation_results():
    if os.path.exists(VALIDATION_REPORT):
        return send_file(VALIDATION_REPORT, as_attachment=True)
    else:
        return jsonify({'error': 'Validation results not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
