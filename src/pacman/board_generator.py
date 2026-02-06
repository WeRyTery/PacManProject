import pygame as pg
from .constants import *

class Board_generator:
    def __init__(self):
        self.board = []

    def draw_board(self, window, pattern):
        window.fill(BLACK)

        for row in range(len(pattern)):
            for col in range(len(pattern[row])):
                block = pattern[row][col]

                match block:
                    case "#": # border
                        pg.draw.rect(window, BLUE, (CENTERING_W + col * SQUARE_SIZE, CENTERING_H + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    case " ": # empty space
                        pg.draw.rect(window, BLACK, (CENTERING_W + col * SQUARE_SIZE, CENTERING_H + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    case ".": # regular coin
                        pg.draw.circle(window, WHITE, ((CENTERING_W + CIRCLE_X_OFFSET) + col * CIRCLE_SIZE, (CENTERING_H + CIRCLE_Y_OFFSET) + row * CIRCLE_SIZE), REGULAR_RADIUS)
                    case "o": # special coin
                        pg.draw.circle(window, WHITE, ((CENTERING_W + CIRCLE_X_OFFSET) + col * CIRCLE_SIZE, (CENTERING_H + CIRCLE_Y_OFFSET) + row * CIRCLE_SIZE), SPECIAL_RADIUS)
                    case "=": # hunters gate
                        pg.draw.rect(window, GREEN, (CENTERING_W + col * SQUARE_SIZE, CENTERING_H + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    case _:
                        print("")
    
