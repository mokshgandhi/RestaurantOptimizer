# data_simulation.py

import pandas as pd
import numpy as np

def generate_data(days=30):
    np.random.seed(42)
    data = []
    
    for i in range(days):
        day = i % 7
        base = 50 + 10 * np.sin(i / 3)
        weekend_boost = 30 if day in [5,6] else 0
        
        orders = int(base + weekend_boost + np.random.randint(-10, 10))
        
        weather = np.random.choice(["hot", "moderate", "rainy"])
        
        data.append({
            "day": day,
            "orders": max(10, orders),
            "weather": weather
        })
    
    return pd.DataFrame(data)
