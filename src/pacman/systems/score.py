import pygame as pg

class Score:
    def __init__(self):
        self.current_score = 0
        self.best_score = 0
        self.font = pg.font.SysFont("Arial", 24)

    def add(self, points):
        self.current_score += points

    def draw(self, window, lives):
        score_surface = self.font.render(f"Score: {self.current_score}", True, (255, 255, 255))
        window.blit(score_surface, (10, 10))
        
        lives_surface = self.font.render(f"Lives: {lives}", True, (255, 255, 255))
        window.blit(lives_surface, (10, 40))

    def save_best_score(self):
        self.best_score = max(self.best_score, self.current_score)

    def get_current_score(self):
        return self.current_score
    
    def get_current_best_score(self):
        return self.best_score