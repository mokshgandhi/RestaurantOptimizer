# inventory_engine.py

def update_inventory(stock, usage, reorder):
    new_stock = stock.copy()
    
    for ing in usage:
        new_stock[ing] = max(0, stock.get(ing, 0) - usage[ing] + reorder/10)
    
    return new_stock
