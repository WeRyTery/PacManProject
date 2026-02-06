import pygame as pg
from .ghost import Ghost
from .constants import RED, CYAN, PINK, ORANGE, GHOST_SPEED, PACMAN_LIVES, CENTERING_W, CENTERING_H, SQUARE_SIZE, WHITE

class GhostHandler:
    def __init__(self, board):
        self.board = board
        self.lives = PACMAN_LIVES
        self.eaten_count = 0
        self.temp_scores = []
        self.spawn_ghosts()

    def spawn_ghosts(self):
        # Призраки выходят с интервалом: 0, 3, 6 и 9 секунд
        self.ghosts = [
            Ghost(13, 14, self.board, RED, 0),
            Ghost(13, 15, self.board, PINK, 3000),
            Ghost(14, 15, self.board, CYAN, 6000),
            Ghost(12, 14, self.board, ORANGE, 9000)
        ]

    def make_ghosts_scared(self):
        self.eaten_count = 0
        for ghost in self.ghosts:
            ghost.start_scared()

    def update(self, pacman):
        current_time = pg.time.get_ticks()
        # Удаляем надписи через 1 секунду
        self.temp_scores = [s for s in self.temp_scores if current_time - s['time'] < 1000]

        for ghost in self.ghosts:
            target = (pacman.x, pacman.y)
            if not ghost.scared and ghost.state == "ALIVE":
                if ghost.normal_color == PINK:
                    target = (pacman.x + pacman.vel_x * 4 * SQUARE_SIZE, pacman.y + pacman.vel_y * 4 * SQUARE_SIZE)
                elif ghost.normal_color == ORANGE:
                    dist = ((ghost.x - pacman.x)**2 + (ghost.y - pacman.y)**2)**0.5
                    if dist < 8 * SQUARE_SIZE: target = (CENTERING_W, CENTERING_H + 28 * SQUARE_SIZE)

            ghost.update(target)
            
            dist_to_p = ((pacman.x - ghost.x)**2 + (pacman.y - ghost.y)**2)**0.5
            if dist_to_p < pacman.radius + ghost.radius:
                if ghost.scared:
                    points = 200 * (2 ** self.eaten_count)
                    pacman.score.add(points)
                    self.temp_scores.append({'score': points, 'pos': (ghost.x, ghost.y), 'time': current_time})
                    self.eaten_count += 1
                    self.reset_ghost(ghost)
                else:
                    self.lives -= 1
                    if self.lives > 0: self.reset_positions(pacman); return False
                    return True
        return False

    def reset_ghost(self, ghost):
        ghost.scared, ghost.speed, ghost.state = False, GHOST_SPEED, "EXITING"
        ghost.x, ghost.y = CENTERING_W + 13 * SQUARE_SIZE + SQUARE_SIZE // 2, CENTERING_H + 14 * SQUARE_SIZE + SQUARE_SIZE // 2

    def reset_positions(self, pacman):
        pacman.x, pacman.y = pacman.start_x, pacman.start_y
        pacman.vel_x, pacman.vel_y, pacman.next_vel_x, pacman.next_vel_y = 0, 0, 0, 0
        self.spawn_ghosts()

    def draw(self, window):
        for ghost in self.ghosts: ghost.draw(window)
        font = pg.font.SysFont("Arial", 18, bold=True)
        for s in self.temp_scores:
            txt = font.render(str(s['score']), True, WHITE)
            window.blit(txt, (s['pos'][0]-10, s['pos'][1]-10))

            