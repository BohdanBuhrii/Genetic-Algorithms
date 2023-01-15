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


class SmartWieghtCultivator(TournamentCultivator):

  def __init__(self, N_t, p_mutate, p_cross, operator, evaluator, selection_pressure):
    self.selection_pressure = selection_pressure

    TournamentCultivator.__init__(
        self, N_t, p_mutate, p_cross, operator, evaluator)

  def cultivateFrom(self, population: list):
    N = len(population)
    
    assert self.selection_pressure <= 2/(N*(N - 1)), 'Selection pressure is very high'
    
    scores = [self.evaluator.evaluate(x) for x in population]
    self.ranking_list = np.argsort(scores)
    
    ranking = np.arange(N)
    q = self.selection_pressure*(N-1)/2 + 1/N

    self.probs = q - ranking * self.selection_pressure
    
    return TournamentCultivator.cultivateFrom(self, population)

  def roundOfTournament(self, population: list):
    participants_indexes = np.random.choice(self.ranking_list, size=self.N_t, p=self.probs)
    participants = [population[i] for i in participants_indexes]

    winner, _ = self.evaluator.bestOfPopulationt(participants)

    return winner

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
    
  def separateElite(self, population, size):
    scores = [self.evaluator.evaluate(x) for x in population]

    ranking = np.argsort(scores)

    elite_indexes = ranking[:size]
    others_indexes = ranking[size:]

    return [population[i] for i in elite_indexes], [population[i] for i in others_indexes]

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