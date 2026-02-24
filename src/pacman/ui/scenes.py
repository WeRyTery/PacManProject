import pygame as pg
import pygame_widgets as pw

from ..core.constants import * 
from .buttons import *
from ..core.event_bus import *

class Scenes:
    def main_menu(self, window, clock, score, save_manager, fps=30):
        offset = BUTTON_HEIGHT+20

        play_button = get_play_button(window)
        settings_button = get_settigns_button(window, offset_y=offset)
        saves_button = get_saves_button(window, offset_y=(offset * 2))

        best_score = save_manager.load_score()
        score.best_score = best_score

        active_window = True

        while active_window:
            clock.tick(fps)
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    active_window = False
                    exit()
                    return
                elif event.type == PLAY_BUTTON:
                    active_window = handle_button_event(window, PLAY_BUTTON)
                elif event.type == SAVELOADER_BUTTON:
                    best_score = handle_button_event(window, SAVELOADER_BUTTON, score, save_manager)
                    
            window.fill(BLACK)
            font = pg.font.SysFont("arial", 20, bold=True)
            game_score_text = font.render(f"Best score: {best_score}", True, WHITE)
            window.blit(game_score_text, (WIDTH // 2.25, HEIGHT // 4))

            pw.update(events)
            pg.display.update()


    def game_cycle(self, window, clock, board, score, save_manager, pacman, ghosts, fps=60):
        pg.time.set_timer(FRUIT_SPAWN, (1000 * SECONDS_TO_FRUIT_SPAWN), 0)

        game_logic_run = True
        

        while game_logic_run:
            clock.tick(fps)

            for event in pg.event.get():
                if event.type == FRUIT_SPAWN:
                    board.spawn_fruit()
                    break
                elif event.type == pg.QUIT:
                    game_logic_run = False
                    save_manager.save_score(score)
                    pg.quit()
                    exit()
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
            
        save_manager.save_score(score)


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