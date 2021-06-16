import matplotlib.pyplot as plt
import numpy as np


def log_to_data(file_path):
    """
    Converts a log file into a a list representing the generations.
    :param file_path: The path to the log file
    :return: A list of lists of lists. Each list is a generation which hold lists which are the games of each individual
    in that generation
    """
    scores = []
    with open(file_path, 'r') as log:
        for line in log:
            if line.startswith('T'):
                scores[-1][-1].append(int(line.split(':')[1].strip()))
            elif line.startswith('G:'):
                scores[-1].append([])
            elif line.startswith('Generation'):
                scores.append([])

    return scores


def generate_graph_from_scores(scores, yticks_distance=4000, increase_ylim=False):
    """
    A function which takes the list created from log_to_data() and generates a graph of the mean fitness, the best
    individual's fitness, and the best game as a function of the generations
    :param scores: The list of lists of lists from log_to_data()
    :param yticks_distance: The distance between each y-axis tick (starts at 0)
    :param increase_ylim: Sometimes plt cuts the ticks too short with the current implementation. If it is set to True,
    it will add another tick above the last one plt placed
    """
    mean_score_per_gen = [np.mean(gen_scores) for gen_scores in scores]
    max_score_per_gen = []
    best_game_per_gen = []

    for gen in scores:
        max_score_per_gen.append(max([np.mean(indv) for indv in gen]))
        best_game_per_gen.append(max([max(indv) for indv in gen]))
    xs = list(range(len(scores)))
    plt.plot(xs, mean_score_per_gen)
    plt.plot(xs, max_score_per_gen)
    plt.plot(xs, best_game_per_gen)
    plt.yticks(
        list(range(0, int(max(list(plt.yticks()[0]))) + (yticks_distance if increase_ylim else 0), yticks_distance)))
    plt.xticks(list(plt.xticks()[0]) + [len(scores) - 1])
    plt.axis([0, len(xs) - 1, 0, int(max(list(plt.yticks()[0])))])
    plt.grid()
    plt.xlabel('Generations')
    plt.ylabel('Tetrominoes Dropped')
    plt.legend(['Avg. of all games', 'Avg. of best individual', 'Best game played'])
    plt.show()


def generate_graph(file_path, yticks_distance, increase_ylim=False):
    """
    An interface for easy access to the other functions
    :param file_path: The path to the log file
    :param yticks_distance: The distance between each y-axis tick (starts at 0)
    :param increase_ylim: Sometimes plt cuts the ticks too short with the current implementation. If it is set to True,
    it will add another tick above the last one plt placed.
    """
    generate_graph_from_scores(log_to_data(file_path), yticks_distance, increase_ylim)
