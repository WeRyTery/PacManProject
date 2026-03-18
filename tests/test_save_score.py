import pytest
import pygame as pg
from pacman.systems.save_manager import Save_manager
from pacman.systems.score import Score


@pytest.fixture
def pygame_init():
    pg.init()
    yield  # To complete after tests
    pg.quit()


@pytest.fixture
def score(pygame_init):
    return Score()


@pytest.fixture
def save_manager(pygame_init):
    return Save_manager()


########################################################################################


@pytest.mark.Data
@pytest.mark.parametrize("best_score", [0, 50, 150])
def test_save_and_load(score, save_manager, best_score):
    score.best_score = best_score
    save_manager.save_score(score)

    loaded_score = save_manager.load_score()
    assert loaded_score == score.get_current_best_score()


@pytest.mark.Data
def test_score_get(score):
    assert score.get_current_score() == 0


@pytest.mark.Data
@pytest.mark.parametrize("score_val", [0, 100, 200])
def test_score_add(score, score_val):
    score.add(score_val)

    assert score.get_current_score() == score_val


@pytest.mark.Data
@pytest.mark.parametrize(
    "score_val, best_score_val", [(100, 150), (200, 300), (350, 900)]
)
def test_score_get_best(score, score_val, best_score_val):
    score.add(score_val)

    score.best_score = best_score_val
    assert score.get_current_best_score() == best_score_val


@pytest.mark.Data
@pytest.mark.parametrize(
    "old_best_score, new_best_score", [(100, 150), (200, 400), (300, 500)]
)
def test_score_best_Save(score, old_best_score, new_best_score):
    new_best_score = new_best_score
    score.best_score = old_best_score
    score.add(new_best_score)

    score.save_best_score()
    assert score.best_score == new_best_score
