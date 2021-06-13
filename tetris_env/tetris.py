def create_board(height, width):
    """
    Creates the game board filled with zeros. Its height is larger by 4 to be able to draw the pieces above the board
    in the case of collision right at row number 0 by the vertical line (height 4).
    The board looks like this in terms of indexes:
     (0,0)  . . .  (0,W-1)
       .              .
       .              .
       .              .
    (H-1,0) . . . (H-1,W-1)
    This means the lowest line is at row H (and not 0)
    :param height: Height of the board
    :param width: Width of the board
    :return: The game board
    """
    board = []
    for _ in range(height + 4):
        board.append([0] * width)
    return board


def copy_board(board):
    """
    Deep copies a board
    :param board: A game board
    :return: A deep copy of the game board
    """
    return [line[:] for line in board]


def print_board(board, with_hidden_lines=False):
    """
    Prints the game board
    :param board: The game board
    :param with_hidden_lines: Print hidden lines? If there is anything in the hidden lines, it is game over
    """
    for i in range(0 if with_hidden_lines else 4, len(board)):
        print(board[i])


def pretty_print_board(board, with_color=True, with_hidden_lines=False):
    colstart = ['\33[96m', '\33[93m', '\33[95m', '\33[92m', '\33[91m', '\33[94m', '\33[97m']
    for i in range(0 if with_hidden_lines else 4, len(board)):
        for val in board[i]:
            if with_color:
                print(colstart[val - 1] + '\u25A0\33[0m ' if val > 0 else '\u25A1 ', end='')
            else:
                print('\u25A0 ' if val > 0 else '\u25A1 ', end='')
        print()


def drop_piece(piece, col_offset, board):
    """
    Drops the piece from the column offset.
    :param piece: The piece itself (not its PID)
    :param col_offset: The column offset (from the left)
    :param board: The game board
    :return: True if game over, False otherwise
    """
    height = len(board)
    # We start at 4 because the first 4 lines are the hidden lines which are there for preventing from collision
    # detection to crash when checking the first line
    for curr_row in range(4, height):
        if collision_detection(piece, curr_row, col_offset, board):
            if curr_row - len(piece) <= 3:  # Is a part of the piece will be frozen into the hidden lines?
                return True
            freeze_piece(piece, curr_row - 1, col_offset, board)
            update_lines(list(range(curr_row - 1 - len(piece), curr_row)), board)
            return False
    freeze_piece(piece, height - 1, col_offset, board)
    update_lines(list(range(height - 1 - len(piece), height)), board)
    return False


def collision_detection(piece, row_offset, col_offset, board):
    """
    Detects collision if the piece were at the specified offset. The piece matrix is considered to start from
    (row_offset, col_offset) on the board and to the right and upwards. Since we hard drop, we only need to check the
    first non-zero value of each column, as the ones above it cannot collide before it collides, making the check for
    them irrelevant
    :param piece: The piece itself (not its PID)
    :param row_offset: The row number (offset from the top)
    :param col_offset: The column number (offset from the left)
    :param board: The game board
    :return: True if there is a collision, False otherwise
    """
    for col in range(len(piece[-1])):
        for row in range(1, len(piece) + 1):
            if piece[-row][col] > 0:
                if board[row_offset - row + 1][col_offset + col] > 0:
                    return True
                break
    return False


def freeze_piece(piece, row_offset, col_offset, board):
    """
    Freezes the piece in place
    :param piece: The piece itself (not its PID)
    :param row_offset: The row number (offset from the top)
    :param col_offset: The column number (offset from the left)
    :param board: The game board
    """
    for row in range(1, len(piece) + 1):
        for col in range(len(piece[-1])):
            if piece[-row][col] > 0:
                board[row_offset - row + 1][col_offset + col] = piece[-row][col]


def update_lines(lines, board):
    """
    Checks lines that might be filled as a result from the last piece drop
    :param lines: Lines to be checked (They need to be in an ascending order)
    :param board: The game board
    """
    counter = 0  # Number of full lines
    # We reverse the order to delete the last lines first. If we were to delete the first first, the deletion would
    # shift the lines downwards and change their index. By doing this, only greater lines from the current line are
    # shifted, which does not affect the lower ones
    for line in reversed(lines):
        if check_line_full(line, board):
            counter += 1
            del board[line]
    for _ in range(counter):
        board.insert(0, [0] * len(board[0]))  # Insert at the beginning


def check_line_full(line, board):
    """
    Checks if line is full
    :param line: :ine number
    :param board: The game board
    :return: True if the line is full, False otherwise
    """
    for value in board[line]:
        if value == 0:
            return False
    return True
