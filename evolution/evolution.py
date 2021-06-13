import math
import random


class EvolutionEnv:
    """
    Environment for the evolutionary algorithm
    """

    def __init__(self, pop_size=100, generations=30, p_mutation=0.2, p_crossover=1, k_tournament=3, g_size=7,
                 init_low_lim=-100, init_high_lim=100):
        """
        :param pop_size: Population size
        :param generations: Number of generations
        :param p_mutation: Probability for mutation per value in the gene
        :param p_crossover: Probability for performing crossover
        :param k_tournament: Number of participants in the tournament selection
        :param g_size: Genome size
        :param init_low_lim: Low limit for the random values in the initial population
        :param init_high_lim: High limit for the random values in the initial population
        """
        self.pop_size = pop_size
        self.generations = generations
        self.p_mutation = p_mutation
        self.p_crossover = p_crossover
        self.k = k_tournament
        self.g_size = g_size
        self.population = [[random.randint(init_low_lim, init_high_lim) for _ in range(g_size)] for _ in
                           range(pop_size)]
        self.fitnesses = []

    def evolve(self):
        """
        Performs the evolutionary algorithm
        """
        for _ in range(self.generations):
            new_population = []
            for _ in range(self.pop_size // 2):
                self.calc_pop_fitness()
                # Select parents
                p1 = self.tournament()
                p2 = self.tournament()
                # Create children
                c1, c2 = self.crossover(p1, p2)
                # Mutate and add children
                new_population.append(self.mutation(c1))
                new_population.append(self.mutation(c2))
            self.population = new_population
            print(sum(self.fitnesses) / self.pop_size)

    def calc_pop_fitness(self):
        """
        Calculates the fitnesses of the entire population
        """
        self.fitnesses = [self.calc_fitness(indv) for indv in self.population]

    def calc_fitness(self, g):
        """
        Calculates the fitness of a given genome
        :param g: The individual/genome
        :return: The fitness value
        """
        return -sum(g)  # Placeholder function for now

    def tournament(self):
        """
        Tournament selection without replacement (cannot pick same individual twice)
        :return: The winner of the tournament
        """
        max_fitness = - math.inf
        best_indv = None
        for i in random.sample(range(self.pop_size), self.k):
            curr_fitness = self.fitnesses[i]
            if curr_fitness > max_fitness:
                max_fitness = curr_fitness
                best_indv = self.population[i]
        return best_indv

    def crossover(self, g1, g2):
        """
        Performs two-point crossover with probability P. With probability 1-P returns the parents as is
        :param g1: Parent 1
        :param g2: Parent 2
        :return: Two children
        """
        if random.uniform(0, 1) < self.p_crossover:
            i, j = sorted(random.sample(range(1, self.g_size - 1), 2))
            return g1[0:i] + g2[i:j] + g1[j:self.g_size], g2[0:i] + g1[i:j] + g2[j:self.g_size]
        else:
            return g1, g2

    def mutation(self, g):
        """
        Mutates the values in the genome. Each value has probability P to be mutated
        :param g: The genome
        :return: The mutated genome
        """
        for i in range(self.g_size):
            if random.uniform(0, 1) < self.p_mutation:
                g[i] *= random.gauss(1, 0.5)
        return g
