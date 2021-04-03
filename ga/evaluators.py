import numpy as np
from abc import ABC, abstractmethod

class SimpleEvaluator(ABC):

  @abstractmethod
  def evaluate(self, x):
    pass

  def bestOfPopulationt(self, population):
    scores = [self.evaluate(x) for x in population]

    best_index = np.argmin(scores)

    return population[best_index], scores[best_index]


class MinimumEvaluator(SimpleEvaluator):
  def __init__(self, f, transformer):
    self.f = f
    self.transformer = transformer

  def evaluate(self, x):
    return self.f(self.transformer.transform(x))
