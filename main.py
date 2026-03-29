# main.py

from data_simulation import generate_data
from demand_model import train_model, predict_demand
from fuzzy_engine import build_fuzzy_system
from recipe_engine import substitute_ingredients, apply_fuzzy_adjustment
from aco_optimizer import ACORecipeOptimizer
from config import RECIPES, INGREDIENTS

# Step 1: Data
df = generate_data()
model = train_model(df)

# Step 2: Fuzzy
fuzzy = build_fuzzy_system()

# Step 3: Inventory
stock = {"cheese": 150, "tomato": 200, "paneer": 80}

# Step 4: Demand Prediction
day = 5
weather = "hot"
demand = predict_demand(model, day, weather)

# Step 5: Fuzzy Decision
fuzzy.input['demand'] = demand
fuzzy.input['stock'] = sum(stock.values())
fuzzy.input['freshness'] = 3
fuzzy.compute()

reorder = fuzzy.output['reorder']
adjustment = fuzzy.output['adjustment']

# Step 6: Recipe Processing
recipe = RECIPES['pasta']
recipe = substitute_ingredients(recipe, stock)
recipe = apply_fuzzy_adjustment(recipe, adjustment)

# Step 7: ACO Optimization
cost_map = {k: INGREDIENTS[k]['cost'] for k in INGREDIENTS}

aco = ACORecipeOptimizer(list(recipe.keys()), cost_map)
optimized_recipe, score = aco.optimize(recipe, stock)

# Output
print("\n=== FINAL OUTPUT ===")
print("Predicted Demand:", demand)
print("Fuzzy Reorder:", reorder)
print("Fuzzy Adjustment:", adjustment)
print("Optimized Recipe:", optimized_recipe)
print("Optimization Score:", score)
