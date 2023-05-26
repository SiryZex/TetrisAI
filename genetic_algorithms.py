from tetris import Tetris
from neural_network import NeuralNetwork
from random import randrange, randint
import random
import sys
from settings import *

def __generate_name():
	current_name = 1
	while True:
		yield current_name
		current_name += 1
_generate_name = __generate_name()

# chromosome = heuristics dictionary
class Chromosome(object):
	def __init__(self, heuristics):
		self.name = next(_generate_name)
		self.heuristics = heuristics
		self.total_fitness = 0
		self.games = 0

	def avg_fitness(self):
		return self.total_fitness / self.games

class GeneticAlgorithms(object):
	def __init__(self):
		self.app = Tetris(self)
		self.neural_network = NeuralNetwork(self.app)
		self.app.neural_network = self.neural_network
		self.population = [self.random_chromosome() for _ in range(POPULATION_SIZE)]
		self.current_chromosome = 0
		self.current_generation = 1
		self.neural_network.heuristics = self.population[self.current_chromosome].heuristics

	def run(self):
		self.app.run()

	def next_ai(self):
		self.current_chromosome += 1
		if self.current_chromosome >= POPULATION_SIZE:
			self.current_chromosome = 0
			self.next_generation()
		self.neural_network.heuristics = self.population[self.current_chromosome].heuristics
	
	def game_over(self, score):
		chromosome = self.population[self.current_chromosome]
		chromosome.games += 1
		chromosome.total_fitness += score
		if chromosome.games % GAMES_TO_AVG == 0:
			self.next_ai()
		self.app.start_game()

	def population_converged(self):
		t = CONVERGED_THRESHOLD
		pop = self.population
		return all(all(pop[0].heuristics[f]-t < w < pop[0].heuristics[f]+t for f, w in c.heuristics.items()) for c in pop)

	def next_generation(self):
		if self.population_converged():
			sys.exit()
		self.current_generation += 1
		new_population = self.selection(SURVIVORS_PER_GENERATION, SELECTION_METHOD)
		for _ in range(NEWBORNS_PER_GENERATION):
			parents = self.selection(2, SELECTION_METHOD)
			new_population.append(self.crossover(parents[0], parents[1], CROSSOVER_METHOD))
		for _ in range(MUTATION_PASSES):
			for chromosome in new_population:
				self.mutation(chromosome, MUTATION_RATE / MUTATION_PASSES)
		assert len(new_population) == len(self.population)
		self.population = new_population

	def selection(self, num_selected, method):
		def roulette(population):
			total_fitness = sum([c.avg_fitness() for c in population])
			winner = randrange(int(total_fitness))
			fitness_so_far = 0
			for chromosome in population:
				fitness_so_far += chromosome.avg_fitness()
				if fitness_so_far > winner:
					return chromosome
		
		if method == SelectionMethod.roulette:
			survivors = []
			for _ in range(num_selected):
				survivors.append(roulette([c for c in self.population if c not in survivors]))
			return survivors

		raise ValueError('SelectionMethod %s not implemented' % method)

	def crossover(self, c1, c2, method):
		def random_attributes():
			heuristics = {}
			for fun, _ in c1.heuristics.items():
				heuristics[fun] = random.choice((c1, c2)).heuristics[fun]
			return Chromosome(heuristics)

		def average_attributes():
			heuristics = {}
			for fun, _ in c1.heuristics.items():
				heuristics[fun] = (c1.heuristics[fun] + c2.heuristics[fun]) / 2
			return Chromosome(heuristics)			

		if method == CrossoverMethod.random_attributes:
			return random_attributes()
		if method == CrossoverMethod.average_attributes:
			return average_attributes()
		raise ValueError('CrossoverMethod %s not implemented' % method)

	def mutation(self, chromosome, mutation_rate):
		if randint(0, int(mutation_rate)) == 0:
			h = chromosome.heuristics
			h[random.choice(list(h.keys()))] = randrange(-1000, 1000)
			print(chromosome.name, "MUTATED")

	def random_chromosome(self):
		return Chromosome({fun: randrange(-1000, 1000) for fun, weight in self.neural_network.heuristics.items()})

if __name__ == "__main__":	
	GeneticAlgorithms().run()
	