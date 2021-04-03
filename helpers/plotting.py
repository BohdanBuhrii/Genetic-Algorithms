import numpy as np
import matplotlib.pyplot as plt

def plotContour(f, x1_int, x2_int, argmin=None, mesh_n=50):
  x = np.linspace(x1_int[0], x1_int[1], mesh_n)
  y = np.linspace(x2_int[0], x2_int[1], mesh_n)

  X, Y = np.meshgrid(x, y)
  Z = f(X, Y)

  fig = plt.figure(figsize=(7, 4))
  ax = fig.add_subplot()

  cs = ax.contourf(X, Y, Z)

  fig.colorbar(cs)

  if(argmin != None):
    ax.plot([argmin[0]], [argmin[1]], 'r*', label=r'$f(x) = min $')

  plt.show()

def plotScores(scores):
  plt.plot(scores)