import pygame as pg
import pygame_widgets as pw

from ..core.constants import * 
from .buttons import *
from ..core.event_bus import *

class Scenes:
    def main_menu(self, window, clock, fps=30):
        offset = BUTTON_HEIGHT+20

        play_button = get_play_button(window)
        settings_button = get_settigns_button(window, offset_y=offset)
        saves_button = get_saves_button(window, offset_y=(offset * 2))

        active_window = True

        while active_window:
            clock.tick(fps)
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    active_window = False
                elif event.type == PLAY_BUTTON:
                    active_window = False
                    print("Started playing")
                    return

            window.fill(BLACK)
            pw.update(events)
            pg.display.update()
        pg.quit()


    def game_cycle(self, window, board, score, pacman, ghosts, clock, fps=60):
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
            if ghosts.update(pacman):
                game_logic_run = False
                break

            window.fill(BLACK)
            board.draw_board(window)
            pacman.draw(window)
            ghosts.draw(window)
            score.draw(window, ghosts.lives)

            pg.display.update()
            
        score.save_best_score()
        return quit_requested


    def game_over(self, window, clock, score, fps=30):
        active_window = True

        while active_window: # Game is active untill user closes window
            clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    active_window = False

            window.fill(BLACK)
            font = pg.font.SysFont("arial", 200, bold=True)
            game_over_text = font.render("Game over!", True, WHITE)

            font = pg.font.SysFont("arial", 100, bold=True)
            game_score_text = font.render(f"Score: {score.get_current_score()}", True, YELLOW)

            window.blit(game_over_text, (WIDTH // 15, HEIGHT // 3))
            window.blit(game_score_text, (WIDTH // 3, HEIGHT // 1.5))

            pg.display.update()

        pg.quit()