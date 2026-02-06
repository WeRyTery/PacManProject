import pygame as pg
from pacman.constants import WIDTH, HEIGHT, BLACK
from pacman.board import Board
from pacman.pacman import Pacman # Импортируем новый класс

FPS = 60
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("PacMan")

board = Board()
pacman = Pacman(13, 22, board) 

def main():
    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            # Передаем событие в пакмана для мгновенной реакции
            pacman.handle_keys(event)

        # Обновляем позицию
        pacman.update()

        # Отрисовка
        WIN.fill(BLACK)
        board.draw_board(WIN)
        pacman.draw(WIN)
        pg.display.update()
            
    pg.quit()

main()