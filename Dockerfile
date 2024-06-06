FROM python:3.11-slim
WORKDIR /news_prediction
COPY src/serve/ ./src/serve/
COPY models ./models
COPY data ./data
COPY reports ./reports
COPY api_requirements.txt ./
ENV MLFLOW_URL=https://lanaben:7ddc36c3f8a57b0df9f619f50e6f0a2cf6da5f55@dagshub.com/lanaben/news-prediction-app.mlflow
RUN pip install --trusted-host pypi.python.org -r api_requirements.txt
EXPOSE 5000
ENV NAME NewsPrediction
CMD ["python", "src/serve/prediction_api.py"]