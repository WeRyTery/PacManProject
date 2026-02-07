import pygame as pg
import random
from .constants import (
    SQUARE_SIZE, CENTERING_W, CENTERING_H, GHOST_SPEED, 
    SCARED_GHOST_COLOR, SCARED_TIME, WHITE, FLASHING_TIME, FLASH_INTERVAL, BLACK
)

class Ghost:
    def __init__(self, col, row, board, color, spawn_delay=0):
        self.board = board
        self.normal_color = color
        self.x = CENTERING_W + col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = CENTERING_H + row * SQUARE_SIZE + SQUARE_SIZE // 2
        self.radius = SQUARE_SIZE // 2 - 2
        self.vel_x, self.vel_y = 0, 0
        self.speed = GHOST_SPEED
        self.state = "EXITING" 
        self.scared = False
        self.scared_timer = 0
        self.spawn_delay = spawn_delay
        self.start_time = pg.time.get_ticks()
        
        self.exit_x = CENTERING_W + 13 * SQUARE_SIZE + SQUARE_SIZE // 2 
        self.target_y = CENTERING_H + 11 * SQUARE_SIZE + SQUARE_SIZE // 2

    def get_dist(self, direction, target_pos):
        next_x = self.x + direction[0]
        next_y = self.y + direction[1]
        return ((next_x - target_pos[0])**2 + (next_y - target_pos[1])**2)**0.5

    def draw(self, window):
        if pg.time.get_ticks() - self.start_time < self.spawn_delay:
            return

        # Определяем основной цвет (с учетом моргания)
        if self.scared:
            time_left = SCARED_TIME - (pg.time.get_ticks() - self.scared_timer)
            if time_left < FLASHING_TIME and (time_left // FLASH_INTERVAL) % 2 == 0:
                body_color = WHITE
            else:
                body_color = SCARED_GHOST_COLOR
        else:
            body_color = self.normal_color

        # 1. Рисуем тело призрака (голова + туловище)
        # Верхняя часть (голова)
        pg.draw.circle(window, body_color, (int(self.x), int(self.y)), self.radius)
        # Нижняя часть (прямоугольник)
        pg.draw.rect(window, body_color, (self.x - self.radius, self.y, self.radius * 2, self.radius))

        # 2. Рисуем глаза
        eye_radius = self.radius // 3
        eye_offset = self.radius // 2
        # Белки глаз (если не испуган)
        if not self.scared:
            # Левый глаз
            pg.draw.circle(window, WHITE, (int(self.x - eye_offset), int(self.y - 2)), eye_radius + 1)
            # Правый глаз
            pg.draw.circle(window, WHITE, (int(self.x + eye_offset), int(self.y - 2)), eye_radius + 1)
            
            # Зрачки (смотрят в сторону направления)
            pupil_radius = eye_radius // 1.5
            px, py = 0, 0
            if self.vel_x > 0: px = 1
            elif self.vel_x < 0: px = -1
            elif self.vel_y > 0: py = 1
            elif self.vel_y < 0: py = -1
            
            pg.draw.circle(window, BLACK, (int(self.x - eye_offset + px*2), int(self.y - 2 + py*2)), pupil_radius)
            pg.draw.circle(window, BLACK, (int(self.x + eye_offset + px*2), int(self.y - 2 + py*2)), pupil_radius)
        else:
            # Если испуган, рисуем маленькие «глазки-точки» или просто испуганное выражение
            pg.draw.circle(window, WHITE, (int(self.x - eye_offset), int(self.y)), 2)
            pg.draw.circle(window, WHITE, (int(self.x + eye_offset), int(self.y)), 2)

    def start_scared(self):
        if self.state == "ALIVE":
            self.scared = True
            self.scared_timer = pg.time.get_ticks()
            self.speed = GHOST_SPEED * 0.5

    def can_move(self, vx, vy):
        board_array = self.board.get_board()
        col, row = int((self.x - CENTERING_W) // SQUARE_SIZE), int((self.y - CENTERING_H) // SQUARE_SIZE)
        next_col, next_row = col + (1 if vx > 0 else -1 if vx < 0 else 0), row + (1 if vy > 0 else -1 if vy < 0 else 0)
        if 0 <= next_row < len(board_array) and 0 <= next_col < len(board_array[0]):
            cell = board_array[next_row][next_col]
            if self.state == "ALIVE": return cell not in ["#", "="]
            return cell != "#"
        return False

    def is_at_center(self):
        inner_pos_x = (self.x - CENTERING_W) % SQUARE_SIZE
        inner_pos_y = (self.y - CENTERING_H) % SQUARE_SIZE
        return abs(inner_pos_x - SQUARE_SIZE // 2) < self.speed and abs(inner_pos_y - SQUARE_SIZE // 2) < self.speed

    def update(self, target_pos):
        if pg.time.get_ticks() - self.start_time < self.spawn_delay:
            return

        if self.scared and pg.time.get_ticks() - self.scared_timer > SCARED_TIME:
            self.scared = False
            self.speed = GHOST_SPEED

        if self.state == "EXITING":
            # 1. Сначала выравниваемся по горизонтали ровно под проходом
            if abs(self.x - self.exit_x) > self.speed:
                self.vel_y = 0
                self.vel_x = self.speed if self.x < self.exit_x else -self.speed
            else:
                # Фиксируем X строго по центру, чтобы не задевать края при подъеме
                self.x = self.exit_x 
                self.vel_x = 0
                self.vel_y = -self.speed
                
                # 2. Выход на дорожку (target_y)
                # Используем <= чтобы поймать момент пересечения линии
                if self.y <= self.target_y:
                    self.y = self.target_y # Жесткая фиксация на центре дорожки
                    self.state = "ALIVE"
                    # Сразу выбираем направление, чтобы не ехать дальше вверх в стену
                    self.vel_x, self.vel_y = random.choice([(self.speed, 0), (-self.speed, 0)])

        elif self.state == "ALIVE":
            if self.is_at_center():
                dirs = [(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)]
                
                # Добавляем проверку, чтобы призраки не считали туннели валидным путем для побега
                valid = []
                board_array = self.board.get_board()
                col = int((self.x - CENTERING_W) // SQUARE_SIZE)
                row = int((self.y - CENTERING_H) // SQUARE_SIZE)

                for d in dirs:
                    next_col = col + (1 if d[0] > 0 else -1 if d[0] < 0 else 0)
                    # Проверяем: 1. Можно ли туда ходить? 2. Не разворот ли это? 3. Не край ли это карты (туннель)?
                    if self.can_move(d[0], d[1]) and d != (-self.vel_x, -self.vel_y):
                        if 0 <= next_col < len(board_array[0]): # Запрещаем призракам заходить в телепорт
                            valid.append(d)
                
                if valid:
                    if self.scared:
                        self.vel_x, self.vel_y = max(valid, key=lambda d: self.get_dist(d, target_pos))
                    else:
                        self.vel_x, self.vel_y = min(valid, key=lambda d: self.get_dist(d, target_pos))
                elif not self.can_move(self.vel_x, self.vel_y):
                    self.vel_x, self.vel_y = -self.vel_x, -self.vel_y

        self.x += self.vel_x
        self.y += self.vel_y