# demand_model.py

from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np

def preprocess(df):
    df = df.copy()
    df['weather'] = df['weather'].map({
        "hot": 2,
        "moderate": 1,
        "rainy": 0
    })
    return df

def train_model(df):
    df = preprocess(df)
    
    X = df[['day', 'weather']]
    y = df['orders']
    
    model = RandomForestRegressor()
    model.fit(X, y)
    
    return model

def predict_demand(model, day, weather):
    weather_map = {"hot": 2, "moderate": 1, "rainy": 0}
    
    # Convert input to proper numpy format
    input_data = np.array([[day, weather_map[weather]]])
    
    prediction = model.predict(input_data)
    
    # Ensure scalar output
    return float(prediction[0])
