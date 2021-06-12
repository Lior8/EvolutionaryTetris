class PieceFactory:
    def __init__(self, width):
        """
        Class which handles creation, rotation, and initial positions of pieces.
        :param width: Width of the board
        """
        self.width = width
        self.num_pieces = 7
        self.pieces = [
            [[[1], [1], [1], [1]], [[1, 1, 1, 1]]],  # I
            [[[2, 2], [2, 2]]],  # O
            [[[3, 3, 3], [0, 3, 0]], [[0, 3], [3, 3], [0, 3]], [[0, 3, 0], [3, 3, 3]], [[3, 0], [3, 3], [3, 0]]],  # T
            [[[0, 4, 4], [4, 4, 0]], [[4, 0], [4, 4], [0, 4]]],  # S
            [[[5, 5, 0], [0, 5, 5]], [[0, 5], [5, 5], [5, 0]]],  # Z
            [[[0, 6], [0, 6], [6, 6]], [[6, 0, 0], [6, 6, 6]], [[6, 6], [6, 0], [6, 0]], [[6, 6, 6], [0, 0, 6]]],  # J
            [[[7, 0], [7, 0], [7, 7]], [[7, 7, 7], [7, 0, 0]], [[7, 7], [0, 7], [0, 7]], [[0, 0, 7], [7, 7, 7]]]  # L
        ]

        # Height is defined as the maximum height of any column. Width is the maximum width of any row
        self.pieces_sizes = [
            [(4, 1), (1, 4)],  # I
            [(2, 2)],  # O
            [(2, 3), (3, 2), (2, 3), (3, 2)],  # T
            [(2, 3), (3, 2)],  # S
            [(2, 3), (3, 2)],  # Z
            [(3, 2), (2, 3), (3, 2), (2, 3)],  # J
            [(3, 2), (2, 3), (3, 2), (2, 3)]  # L
        ]

    def print_piece(self, pid, rotation):
        """
        Prints a piece
        :param pid: Piece ID
        :param rotation: Rotation number
        :return:
        """
        piece = self.pieces[pid][rotation]
        for i in range(len(piece)):
            print(''.join(map(str, piece[i])))

    def get_rotations_and_offset_limit(self, pid):
        """
        Calculates all possible places to drop the from.
        :param pid: Piece ID
        :return: A list of tuples. Each tuple holds the piece with its rotation, and the limit for its offset (from the
        left side). The last legal position is in limit - 1 and not in limit.
        """
        return [(self.pieces[pid][rid], self.width - self.pieces_sizes[pid][rid][1] + 1) for rid in
                range(len(self.pieces[pid]))]

    def calculate_piece_size(self, piece):
        """
        Calculates the size of the piece.
        :param piece: The piece itself
        :return: The height and width of the piece
        """
        return len(piece), len(piece[-1])
