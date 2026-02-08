import pygame as pg
from .constants import * 
from .event_bus import FRUIT_SPAWN, GAME_OVER

class Scenes:
    def main_menu(self, window, clock, fps):
        pass

    def game_cycle(self, window, board, pacman, ghost_handler, score, clock, fps=60):
        pg.time.set_timer(FRUIT_SPAWN, (1000 * SECONDS_TO_FRUIT_SPAWN), 0)
        game_logic_run = True
        quit_requested = False

        while game_logic_run:
            clock.tick(fps)

            for event in pg.event.get():
                if event.type == FRUIT_SPAWN:
                    board.spawn_fruit()
                    break
                elif event.type == pg.QUIT:
                    game_logic_run = False
                    quit_requested = True
                pacman.handle_keys(event)
                

            pacman.update()

            #Pacman lost all lives
            if ghost_handler.update(pacman):
                game_logic_run = False
                break

            window.fill(BLACK)
            board.draw_board(window)
            pacman.draw(window)
            ghost_handler.draw(window)
            score.draw(window, ghost_handler.lives)

            pg.display.update()

        return quit_requested

    def game_over(self, window, clock, fps=30):
        active_window = True

        while active_window: # Game is active untill user closes window
            clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    active_window = False

            window.fill(BLACK)
            font = pg.font.SysFont("arial", 200, bold=True)
            text = font.render("Game over!", True, WHITE)
            window.blit(text, (WIDTH // 15, HEIGHT // 3))

            pg.display.update()

        pg.quit()