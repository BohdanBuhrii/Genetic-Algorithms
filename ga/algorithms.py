import numpy as np

class SimpleGA:
  def __init__(self, fabric, evaluator, transformer, cultivator):
    self.fabric = fabric
    self.transformer = transformer
    self.evaluator = evaluator
    self.cultivator = cultivator

  def solve(self, N, max_iterations, max_iterations_without_evolution):
    self.solution = None
    self.best_from_populations = []
    self.scores = []

    population = self.fabric.generatePopulation(N)
    iterations_without_evolution = 0

    for i in range(max_iterations):
      best, population_score = self.evaluator.bestOfPopulationt(population)

      if self.scores != [] and np.abs(self.scores[-1] - population_score) < 1e-5:
        iterations_without_evolution += 1
      else:
        iterations_without_evolution = 0

      if iterations_without_evolution >= max_iterations_without_evolution:
        break

      self.best_from_populations.append(best)
      self.scores.append(population_score)

      population = self.cultivator.cultivateFrom(population)

      self.showProgress(i, max_iterations)

    all_time_best, best_score = self.evaluator.bestOfPopulationt(self.best_from_populations)

    self.solution = self.transformer.transform(all_time_best)

    return self.solution, best_score
  
  def showProgress(self, i, max_iterations):
    p = int(i/max_iterations * 100)
    
    if p % 10 == 0:
      print(str(p)+'%')

class KatGA:
  def __init__(self, fabric, evaluator, transformer, cultivator):
    self.fabric = fabric
    self.transformer = transformer
    self.evaluator = evaluator
    self.cultivator = cultivator
   

  def solve(self, N, max_iterations, epsilon, delta):

    self.solution = None
    self.best_from_populations = []
    self.scores = []

    population = self.fabric.generatePopulation(N)
    iterations_without_evolution = 0
    for i in range(max_iterations):
      best, population_score = self.evaluator.bestOfPopulationt(population)

      # if self.scores != [] and np.abs(self.scores[-1] - population_score) < 1e-5:
      #   iterations_without_evolution += 1
      # else:
      #   iterations_without_evolution = 0

      # if iterations_without_evolution >= 10:
      #   break

      # epsilon stop criteria - distance between members of the populatio
      if self.population_spread(population) < epsilon:
        break

      # delta stop criteria - distance between average population scores
      if self.scores != [] and np.abs(self.scores[-1] - population_score) < delta:
        break

      self.best_from_populations.append(best)
      self.scores.append(population_score)

      population = self.cultivator.cultivateFrom(population)

      self.showProgress(i, max_iterations)

    all_time_best, _ = self.evaluator.bestOfPopulationt(self.best_from_populations)

    self.solution = self.transformer.transform(all_time_best)

    return self.solution, self.evaluator.evaluate(all_time_best)
  
  def showProgress(self, i, max_iterations):
    p = int(i/max_iterations * 100)
    
    if p % 10 == 0:
      print(str(p)+'%')

  def population_spread(self, population):
    individuals = np.array([self.transformer.transform(i) for i in population])

    return self.distND(individuals)

  # finds maximum distance between individuals in the population 
  def distND(self, p):
    dist = 0
    for k in p:
      for l in p:
        new_dist = np.linalg.norm(k - l)
        if new_dist > dist:
          dist = new_dist
    
    return dist
