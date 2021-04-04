from bitarray.util import urandom

class BinaryFabric:
  
  def __init__(self, n):
    self.n = n
  
  def generatePopulation(self, N):
    return [urandom(self.n) for _ in range(N)]
