import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_flight_data(num_samples=5000):
    routes = ['JFK-LHR', 'LHR-JFK', 'SFO-JFK', 'JFK-SFO', 'LHR-DXB', 'DXB-LHR']
    airlines = ['YieldWings', 'SkyHigh', 'Oceanic']
    
    data = []
    
    start_date = datetime.now()
    
    print("Generating synthetic flight data...")
    
    for _ in range(num_samples):
        route = random.choice(routes)
        airline = 'YieldWings'
        
        # Flight Date within next 3 months
        days_ahead = random.randint(1, 90)
        flight_date = start_date + timedelta(days=days_ahead)
        
        # Base Price based on distance (simplified by route)
        base_price = 500 if 'LHR' in route else 300
        if 'DXB' in route: base_price = 700
            
        # Time factor: closer to date -> higher price
        time_factor = 1 + (1 / (days_ahead + 1)) * 2  # Price spikes last minute
        
        # Seasonality/Demand factor (Randomized simplified model)
        is_weekend = flight_date.weekday() >= 5
        seasonality_factor = 1.2 if is_weekend else 1.0
        
        # Competitor Price (random noise around base)
        competitor_price = base_price * time_factor * seasonality_factor * random.uniform(0.9, 1.1)
        
        # Our Price (random strategy for training data)
        price = base_price * time_factor * seasonality_factor * random.uniform(0.8, 1.2)
        
        # Demand Generation (Higher price -> Lower demand)
        # Demand = Base Demand * (Compatitor Price / Our Price) * Seasonality
        base_demand = 150 # Average seats
        price_ratio = competitor_price / price
        demand_factor = price_ratio ** 2 # Elasticity
        
        demand = int(base_demand * demand_factor * random.uniform(0.9, 1.1))
        # Cap demand at capacity (e.g. 200 seats)
        capacity = 200
        bookings = min(demand, capacity)
        
        sample = {
            'route': route,
            'date': flight_date.strftime('%Y-%m-%d'),
            'day_of_week': flight_date.weekday(), # 0=Mon, 6=Sun
            'days_prior': days_ahead,
            'competitor_price': round(competitor_price, 2),
            'price': round(price, 2),
            'bookings': bookings,
            'capacity': capacity,
            'is_weekend': int(is_weekend)
        }
        data.append(sample)
        
    df = pd.DataFrame(data)
    print(f"Generated {len(df)} samples.")
    return df

if __name__ == "__main__":
    df = generate_flight_data()
    # Ensure data directory exists
    import os
    os.makedirs('data', exist_ok=True)
    
    output_path = os.path.join('data', 'flight_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
