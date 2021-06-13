import math
import random

from bot.feature_extraction import extract_features
from tetris_env import tetris
from tetris_env.piece_factory import PieceFactory


class TetrisBot:
    """
    A bot which plays tetris given the feature weights
    """
    def __init__(self, height, width, genome):
        """
        :param height: The board's height
        :param width:  The board's width
        :param genome: The weights for the features
        """
        self.height = height
        self.width = width
        self.weights = genome
        self.pf = PieceFactory(width)
        self.genome_len = len(genome)

    def play_game(self, with_print=False):
        """
        Play a single game of Tetris using the weights given to the bot
        :param with_print: Print the board?
        :return: Number of pieces dropped in the game
        """
        pieces_counter = 0
        board = tetris.create_board(self.height, self.width)
        while True:
            curr_pid = random.randint(0, 6)
            pieces_counter += 1
            board, _ = self.find_best_move(board, curr_pid)
            if board is None:
                if with_print:
                    print('GAME OVER')
                break
            if with_print:
                tetris.pretty_print_board(board)
                print('-' * 20)
        return pieces_counter

    def find_best_move(self, board, pid):
        """
        Evaluates the best place and rotation to drop the current piece in the board
        :param board: The game board
        :param pid: Piece ID in range [0,6]
        :return: The game board after dropping the piece in the optimal position and the score of the board
        """
        roas = self.pf.get_rotations_and_offset_limit(pid)
        max_score = - math.inf
        best_board = None
        for (piece, offset_limit) in roas:
            for col_offset in range(offset_limit + 1):
                new_board = tetris.copy_board(board)
                if not tetris.drop_piece(piece, col_offset, new_board):
                    move_score = self.eval_board(new_board)
                    if move_score > max_score:
                        max_score = move_score
                        best_board = new_board
        return best_board, max_score

    def eval_board(self, board):
        """
        Calculates the score of the board
        :param board: The game board
        :return: The board's score
        """
        features = extract_features(board)
        score = 0
        for i in range(self.genome_len):
            score += self.weights[i] * features[i]
        return score
