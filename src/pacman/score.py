import pygame as pg

class Score:
    def __init__(self):
        self.value = 0
        self.font = pg.font.SysFont("Arial", 24)

    def add(self, points):
        self.value += points

    def draw(self, window):
        # Создаем текстовую поверхность
        score_surface = self.font.render(f"Score: {self.value}", True, (255, 255, 255))
        # Отрисовываем в верхнем левом углу с небольшим отступом
        window.blit(score_surface, (10, 10))