# app.py

from data_simulation import generate_data
from demand_model import train_model, predict_demand
from fuzzy_engine import build_fuzzy_system
from recipe_engine import adjust_recipe, substitute_ingredients
from config import RECIPES, INGREDIENTS

# Generate data
df = generate_data()

# Train ML model
model = train_model(df)

# Fuzzy system
fuzzy = build_fuzzy_system()

# Initial stock
stock = {"cheese": 200, "tomato": 200, "paneer": 100}

# Simulate one day
day = 6
weather = "hot"

demand = predict_demand(model, day, weather)

fuzzy.input['demand'] = demand
fuzzy.input['stock'] = sum(stock.values())
fuzzy.input['freshness'] = 3
fuzzy.compute()

reorder = fuzzy.output['reorder']
adjustment = fuzzy.output['adjustment']

recipe = RECIPES['pasta']

recipe = substitute_ingredients(recipe, stock)
adjusted_recipe = adjust_recipe(recipe, adjustment)

print("Predicted Demand:", demand)
print("Reorder:", reorder)
print("Adjustment:", adjustment)
print("Adjusted Recipe:", adjusted_recipe)
