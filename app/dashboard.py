import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# API URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="YieldWings Dashboard", layout="wide")

st.title("✈️ YieldWings: Airline Yield Management System")

# Sidebar for Navigation
page = st.sidebar.selectbox("Select View", ["Airline Manager", "Passenger Predictor"])

if page == "Airline Manager":
    st.header("Yield Management Console")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Flight Parameters")
        route = st.selectbox("Route", ['JFK-LHR', 'LHR-JFK', 'SFO-JFK', 'JFK-SFO', 'LHR-DXB', 'DXB-LHR'])
        days_prior = st.slider("Days Prior to Flight", 1, 90, 30)
        competitor_price = st.number_input("Competitor Price ($)", value=300.0)
        
        # Derived inputs
        today = datetime.now()
        day_of_week = today.weekday() # Simplified: assuming prediction for 'today' relative to flight
        is_weekend = 1 if day_of_week >= 5 else 0
        
    with col2:
        st.subheader("Optimization")
        base_price_guess = st.number_input("Base Price Guess ($)", value=300.0)
        
        if st.button("Find Optimal Price"):
            payload = {
                "route": route,
                "day_of_week": day_of_week,
                "days_prior": days_prior,
                "is_weekend": is_weekend,
                "competitor_price": competitor_price,
                "base_price": base_price_guess
            }
            try:
                response = requests.post(f"{API_URL}/optimize_price", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Optimal Price: ${result['optimal_price']}")
                    st.metric("Predicted Revenue", f"${result['predicted_revenue']}")
                    st.metric("Predicted Bookings", f"{result['predicted_bookings']}")
                else:
                    st.error("Error connecting to API")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
                st.info("Make sure you are running the API with: `uvicorn app.api:app --reload`")

    # Real-time Simulation
    st.divider()
    st.subheader("Price vs. Revenue Simulator")
    
    # Generate curve data locally for visualization (simulating what API does)
    # We'll just call the API for a few points if possible, or if not visualize statically
    # To avoid too many API calls, we'll just allow user to sweep simple price
    
    test_price = st.slider("Test Price Point ($)", 100, 1000, int(base_price_guess))
    
    if st.button("Predict Demand for Price"):
        payload = {
            "route": route,
            "day_of_week": day_of_week,
            "days_prior": days_prior,
            "is_weekend": is_weekend,
            "competitor_price": competitor_price,
            "price": float(test_price)
        }
        try:
            res = requests.post(f"{API_URL}/predict_demand", json=payload)
            if res.status_code == 200:
                demand = res.json()['predicted_demand']
                st.metric("Predicted Demand", f"{demand} seats")
            else:
                st.error("API Error")
        except:
            st.error("API Connection Error")

elif page == "Passenger Predictor":
    st.header("Passsenger Price Forecaster")
    st.write("Should I buy now or wait?")
    
    route = st.selectbox("Route", ['JFK-LHR', 'LHR-JFK', 'SFO-JFK', 'JFK-SFO'])
    
    # Mock Data for trends
    dates = pd.date_range(end=datetime.now(), periods=10).strftime("%Y-%m-%d")
    prices = [300 + i*10 + (50 if i%2==0 else -50) for i in range(10)]
    
    df_trend = pd.DataFrame({"Date": dates, "Price": prices})
    
    fig = px.line(df_trend, x="Date", y="Price", title=f"Price Trend for {route} (Last 10 Days)")
    st.plotly_chart(fig)
    
    st.info("Recommendation: **Buy Now**! Prices are trending upwards.")
