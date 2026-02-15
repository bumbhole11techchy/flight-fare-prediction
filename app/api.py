from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="YieldWings API", description="Airline Yield Management System API")

# Load Model
MODEL_PATH = os.path.join('models', 'demand_model.pkl')
model = None

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

class FlightInput(BaseModel):
    route: str
    day_of_week: int
    days_prior: int
    is_weekend: int
    competitor_price: float
    price: float

class OptimizationInput(BaseModel):
    route: str
    day_of_week: int
    days_prior: int
    is_weekend: int
    competitor_price: float
    base_price: float

@app.get("/")
def home():
    return {"message": "Welcome to YieldWings API"}

@app.post("/predict_demand")
def predict_demand(input_data: FlightInput):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Create DataFrame
    data = pd.DataFrame([input_data.dict()])
    
    # Predict
    prediction = model.predict(data)[0]
    return {"predicted_demand": int(prediction)}

@app.post("/optimize_price")
def optimize_price(input_data: OptimizationInput):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Simple optimization loop
    # Try prices from 0.5x to 1.5x of base_price
    min_price = input_data.base_price * 0.5
    max_price = input_data.base_price * 1.5
    
    best_price = input_data.base_price
    max_revenue = 0
    
    # Test 20 price points
    test_prices = np.linspace(min_price, max_price, 20)
    
    for price in test_prices:
        # Construct input for predictor
        row = {
            'route': input_data.route,
            'day_of_week': input_data.day_of_week,
            'days_prior': input_data.days_prior,
            'is_weekend': input_data.is_weekend,
            'competitor_price': input_data.competitor_price,
            'price': price
        }
        df = pd.DataFrame([row])
        pred_demand = model.predict(df)[0]
        
        # Assume capacity is 200 for simplicity (can be parameterized)
        capacity = 200
        bookings = min(pred_demand, capacity)
        revenue = bookings * price
        
        if revenue > max_revenue:
            max_revenue = revenue
            best_price = price
            
    return {
        "optimal_price": round(best_price, 2),
        "predicted_revenue": round(max_revenue, 2),
        "predicted_bookings": int(max_revenue / best_price) if best_price > 0 else 0
    }
