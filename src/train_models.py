import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import joblib
import os

def train_models():
    print("Loading data...")
    # Load data
    data_path = os.path.join('data', 'flight_data.csv')
    if not os.path.exists(data_path):
        print("Data not found. Please run data_generator.py first.")
        return

    df = pd.read_csv(data_path)
    
    # Features and Target
    X = df[['route', 'day_of_week', 'days_prior', 'is_weekend', 'competitor_price', 'price']]
    y = df['bookings'] # Target: Demand
    
    # Preprocessing
    categorical_features = ['route']
    numerical_features = ['day_of_week', 'days_prior', 'is_weekend', 'competitor_price', 'price']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', 'passthrough', numerical_features)
        ])
        
    # Model Pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Demand Forecasting Model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Model MAE: {mae:.2f}")
    
    # Save Model
    print("Saving model...")
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, os.path.join('models', 'demand_model.pkl'))
    print("Model saved to models/demand_model.pkl")

if __name__ == "__main__":
    train_models()
