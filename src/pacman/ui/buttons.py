import pygame as pg
from pygame_widgets.button import Button
from ..core.constants import * 
from ..core import event_bus

def get_play_button(window, offset_x=0, offset_y=0):
    play_button = Button(
        window,
        BUTTON_X + offset_x,
        BUTTON_Y + offset_y,
        BUTTON_WIDTH, 
        BUTTON_HEIGHT,
        text = 'Play',
        inactiveColour=YELLOW,
        onClick=lambda: pg.event.post(pg.event.Event(event_bus.PLAY_BUTTON))
    )
    return play_button

def get_settigns_button(window, offset_x=0, offset_y=0):
    settings_button = Button(
        window,
        BUTTON_X + offset_x,
        BUTTON_Y + offset_y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        text = "Settings",
        inactiveColour=YELLOW,
        onClick=lambda: pg.event.post(pg.event.Event(event_bus.SETTINGS_BUTTON))
    )
    return settings_button

def get_saves_button(window, offset_x=0, offset_y=0):
    saves_button = Button(
        window,
        BUTTON_X + offset_x,
        BUTTON_Y + offset_y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        text = "Load save",
        inactiveColour=YELLOW,
        onClick=lambda: pg.event.post(pg.event.Event(event_bus.SAVELOADER_BUTTON))
    )
    return saves_button