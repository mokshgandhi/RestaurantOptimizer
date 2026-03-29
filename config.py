# config.py

INGREDIENTS = {
    "cheese": {"cost": 50, "shelf_life": 5},
    "tomato": {"cost": 20, "shelf_life": 3},
    "paneer": {"cost": 60, "shelf_life": 4}
}

RECIPES = {
    "pasta": {"cheese": 100, "tomato": 150},
    "pizza": {"cheese": 120, "tomato": 100}
}

SUBSTITUTES = {
    "cheese": ["paneer"],
    "paneer": ["cheese"]
}
