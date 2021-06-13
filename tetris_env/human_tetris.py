from bot.feature_extraction import extract_features
from tetris_env import tetris
from tetris_env.piece_factory import PieceFactory


class HumanTetris:
    """
    Let a human player plays the Tetris environment
    """
    def __init__(self, height, width):
        """
        :param height: Height of the board
        :param width: Width of the board
        """
        self.width = width
        self.board = tetris.create_board(height, width)
        self.pf = PieceFactory(width)

    def play(self, print_features=True):
        """
        Game loop
        """
        tetris.pretty_print_board(self.board)
        while True:
            # Insert data as "piece_number num_of_rotations offset from the left"
            pid, rid, col_offset = map(int, input().split())
            # Retrieves the piece in its relevant rotation
            piece = self.pf.pieces[pid][rid % len(self.pf.pieces[pid])]
            # If you go over the maximum offset, it will set you to the maximum
            if col_offset + len(piece[-1]) > self.width:
                col_offset = self.width - len(piece[-1])
            if tetris.drop_piece(piece, col_offset, self.board):
                print('GAME OVER')
                break
            tetris.pretty_print_board(self.board)
            if print_features:
                print(extract_features(self.board))
