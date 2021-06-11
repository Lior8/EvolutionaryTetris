class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = []
        for _ in range(height):
            self.board.append([0] * width)
