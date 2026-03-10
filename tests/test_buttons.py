import pygame
from pacman.core import event_bus
from pacman.ui import buttons
from unittest.mock import Mock


def test_play_button_event():
    window = pygame.Surface((800, 800))
    event = event_bus.PLAY_BUTTON

    result = buttons.handle_button_event(window, event)
    assert result is False


def test_saveloader_button_event(monkeypatch):
    window = pygame.Surface((800, 800))
    event = event_bus.SAVELOADER_BUTTON

    score = Mock()
    save_manager = Mock()

    save_manager.load_score.return_value = 100
    fake_event = pygame.event.Event(pygame.QUIT)

    monkeypatch.setattr(pygame.event, "get", lambda: [fake_event])
    result = buttons.handle_button_event(window, event, score, save_manager)

    assert result == 100
    assert score.best_score == 100
