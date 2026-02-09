import pygame as pg

from pacman.core.constants import WIDTH, HEIGHT
from pacman.ui.scenes import Scenes
from pacman.board.board import Board
from pacman.entities.pacman import Pacman
from pacman.systems.score import Score
from pacman.systems.save_manager import Save_manager
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
    save_manager = Save_manager()

    pacman = Pacman(13, 22, board, score)
    ghost_handler = GhostHandler(board)
    
    
    scenes.main_menu(WIN, clock, score, save_manager, FPS)
    scenes.game_cycle(WIN, clock, board, score, save_manager, pacman, ghost_handler, FPS)
    scenes.game_over(WIN, clock, score, FPS)

main()
