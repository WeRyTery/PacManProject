import pygame
from .constants import COINS_PERCENTAGE, SUPER_COINS_PERCENTAGE
from .board_generator import Board_generator

class Board:
    def __init__(self):
        self.board = []
        self.coins = COINS_PERCENTAGE
        self.super_coins = SUPER_COINS_PERCENTAGE
    
    def draw_board(self, WIN):
        Board_generator.draw_board(WIN)