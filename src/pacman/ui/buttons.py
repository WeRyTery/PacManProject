import pygame as pg
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from ..core.constants import *
from ..core import event_bus


def get_play_button(window, offset_x=0, offset_y=0):
    play_button = Button(
        window,
        BUTTON_X + offset_x,
        BUTTON_Y + offset_y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        text="Play",
        inactiveColour=YELLOW,
        hoverColour=ORANGE,
        onClick=lambda: pg.event.post(pg.event.Event(event_bus.PLAY_BUTTON)),
    )
    return play_button


def get_settigns_button(window, offset_x=0, offset_y=0):
    settings_button = Button(
        window,
        BUTTON_X + offset_x,
        BUTTON_Y + offset_y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        text="Settings",
        inactiveColour=YELLOW,
        hoverColour=ORANGE,
        onClick=lambda: pg.event.post(pg.event.Event(event_bus.SETTINGS_BUTTON)),
    )
    return settings_button


def get_saves_button(window, offset_x=0, offset_y=0):
    saves_button = Button(
        window,
        BUTTON_X + offset_x,
        BUTTON_Y + offset_y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        text="Load save",
        inactiveColour=YELLOW,
        hoverColour=ORANGE,
        onClick=lambda: pg.event.post(pg.event.Event(event_bus.SAVELOADER_BUTTON)),
    )
    return saves_button


def handle_button_event(window, event, score=None, save_manager=None):
    if event == event_bus.PLAY_BUTTON:
        active_window = False
        return active_window
    elif event == event_bus.SAVELOADER_BUTTON:
        best_score = save_manager.load_score()
        score.best_score = best_score
        active_saveloader = True

        while active_saveloader:
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    active_saveloader = False
                    break

            window.fill(BLACK)
            font = pg.font.SysFont("arial", 30, bold=True)
            game_score_text = font.render(
                f"Save file has been loaded from: {SAVE_DIR}", True, GREEN
            )
            window.blit(game_score_text, (WIDTH * 0.1, HEIGHT // 2.5))
            pg.display.update()
        return best_score


def get_volume_slider(window, offset_y=0):
    volume_slider = Slider(
        window,
        BUTTON_X,
        BUTTON_Y + offset_y,
        BUTTON_WIDTH,
        20,
        min=0,
        max=100,
        step=1,
        initial=100,
        colour=YELLOW,
        handleColour=WHITE,
    )
    return volume_slider


def get_back_button(window, offset_y=0):
    return Button(
        window,
        BUTTON_X,
        BUTTON_Y + offset_y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        text="Back",
        inactiveColour=YELLOW,
        hoverColour=ORANGE,
        onClick=lambda: pg.event.post(pg.event.Event(pg.USEREVENT + 10)),
    )
