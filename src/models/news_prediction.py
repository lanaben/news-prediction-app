import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Read the data from CSV
df = pd.read_csv('../../data/processed/articles_with_keywords.csv')

# Convert DateTime to numerical value (timestamp)
df['DateTime'] = pd.to_datetime(df['DateTime']).astype('int64') / 10 ** 9

# Split data into features and target
X = df.drop(columns='Relevance')
y = df['Relevance']

# Preprocess the data
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

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with preprocessor and Random Forest Regressor
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"Mean Absolute Error: {mae}")
print(f"R^2: {r2}")

joblib.dump(model, '../../models/news_prediction_model.h5')
