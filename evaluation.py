# evaluation.py

def compute_waste(stock, freshness):
    waste = 0
    for ing in stock:
        if freshness < 3:
            waste += stock[ing] * 0.3
    return waste

def cost(stock, prices):
    return sum(stock[i] * prices[i]['cost'] for i in stock)
