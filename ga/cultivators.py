import numpy as np
import random

class RandomCultivator:
  
  def __init__(self, selector, operator, p_mutate):
    self.selector = selector
    self.operator = operator
    self.p_mutate = p_mutate
    
  def cultivateFrom(self, population: list):
    new_population = []
    N = len(population)

    for _ in range(N//2):
      mom, dad = self.selector.select_pair(population)

      mom, dad = self.operator.crossbreed(mom, dad)

      if self.shouldMutate():
        mom = self.operator.mutate(mom)
        dad = self.operator.mutate(dad)

      new_population.append(mom)
      new_population.append(dad)

    new_population.extend(population)

    indexes = random.sample(range(len(new_population)), N)

    return [new_population[i] for i in indexes]
    

  def shouldMutate(self):
    return np.random.choice([True, False], p=[self.p_mutate, 1 - self.p_mutate])



class TotalEliteCultivator:
  
  def __init__(self, selector, operator, evaluator, p_mutate):
    self.selector = selector
    self.operator = operator
    self.evaluator = evaluator
    self.p_mutate = p_mutate
    
  def cultivateFrom(self, population: list):
    new_population = []
    N = len(population)

    for _ in range(N//2):
      mom, dad = self.selector.select_pair(population)

      mom, dad = self.operator.crossbreed(mom, dad)

      if self.shouldMutate():
        mom = self.operator.mutate(mom)
        dad = self.operator.mutate(dad)

      new_population.append(mom)
      new_population.append(dad)

    new_population.extend(population)

    return sorted(new_population, key = lambda x: self.evaluator.evaluate(x))[:N]


  def shouldMutate(self):
    return np.random.choice([True, False], p=[self.p_mutate, 1 - self.p_mutate])



class ExpulsionCultivator:
  
  def __init__(self, selector, operator, evaluator, p_mutate):
    self.selector = selector
    self.operator = operator
    self.evaluator = evaluator
    self.p_mutate = p_mutate
    
  def cultivateFrom(self, population: list):
    new_population = []
    N = len(population)

    for _ in range(N//2):
      mom, dad = self.selector.select_pair(population)

      mom, dad = self.operator.crossbreed(mom, dad)

      if self.shouldMutate():
        mom = self.operator.mutate(mom)
        dad = self.operator.mutate(dad)

      new_population.append(mom)
      new_population.append(dad)

    new_population.extend(population)

    sorted_p = sorted(new_population, key = lambda x: self.evaluator.evaluate(x))
    distinct_p = sorted_p[:1]

    for ind in sorted_p:
      if ind != distinct_p[-1]:
        distinct_p.append(ind)
      
    return distinct_p[:N]


  def shouldMutate(self):
    return np.random.choice([True, False], p=[self.p_mutate, 1 - self.p_mutate])