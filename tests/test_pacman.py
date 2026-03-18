import pytest
import pygame as pg
from unittest.mock import Mock
from pacman.entities.pacman import Pacman
from pacman.core.constants import SQUARE_SIZE, PACMAN_SPEED

@pytest.fixture
def pacman_deps():
    board = Mock()
    board.get_board.return_value = [[" " for _ in range(30)] for _ in range(30)]
    score = Mock()
    sound_manager = Mock()
    sound_manager.sounds = {}
    return board, score, sound_manager

@pytest.mark.UI
def test_pacman_initialization(pacman_deps):
    board, score, sound_manager = pacman_deps
    pacman = Pacman(1, 1, board, score, None, sound_manager)
    
    assert pacman.radius == SQUARE_SIZE // 2 - 2
    assert pacman.vel_x == 0
    assert pacman.vel_y == 0

@pytest.mark.UI
def test_pacman_handle_keys(pacman_deps):
    board, score, sound_manager = pacman_deps
    pacman = Pacman(1, 1, board, score, None, sound_manager)
    
    event = pg.event.Event(pg.KEYDOWN, key=pg.K_d)
    pacman.handle_keys(event)
    
    assert pacman.next_vel_x == PACMAN_SPEED

@pytest.mark.Data
def test_pacman_eating_dot(pacman_deps):
    board, score, sound_manager = pacman_deps
    grid = [[" " for _ in range(5)], [" ", ".", " "]]
    board.get_board.return_value = grid
    
    pacman = Pacman(1, 1, board, score, None, sound_manager)
    pacman.update()
    
    assert grid[1][1] == " "
    score.add.assert_called_with(10)