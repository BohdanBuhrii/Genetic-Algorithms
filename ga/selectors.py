import random
import numpy as np

class InbreedingSelector:
  def __init__(self, distance_metric):
    self.distance = distance_metric

  def select_pair(self, population):
    mom = population[np.random.randint(len(population))]
    dad = sorted(population, key = lambda x: self.distance(x, mom))[1]

    return mom, dad


class OutbreedingSelector:
  def __init__(self, distance_metric):
    self.distance = distance_metric

  def select_pair(self, population):
    mom = population[np.random.randint(len(population))]
    dad = sorted(population, key = lambda x: self.distance(x, mom))[-1]

    return mom, dad

class PanmixiaSelector:
  def select_pair(self, population):
    i1, i2 = random.sample(range(len(population)), 2)

    return population[i1], population[i2]

class SelectiveSelector:
  def __init__(self, evaluator):
    self.evaluator = evaluator

  def select_pair(self, population):
    N = len(population)
    scores = np.array([self.evaluator.evaluate(x) for x in population])
    mean = np.mean(scores)

    parents = []
    for i in range(N):
      if scores[i] >= mean:
        parents.append(population[i])

    i1, i2 = random.sample(range(len(parents)), 2)

    return parents[i1], parents[i2]
