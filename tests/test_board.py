import pytest
import pygame
from pacman.board.board_generator import Board_generator


class TestBoard:
    @pytest.mark.UI
    def test_draw_board(self):
        pygame.init()
        pygame.display.set_mode((1, 1))

        generator = Board_generator()

        window = pygame.Surface((800, 800))
        generator.draw_board(window, "#####")

        color = window.get_at((10, 10))
        assert color[1:4] == (0, 0, 255)
