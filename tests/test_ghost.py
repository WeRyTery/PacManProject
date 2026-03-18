import pytest
from unittest.mock import Mock
from pacman.entities.ghost import Ghost
from pacman.core.constants import RED, GHOST_SPEED


@pytest.fixture
def ghost_deps():
    board = Mock()
    board.get_board.return_value = [[" " for _ in range(30)] for _ in range(30)]
    return board


@pytest.mark.UI
def test_ghost_initialization(ghost_deps):
    ghost = Ghost(13, 14, ghost_deps, RED)

    assert ghost.normal_color == RED
    assert ghost.state == "EXITING"
    assert ghost.scared is False


@pytest.mark.Data
def test_ghost_start_scared(ghost_deps):
    ghost = Ghost(13, 14, ghost_deps, RED)
    ghost.state = "ALIVE"

    ghost.start_scared()

    assert ghost.scared is True
    assert ghost.speed == ghost.max_speed * 0.5


@pytest.mark.UI
def test_ghost_can_move_collision(ghost_deps):
    ghost_deps.get_board.return_value = [[" ", "#"]]
    ghost = Ghost(0, 0, ghost_deps, RED)
    ghost.state = "ALIVE"

    assert ghost.can_move(GHOST_SPEED, 0) is False
