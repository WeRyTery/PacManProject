import pygame as pg

class Score:
    def __init__(self):
        self.value = 0
        self.font = pg.font.SysFont("Arial", 24)

    def add(self, points):
        self.value += points

    def draw(self, window, lives):
        # Отрисовка счета
        score_surface = self.font.render(f"Score: {self.value}", True, (255, 255, 255))
        window.blit(score_surface, (10, 10))
        
        # Отрисовка жизней (чуть ниже счета)
        lives_surface = self.font.render(f"Lives: {lives}", True, (255, 255, 255))
        window.blit(lives_surface, (10, 40))