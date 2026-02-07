from .constants import FRUIT_POSITION
from .board_generator import Board_generator

class Board:
    def __init__(self):
        #Game level pattern
        self.board = [
            list("############################"),
            list("#............##............#"),
            list("#.####.#####.##.#####.####.#"),
            list("#o####.#####.##.#####.####o#"),
            list("#.####.#####.##.#####.####.#"),
            list("#..........................#"),
            list("#.####.##.########.##.####.#"),
            list("#.####.##.########.##.####.#"),
            list("#......##....##....##......#"),
            list("######.##### ## #####.######"),
            list("     #.##### ## #####.#     "),
            list("     #.##          ##.#     "),
            list("     #.## ###==### ##.#     "),
            list("######.## #      # ##.######"),
            list("      .   #      #   .      "),
            list("######.## #      # ##.######"),
            list("     #.## ######## ##.#     "),
            list("     #.##          ##.#     "),
            list("     #.## ######## ##.#     "),
            list("######.## ######## ##.######"),
            list("#............##............#"),
            list("#.####.#####.##.#####.####.#"),
            list("#o..##................##..o#"),
            list("###.##.##.########.##.##.###"),
            list("#......##....##....##......#"),
            list("#.##########.##.##########.#"),
            list("#..........................#"),
            list("############################"),
        ]
        self.generator = Board_generator()
    
    def draw_board(self, WIN):
        self.generator.draw_board(WIN, self.board)
    
    def get_board(self):
        return self.board
    
    def update_board(self, new_board):
        self.board = new_board

    def spawn_fruit(self):
        x = FRUIT_POSITION[0]
        y = FRUIT_POSITION[1]

        self.board[x][y] = "F"
        
