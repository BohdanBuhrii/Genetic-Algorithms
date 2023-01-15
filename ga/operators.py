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


class TwoPointOperator:
  
  def __init__(self, n):
    self.n = n

  def mutate(self, x):
    index = np.random.randint(self.n)

    mutated = x.copy()
    mutated[index] = not mutated[index]

    return mutated

  def crossbreed(self, mom, dad):
    index = sorted([np.random.randint(self.n), np.random.randint(self.n)])

    return (mom[:index[0]] + dad[index[0]:index[1]] + mom[index[1]:], dad[:index[0]] + mom[index[0]:index[1]] + dad[index[1]:])