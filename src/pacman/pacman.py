import pygame as pg
import math
from .constants import YELLOW, SQUARE_SIZE, CENTERING_W, CENTERING_H, PACMAN_SPEED

class Pacman:
    def __init__(self, col, row, board, score):
        self.board = board 
        self.score = score
        self.ghost_handler = None # Сюда придет ссылка из Game.py
        
        self.x = CENTERING_W + col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = CENTERING_H + row * SQUARE_SIZE + SQUARE_SIZE // 2
        self.start_x, self.start_y = self.x, self.y
        
        self.radius = SQUARE_SIZE // 2 - 2
        self.vel_x, self.vel_y = 0, 0
        self.next_vel_x, self.next_vel_y = 0, 0

        self.mouth_open_angle = 0
        self.animation_speed = 5
        self.opening = True

    def draw(self, window):
        center = (int(self.x), int(self.y))
        if self.mouth_open_angle == 0 or (self.vel_x == 0 and self.vel_y == 0):
            pg.draw.circle(window, YELLOW, center, self.radius)
        else:
            base_angle = 0
            if self.vel_x > 0: base_angle = 0
            elif self.vel_x < 0: base_angle = math.pi
            elif self.vel_y > 0: base_angle = 0.5 * math.pi
            elif self.vel_y < 0: base_angle = 1.5 * math.pi

            points = [center]
            start_deg = math.degrees(base_angle) + self.mouth_open_angle
            end_deg = math.degrees(base_angle) + (360 - self.mouth_open_angle)
            for i in range(21):
                angle = math.radians(start_deg + (end_deg - start_deg) * i / 20)
                points.append((self.x + self.radius * math.cos(angle), self.y + self.radius * math.sin(angle)))
            pg.draw.polygon(window, YELLOW, points)

    def handle_keys(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a: self.next_vel_x, self.next_vel_y = -PACMAN_SPEED, 0
            elif event.key == pg.K_d: self.next_vel_x, self.next_vel_y = PACMAN_SPEED, 0
            elif event.key == pg.K_w: self.next_vel_x, self.next_vel_y = 0, -PACMAN_SPEED
            elif event.key == pg.K_s: self.next_vel_x, self.next_vel_y = 0, PACMAN_SPEED

    def is_at_center(self):
        inner_pos_x = (self.x - CENTERING_W) % SQUARE_SIZE
        inner_pos_y = (self.y - CENTERING_H) % SQUARE_SIZE
        return abs(inner_pos_x - SQUARE_SIZE // 2) <= PACMAN_SPEED and abs(inner_pos_y - SQUARE_SIZE // 2) <= PACMAN_SPEED

    def can_move(self, vx, vy):
        board_array = self.board.get_board()
        col = int((self.x - CENTERING_W) // SQUARE_SIZE)
        row = int((self.y - CENTERING_H) // SQUARE_SIZE)
        next_col = col + (1 if vx > 0 else -1 if vx < 0 else 0)
        next_row = row + (1 if vy > 0 else -1 if vy < 0 else 0)
        if next_col < 0 or next_col >= len(board_array[0]): return True 
        if 0 <= next_row < len(board_array):
            return board_array[next_row][next_col] not in ["#", "="]
        return False

    def update(self):
        if (self.next_vel_x != 0 or self.next_vel_y != 0) and self.is_at_center():
            if self.can_move(self.next_vel_x, self.next_vel_y):
                col, row = int((self.x - CENTERING_W) // SQUARE_SIZE), int((self.y - CENTERING_H) // SQUARE_SIZE)
                self.x, self.y = CENTERING_W + col * SQUARE_SIZE + SQUARE_SIZE // 2, CENTERING_H + row * SQUARE_SIZE + SQUARE_SIZE // 2
                self.vel_x, self.vel_y = self.next_vel_x, self.next_vel_y
                self.next_vel_x, self.next_vel_y = 0, 0

        if not self.can_move(self.vel_x, self.vel_y) and self.is_at_center():
            self.vel_x, self.vel_y = 0, 0

        self.x += self.vel_x
        self.y += self.vel_y

        # Телепортация
        cols_count = len(self.board.get_board()[0])
        if self.x < CENTERING_W + SQUARE_SIZE // 2: self.x = CENTERING_W + (cols_count - 1) * SQUARE_SIZE + SQUARE_SIZE // 2
        elif self.x > CENTERING_W + cols_count * SQUARE_SIZE - SQUARE_SIZE // 2: self.x = CENTERING_W + SQUARE_SIZE // 2

        # Поедание
        board_array = self.board.get_board()
        col, row = int((self.x - CENTERING_W) // SQUARE_SIZE), int((self.y - CENTERING_H) // SQUARE_SIZE)
        if 0 <= row < len(board_array) and 0 <= col < len(board_array[0]):
            cell = board_array[row][col]
            if cell == ".":
                board_array[row][col] = " "
                self.score.add(10)
            elif cell == "o":
                board_array[row][col] = " "
                self.score.add(50)
                # Вызываем испуг призраков
                if self.ghost_handler: 
                    self.ghost_handler.make_ghosts_scared()

        # Анимация
        if self.vel_x != 0 or self.vel_y != 0:
            if self.opening:
                self.mouth_open_angle += self.animation_speed
                if self.mouth_open_angle >= 45: self.opening = False
            else:
                self.mouth_open_angle -= self.animation_speed
                if self.mouth_open_angle <= 0: self.opening = True
        else: self.mouth_open_angle = 0