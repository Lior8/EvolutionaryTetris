def extract_heights_and_holes(board):
    """
    Calculates the:
    Max height - Highest non-empty column (height is the tallest non-empty block)
    Cumulative height - sum of the height of each column
    Relative height - difference between the highest and lowest columns
    Holes - Hole is defined as an empty block with non-empty block somewhere above it in the column
    Roughness - Difference between each column and its right neighbor
    :param board: The game board
    :return: Feature vector
    """
    board_height = len(board)
    board_width = len(board[0])
    heights = [-1] * board_width
    holes = 0
    for col in range(board_width):
        for row in range(board_height):
            if heights[col] < 0:
                if board[row][col] > 0:
                    heights[col] = board_height - row
            else:
                if board[row][col] == 0:
                    holes += 1
        if heights[col] < 0:
            heights[col] = 0

    roughness = 0
    for i in range(board_width - 1):
        roughness += abs(heights[i + 1] - heights[i])
    height = max(heights)
    rel_height = height - min(heights)
    cum_height = sum(heights)
    return height, cum_height, rel_height, holes, roughness


def extract_wells(board):
    """
    Well is defined as an empty block with non-empty blocks on both its sides (the board's edges are considered
    non-empty blocks).
    This function finds the maximum well and the sum of all wells.
    :param board: The game board
    :return: Feature vector
    """
    board_height = len(board)
    board_width = len(board[0])
    max_well = 0
    cum_well = 0
    for col in range(1, board_width - 1):
        curr_well = 0
        for row in range(board_height):
            if board[row][col-1] > 0 and board[row][col] == 0 and board[row][col+1] > 0:
                curr_well += 1
                cum_well += 1
                if curr_well > max_well:
                    max_well = curr_well
            else:
                curr_well = 0
    left_well = 0
    right_well = 0
    for row in range(board_height):
        if board[row][0] == 0 and board[row][1] > 0:
            left_well += 1
            cum_well += 1
            if left_well > max_well:
                max_well = left_well
        else:
            left_well = 0

        if board[row][-1] == 0 and board[row][-2] > 0:
            right_well += 1
            cum_well += 1
            if right_well > max_well:
                max_well = right_well
        else:
            right_well = 0

    return max_well, cum_well


def extract_features(board):
    """
    An function to get all the board's features
    :param board: The game board
    :return: Feature vector
    """
    return extract_heights_and_holes(board) + extract_wells(board)
