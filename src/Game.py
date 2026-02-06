import pygame as pg
from pacman.constants import WIDTH, HEIGHT
from pacman.board import Board

FPS = 60

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("PacMan")

board = Board()

def main():
    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        board.draw_board(WIN)
        pg.display.update()
            
    pg.quit()

main()