import os
import joblib
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from dagshub import dagshub_logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from dotenv import load_dotenv

load_dotenv()
mlflow_url = os.getenv("MLFLOW_URL")

if not mlflow_url:
    raise ValueError("MLFLOW_URL environment variable not set. Please check your .env file.")

mlflow.set_tracking_uri(mlflow_url)

experiment_name = "news_prediction_model_metrics"
mlflow.set_experiment(experiment_name)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, '..', '..', 'data')
MODELS_DIR = os.path.join(ROOT_DIR, '..', '..', 'models')

data_path = os.path.join(DATA_DIR, "processed", "articles_with_keywords.csv")
df = pd.read_csv(data_path)

df['DateTime'] = pd.to_datetime(df['DateTime']).astype('int64') / 10 ** 9

X = df.drop(columns='Relevance')
y = df['Relevance']

preprocessor = ColumnTransformer(
    transformers=[
        ('title', TfidfVectorizer(), 'Title'),
        ('categories', OneHotEncoder(), ['Categories']),
        ('keywords', TfidfVectorizer(), 'Keywords'),
        ('datetime', 'passthrough', ['DateTime']),
        ('sentiment', 'passthrough', ['Sentiment'])
    ],
    remainder='drop'
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])


def get_production_model_r2(model_name):
    client = mlflow.tracking.MlflowClient()
    filter_string = f"name='{model_name}'"
    results = client.search_model_versions(filter_string)
    for version in results:
        if version.current_stage == 'Production':
            print(f"Found production model: Version {version.version}")
            run_id = version.run_id
            metrics = client.get_run(run_id).data.metrics
            print(f"Metrics for run_id {run_id}: {metrics}")
            return metrics.get('r2')
    return None


def transition_model_version_stage(model_name, model_version, stage):
    client = mlflow.tracking.MlflowClient()
    client.transition_model_version_stage(
        name=model_name,
        version=model_version,
        stage=stage
    )


with dagshub_logger() as logger, mlflow.start_run() as run:
    try:
        mlflow.set_tag("mlflow.runName", "run_" + pd.Timestamp.now().strftime("%Y%m%d_%H%M%S"))
        mlflow.log_param("experiment_name", experiment_name)

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)

        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        print(f"Mean Squared Error: {mse}")
        print(f"Mean Absolute Error: {mae}")
        print(f"R^2: {r2}")

        model_info = mlflow.sklearn.log_model(model, "model")

        print(f"Model logged in run {run.info.run_id}")

        model_name = "news_prediction_model"
        model_version = mlflow.register_model(model_uri=model_info.model_uri, name=model_name)

        print(f"Model registered as {model_name} with version {model_version.version}")

        production_r2 = get_production_model_r2(model_name)
        print(f"Current production model R^2: {production_r2}")

        if production_r2 is None or r2 > production_r2:
            transition_model_version_stage(model_name, model_version.version, "Production")
            print(f"New model version {model_version.version} transitioned to Production")
        else:
            print(f"New model version {model_version.version} is not better than the current production model")

        model_path = os.path.join(MODELS_DIR, "news_prediction_model.joblib")
        model_path_compressed = os.path.join(MODELS_DIR, "news_prediction_model_compressed.joblib")

        joblib.dump(model, model_path)
        print(f"Uncompressed Random Forest: {np.round(os.path.getsize(model_path) / 1024 / 1024, 2)} MB")

        joblib.dump(model, model_path_compressed, compress=3)
        print(f"Compressed Random Forest: {np.round(os.path.getsize(model_path_compressed) / 1024 / 1024, 2)} MB")

        logger.log_hyperparams({"n_estimators": 100, "random_state": 42})
        logger.log_metrics({"mse": mse, "mae": mae, "r2": r2})

    except Exception as e:
        print(f"An error occurred: {e}")
        mlflow.end_run(status='FAILED')
    else:
        mlflow.end_run(status='FINISHED')