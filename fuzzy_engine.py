# fuzzy_engine.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def build_fuzzy_system():
    
    demand = ctrl.Antecedent(np.arange(0, 151, 1), 'demand')
    stock = ctrl.Antecedent(np.arange(0, 501, 1), 'stock')
    freshness = ctrl.Antecedent(np.arange(0, 11, 1), 'freshness')

    reorder = ctrl.Consequent(np.arange(0, 501, 1), 'reorder')
    adjustment = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'adjustment')

    # Memberships
    demand['low'] = fuzz.trimf(demand.universe, [0, 0, 50])
    demand['medium'] = fuzz.trimf(demand.universe, [30, 75, 120])
    demand['high'] = fuzz.trimf(demand.universe, [100, 150, 150])

    stock['low'] = fuzz.trimf(stock.universe, [0, 0, 150])
    stock['adequate'] = fuzz.trimf(stock.universe, [100, 250, 400])
    stock['high'] = fuzz.trimf(stock.universe, [300, 500, 500])

    freshness['spoiling'] = fuzz.trimf(freshness.universe, [0, 0, 4])
    freshness['fresh'] = fuzz.trimf(freshness.universe, [3, 10, 10])

    reorder['low'] = fuzz.trimf(reorder.universe, [0, 0, 150])
    reorder['medium'] = fuzz.trimf(reorder.universe, [100, 250, 400])
    reorder['high'] = fuzz.trimf(reorder.universe, [300, 500, 500])

    adjustment['low'] = fuzz.trimf(adjustment.universe, [0, 0, 0.3])
    adjustment['moderate'] = fuzz.trimf(adjustment.universe, [0.2, 0.5, 0.8])
    adjustment['high'] = fuzz.trimf(adjustment.universe, [0.7, 1.0, 1.0])

    # Rules (expanded)
    rules = [
        ctrl.Rule(demand['high'] & stock['low'], reorder['high']),
        ctrl.Rule(demand['medium'] & stock['low'], reorder['medium']),
        ctrl.Rule(demand['low'] & stock['high'], reorder['low']),
        ctrl.Rule(freshness['spoiling'], adjustment['high']),
        ctrl.Rule(stock['low'] & demand['high'], adjustment['moderate']),
        ctrl.Rule(stock['adequate'], adjustment['low']),
        ctrl.Rule(demand['high'] & freshness['fresh'], reorder['high']),
        ctrl.Rule(demand['low'] & freshness['spoiling'], adjustment['high'])
    ]

    system = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(system)
