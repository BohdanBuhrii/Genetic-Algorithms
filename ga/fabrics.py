from bitarray import bitarray

class BinaryFabric:
  
  def __init__(self, n):
    self.n = n
  
  def generatePopulation(self, N):
    return [bitarray(self.n) for _ in range(N)]
