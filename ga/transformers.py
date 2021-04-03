class BinaryTransformer:

  def transform(self, x, x_int, n):
    d = 0
    for i, b in enumerate(x):
      if b:
        d += 2 ** i

    return (x_int[1] - x_int[0]) / (2 ** n - 1) * d + x_int[0]


class SingleDimentionTransformer(BinaryTransformer):

  def __init__(self, n, x_int):
    self.n = n
    self.x_int = x_int

  def transform(self, x):
    return BinaryTransformer.transform(self, x, self.x_int, self.n)


class MultiDimentionTransformer(BinaryTransformer):

  def __init__(self, n_xs: list, x_ints: list):
    self.n_xs = n_xs
    self.x_ints = x_ints

  def transform(self, x):
    xs = []
    pointer = 0

    for n_xi, x_inti in zip(self.n_xs, self.x_ints):
      xs.append(BinaryTransformer.transform(
        self,
        x[pointer:pointer+n_xi],
        x_inti,
        n_xi))

      pointer += n_xi

    return xs
