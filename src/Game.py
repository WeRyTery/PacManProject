import pygame as pg
from pacman.constants import WIDTH, HEIGHT, BLACK, SECONDS_TO_FRUIT_SPAWN, FRUIT_POSITION
from pacman.board import Board
from pacman.pacman import Pacman
from pacman.score import Score
from pacman.ghost_handler import GhostHandler
from pacman.event_bus import FRUIT_SPAWN

FPS = 60
pg.init() 
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("PacMan")

board = Board()
score = Score()
pacman = Pacman(13, 22, board, score)
ghost_handler = GhostHandler(board)

pacman.ghost_handler = ghost_handler 

pg.time.set_timer(FRUIT_SPAWN, (1000 * SECONDS_TO_FRUIT_SPAWN), 0)
fruit_x = FRUIT_POSITION[0]
fruit_y = FRUIT_POSITION[1]

def main():
    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == FRUIT_SPAWN:
                board.spawn_fruit()
            elif event.type == pg.QUIT:
                run = False
            pacman.handle_keys(event)

        pacman.update()
        
        # Если призраки съели все жизни — Game Over
        if ghost_handler.update(pacman):
            print("Game Over!")
            run = False

        WIN.fill(BLACK)
        board.draw_board(WIN)
        pacman.draw(WIN)
        ghost_handler.draw(WIN)
        score.draw(WIN, ghost_handler.lives)
        
        pg.display.update()
            
    pg.quit()

main()