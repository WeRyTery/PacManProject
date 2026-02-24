import pygame as pg
import pygame_widgets as pw

from ..core.constants import * 
from .buttons import *
from ..core.event_bus import *

class Scenes:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.game_status_text = "lost"

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
                    if "game_start" in self.sound_manager.sounds:
                        self.sound_manager.sounds["game_start"].play()
                    active_window = handle_button_event(window, PLAY_BUTTON)
                elif event.type == SAVELOADER_BUTTON:
                    best_score = handle_button_event(window, SAVELOADER_BUTTON, score, save_manager)
                elif event.type == SETTINGS_BUTTON:
                    play_button.hide()
                    settings_button.hide()
                    saves_button.hide()
                    
                    self.settings_menu(window, clock, fps)
                    
                    play_button.show()
                    settings_button.show()
                    saves_button.show()
                    
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

            #All coins collected
            if board.check_for_win():
                self.game_logic_run = False
                self.game_status_text = "won"
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
            font = pg.font.SysFont("arial", 100, bold=True)
            game_over_text = font.render(f"Game over, you {self.game_status_text}!", True, WHITE)

            font = pg.font.SysFont("arial", 100, bold=True)
            game_score_text = font.render(f"Score: {score.get_current_score()}", True, YELLOW)

            window.blit(game_over_text, (WIDTH // 10, HEIGHT // 3))
            window.blit(game_score_text, (WIDTH // 3, HEIGHT // 1.5))

            pg.display.update()
            
        pg.quit()



    def settings_menu(self, window, clock, fps=30):

        volume_slider = get_volume_slider(window, offset_y=0)
        back_button = get_back_button(window, offset_y=100)
        
        active_settings = True
        BACK_EVENT = pg.USEREVENT + 10

        while active_settings:
            clock.tick(fps)
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == BACK_EVENT:
                    active_settings = False

            current_vol = volume_slider.getValue()
            self.sound_manager.set_volume(current_vol)

            window.fill(BLACK)
            
            font = pg.font.SysFont("arial", 30, bold=True)
            text = font.render(f"Volume: {current_vol}%", True, WHITE)
            window.blit(text, (BUTTON_X, BUTTON_Y - 40))

            pw.update(events)
            pg.display.update()
            
        volume_slider.hide()
        back_button.hide()