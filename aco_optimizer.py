# aco_optimizer.py

import numpy as np
import random

class ACORecipeOptimizer:
    def __init__(self, ingredients, cost_map, n_ants=10, n_iter=20):
        self.ingredients = ingredients
        self.cost_map = cost_map
        self.n_ants = n_ants
        self.n_iter = n_iter
        self.pheromone = {i: 1.0 for i in ingredients}

    def fitness(self, solution, stock):
        cost = sum(solution[i] * self.cost_map[i] for i in solution)
        
        penalty = 0
        for i in solution:
            if solution[i] > stock.get(i, 0):
                penalty += 100
        
        return cost + penalty

    def generate_solution(self, base_recipe):
        solution = {}
        for ing in base_recipe:
            variation = random.uniform(0.7, 1.3)
            solution[ing] = base_recipe[ing] * variation
        return solution

    def update_pheromone(self, solutions):
        for sol, score in solutions:
            for ing in sol:
                self.pheromone[ing] += 1.0 / (score + 1)

    def optimize(self, base_recipe, stock):
        best_solution = None
        best_score = float('inf')

        for _ in range(self.n_iter):
            solutions = []

            for _ in range(self.n_ants):
                sol = self.generate_solution(base_recipe)
                score = self.fitness(sol, stock)
                solutions.append((sol, score))

                if score < best_score:
                    best_solution = sol
                    best_score = score

            self.update_pheromone(solutions)

        return best_solution, best_score
