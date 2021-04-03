import numpy as np

class BinaryOperator:
  
  def __init__(self, n):
    self.n = n

  def mutate(self, x):
    index = np.random.randint(self.n)

    mutated = x.copy()
    mutated[index] = not mutated[index]

    return mutated

  def crossbreed(self, mom, dad):
    index = np.random.randint(self.n)

    return (mom[:index] + dad[index:], dad[:index] + mom[index:])
