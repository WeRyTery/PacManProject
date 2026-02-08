import pygame as pg
from pacman.constants import *
from pacman.board import Board
from pacman.pacman import Pacman
from pacman.score import Score
from pacman.ghost_handler import GhostHandler
from pacman.scenes import Scenes

FPS = 60
pg.init() 
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("PacMan")

scenes = Scenes()
board = Board()
score = Score()

pacman = Pacman(13, 22, board, score)
ghost_handler = GhostHandler(board)

pacman.ghost_handler = ghost_handler 

def main():
    clock = pg.time.Clock()
    quit_requested = False
    
    quit_requested = scenes.game_cycle(WIN, board, pacman, ghost_handler, score, clock, FPS)

    if quit_requested:
        pg.quit()
        return
    
    scenes.game_over(WIN, clock, FPS)

    

main()