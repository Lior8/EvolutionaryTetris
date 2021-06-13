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
