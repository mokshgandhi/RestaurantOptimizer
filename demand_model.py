# demand_model.py

from sklearn.ensemble import RandomForestRegressor
import pandas as pd

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
    return model.predict([[day, weather_map[weather]]])[0]
