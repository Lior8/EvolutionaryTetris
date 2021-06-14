import multiprocessing
import multiprocessing as mp

from evolution.evolution import EvolutionEnv


class ParallelEvolutionEnv(EvolutionEnv):
    def __init__(self, pop_size=100, generations=40, p_mutation=0.2, p_crossover=1, k_tournament=3, g_size=7,
                 init_low_lim=-100, init_high_lim=100, games_per_fitness=5, board_height=12, board_width=6,
                 with_logging=True, with_printing=True, num_cores=-1):
        super().__init__(pop_size, generations, p_mutation, p_crossover, k_tournament, g_size, init_low_lim,
                         init_high_lim, games_per_fitness, board_height, board_width, with_logging, with_printing)
        self.num_cores = multiprocessing.cpu_count() if num_cores == -1 else num_cores

    def calc_pop_fitness(self):
        results = mp.Pool(processes=self.num_cores).map(self.calc_fitness, self.population)
        for i in range(self.pop_size):
            self.logger.debug(f'G: {self.population[i]}')
            for j in range(self.games_per_fitness):
                self.logger.debug(f'T{j}: {results[i][j]}')
        self.fitnesses = [sum(result) / self.games_per_fitness for result in results]

    def calc_fitness(self, g):
        scores = []
        for i in range(self.games_per_fitness):
            game_score = self.play_game(g)
            scores.append(game_score)
        if self.with_printing:
            print(f'{["%.2f" % elem for elem in g]} finished with {sum(scores) / self.games_per_fitness}')
        return scores
