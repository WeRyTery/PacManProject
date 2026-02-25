import pygame as pg
import argparse

from pacman.core.constants import WIDTH, HEIGHT
from pacman.ui.scenes import Scenes
from pacman.board.board import Board
from pacman.entities.pacman import Pacman
from pacman.systems.score import Score
from pacman.systems.save_manager import Save_manager
from pacman.systems.sound_manager import Sound_Manager
from pacman.entities.ghost_handler import GhostHandler


def main():
    print(argument_parser())
    FPS = argument_parser()

    pg.init() 
    WIN = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("PacMan")

    sound_manager = Sound_Manager()
    clock = pg.time.Clock()
    scenes = Scenes(sound_manager)
    board = Board()
    score = Score()
    save_manager = Save_manager()

    ghost_handler = GhostHandler(board, sound_manager)
    pacman = Pacman(13, 22, board, score, ghost_handler, sound_manager)
    
    
    scenes.main_menu(WIN, clock, score, save_manager, FPS)
    scenes.game_cycle(WIN, clock, board, score, save_manager, pacman, ghost_handler, FPS)
    scenes.game_over(WIN, clock, score, FPS)


def argument_parser() -> int:
    parser = argparse.ArgumentParser(prog="Pacman")
    parser.add_argument('-f', '--fps',
                         default=60,
                         type=int
                        )
    args = parser.parse_args()
    return args.fps
main()