import pygame as pg
from pacman.constants import WIDTH, HEIGHT, BLACK
from pacman.board import Board
from pacman.pacman import Pacman
from pacman.score import Score  # Импортируем новый класс

FPS = 60
pg.init() # Важно инициализировать все модули pygame для работы шрифтов
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("PacMan")

board = Board()
score = Score() # Создаем экземпляр счета
pacman = Pacman(13, 22, board, score) # Передаем счет в пакмана

def main():
    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            pacman.handle_keys(event)

        pacman.update()

        WIN.fill(BLACK)
        board.draw_board(WIN)
        pacman.draw(WIN)
        score.draw(WIN) # Отрисовываем счет через новый файл
        
        pg.display.update()
            
    pg.quit()

main()