import pygame as pg
from .constants import *


class Board_generator:
    def __init__(self):
        self.board = []
        self.coins = COINS_PERCENTAGE
        self.super_coins = SUPER_COINS_PERCENTAGE

    def draw_board(self, window):
        window.fill(BLACK)

        for row in range(len(LEVEL_PATTERN)):
            for col in range(len(LEVEL_PATTERN[row])):
                block = LEVEL_PATTERN[row][col]

                match block:
                    case "#": # border
                        pg.draw.rect(window, BLUE, (CENTERING_W + row * SQUARE_SIZE, CENTERING_H + col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    case " ": # empty space
                        pg.draw.rect(window, BLACK, (CENTERING_W + row * SQUARE_SIZE, CENTERING_H + col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    case ".": # regular coin
                        pg.draw.circle(window, WHITE, ((CENTERING_W + CIRCLE_X_OFFSET) + row * SQUARE_SIZE, (CENTERING_H + CIRCLE_Y_OFFSET) + col * SQUARE_SIZE), REGULAR_RADIUS)
                    case "o": # special coin
                        pg.draw.circle(window, WHITE, ((CENTERING_W + CIRCLE_X_OFFSET) + row * SQUARE_SIZE, (CENTERING_H + CIRCLE_Y_OFFSET) + col * SQUARE_SIZE), SPECIAL_RADIUS)
                    case "=": # hunters gate
                        pg.draw.rect(window, GREEN, (CENTERING_W + row * SQUARE_SIZE, CENTERING_H + col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    case _:
                        print("")
