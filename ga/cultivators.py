import numpy as np
import random

class TournamentCultivator:

  def __init__(self, N_t, p_mutate, p_cross, operator, evaluator):
    self.N_t = N_t
    self.p_mutate = p_mutate
    self.p_cross = p_cross
    self.operator = operator
    self.evaluator = evaluator

  def cultivateFrom(self, population: list):
    new_population = []
    N = len(population)

    for _ in range(N//2):

      mom = self.roundOfTournament(population)
      dad = self.roundOfTournament(population)

      if self.shouldMutate():
        mom = self.operator.mutate(mom)
        dad = self.operator.mutate(dad)

      if self.shouldCross():
        mom, dad = self.operator.crossbreed(mom, dad)

      new_population.append(mom)
      new_population.append(dad)

    return new_population

  def roundOfTournament(self, population: list):
    participants = random.sample(population, self.N_t)

    winner, _ = self.evaluator.bestOfPopulationt(participants)

    return winner

  def shouldMutate(self):
    return np.random.choice([True, False], p=[self.p_mutate, 1 - self.p_mutate])

  def shouldCross(self):
    return np.random.choice([True, False], p=[self.p_cross, 1 - self.p_cross])


class EliteCultivator:
  
  def __init__(self, cultivator, p_elite):
    self.cultivator = cultivator
    self.evaluator = cultivator.evaluator
    self.p_elite = p_elite
    
  def cultivateFrom(self, population: list):
    N = len(population)
    elite_size = int(N * self.p_elite)
    
    elite, others = self.separateElite(population, elite_size)
    
    new_population = self.cultivator.cultivateFrom(others)
    
    new_population.extend(elite)
    
    return new_population
    
  def separateElite(self, population, n):
    scores = [self.evaluator.evaluate(x) for x in population]

    ranking = np.argsort(scores)

    elite_indexes = ranking[:n]
    others_indexes = ranking[n:]

    return [population[i] for i in elite_indexes], [population[i] for i in others_indexes]
