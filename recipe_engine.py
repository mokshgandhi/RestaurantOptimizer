# recipe_engine.py

from config import SUBSTITUTES

def substitute_ingredients(recipe, stock):
    new_recipe = recipe.copy()
    
    for ing in recipe:
        if stock.get(ing, 0) < 20:
            if ing in SUBSTITUTES:
                sub = SUBSTITUTES[ing][0]
                new_recipe[sub] = new_recipe.pop(ing)
    
    return new_recipe


def apply_fuzzy_adjustment(recipe, adjustment):
    adjusted = {}
    for ing, qty in recipe.items():
        adjusted[ing] = max(10, qty * (1 - adjustment * 0.4))
    return adjusted
