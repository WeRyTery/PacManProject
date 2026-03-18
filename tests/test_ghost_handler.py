import pytest
from unittest.mock import Mock
from pacman.entities.ghost_handler import GhostHandler
from pacman.entities.pacman import Pacman
from pacman.core.constants import RED


@pytest.fixture
def handler_deps():
    board = Mock()
    board.get_board.return_value = [[" " for _ in range(30)] for _ in range(30)]
    sound_manager = Mock()
    sound_manager.sounds = {}
    return board, sound_manager


@pytest.mark.Data
def test_handler_spawn_ghosts(handler_deps):
    board, sound_manager = handler_deps
    handler = GhostHandler(board, sound_manager)

    assert len(handler.ghosts) == 4
    assert handler.ghosts[0].normal_color == RED


@pytest.mark.Data
def test_handler_make_ghosts_scared(handler_deps):
    board, sound_manager = handler_deps
    handler = GhostHandler(board, sound_manager)

    for ghost in handler.ghosts:
        ghost.state = "ALIVE"

    handler.make_ghosts_scared()

    assert all(ghost.scared for ghost in handler.ghosts)
    assert handler.eaten_count == 0


@pytest.mark.UI
def test_collision_pacman_death(handler_deps):
    board, sound_manager = handler_deps
    score = Mock()
    handler = GhostHandler(board, sound_manager)
    pacman = Pacman(13, 14, board, score, handler, sound_manager)

    ghost = handler.ghosts[0]
    ghost.state = "ALIVE"
    ghost.scared = False
    ghost.x, ghost.y = pacman.x, pacman.y

    handler.update(pacman)
    assert handler.lives == 2
