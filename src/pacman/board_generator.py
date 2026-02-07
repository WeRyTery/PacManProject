import pygame as pg
from .constants import *
from .event_bus import FRUIT_SPAWN

class Board_generator:
    def __init__(self):
        self.board = []
        self.cherry_img = pg.image.load(r"C:\Users\Ghost\Documents\GitHub\PacManProject\sprites\Pac-Man-Pixel-PNG-Image-File.png").convert_alpha()
        self.cherry_img = pg.transform.scale(self.cherry_img, (CIRCLE_SIZE, CIRCLE_SIZE))

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
                    case "F":
                        window.blit(self.cherry_img, (CENTERING_W + col * CIRCLE_SIZE, CENTERING_H + row * CIRCLE_SIZE))
                        pg.time.set_timer(FRUIT_SPAWN, (1000 * SECONDS_TO_FRUIT_SPAWN), 0) # NOTE: Timer doesn't countdown unless fruit has been eaten
                        
                        
