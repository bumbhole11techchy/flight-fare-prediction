# YieldWings: AI-Driven Airline Yield Management

## Overview
YieldWings is a data-driven system designed to optimize airline ticket pricing. It uses machine learning to predict demand based on flight characteristics and competitor pricing, allowing airlines to adjust prices dynamically to maximize revenue.

## Features
- **Synthetic Data Generation**: Creates realistic flight datasets.
- **Demand Forecasting**: Random Forest model to predict booking rates.
- **Price Optimization**: Algorithm to find the revenue-maximizing price point.
- **FastAPI Backend**: Serves predictions and optimization results.
- **Streamlit Dashboard**: Interactive UI for managers.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Generate Data**:
    ```bash
    python src/data_generator.py
    ```

3.  **Train Models**:
    ```bash
    python src/train_models.py
    ```

## Running the Application

### 1. Start the Backend API
Run this in a terminal:
```bash
python -m uvicorn app.api:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 2. Start the Frontend Dashboard
Run this in a **separate** terminal:
```bash
python -m streamlit run app/dashboard.py
```
The dashboard will open in your browser.

## API Endpoints
- `POST /predict_demand`: Predicts seats booked for a given price.
- `POST /optimize_price`: Returns the optimal price for a route.
