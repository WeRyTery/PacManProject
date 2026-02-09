import pygame as pg

from pacman.core.constants import WIDTH, HEIGHT
from pacman.ui.scenes import Scenes
from pacman.board.board import Board
from pacman.entities.pacman import Pacman
from pacman.systems.score import Score
from pacman.entities.ghost_handler import GhostHandler


def main():
    FPS = 60

    pg.init() 
    WIN = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("PacMan")

    clock = pg.time.Clock()
    scenes = Scenes()
    board = Board()
    score = Score()

    pacman = Pacman(13, 22, board, score)
    ghost_handler = GhostHandler(board)
    
    scenes.main_menu(WIN, clock, FPS)

    quit_requested = scenes.game_cycle(WIN, board, score, pacman, ghost_handler, clock, FPS)
    if quit_requested:
        pg.quit()
        return
    
    scenes.game_over(WIN, clock, score, FPS)

main()