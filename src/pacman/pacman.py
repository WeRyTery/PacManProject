import pygame as pg
import math
from .constants import YELLOW, SQUARE_SIZE, CENTERING_W, CENTERING_H, PACMAN_SPEED

class Pacman:
    def __init__(self, col, row, board, score):
        # Сохраняем ссылку на доску, чтобы проверять стены
        self.board = board 
        self.score = score
        # Центрируем Пакмана в клетке
        self.x = CENTERING_W + col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = CENTERING_H + row * SQUARE_SIZE + SQUARE_SIZE // 2
        self.radius = SQUARE_SIZE // 2 - 2
        
        # Текущая скорость
        self.vel_x = 0
        self.vel_y = 0
        
        # Буфер для следующего поворота (намерение игрока)
        self.next_vel_x = 0
        self.next_vel_y = 0

        # --- НОВОЕ: АНИМАЦИЯ ---
        self.mouth_open_angle = 0  # Текущий угол открытия рта
        self.animation_speed = 5    # Скорость анимации
        self.opening = True


    def draw(self, window):
        center = (int(self.x), int(self.y))
        
        if self.mouth_open_angle == 0 or (self.vel_x == 0 and self.vel_y == 0):
            pg.draw.circle(window, YELLOW, center, self.radius)
        else:
            # Вычисляем направление (в радианах)
            base_angle = 0
            if self.vel_x > 0: base_angle = 0
            elif self.vel_x < 0: base_angle = math.pi
            elif self.vel_y > 0: base_angle = 0.5 * math.pi
            elif self.vel_y < 0: base_angle = 1.5 * math.pi

            # Генерируем точки для дуги
            points = [center]
            num_points = 20
            # Вырезаем угол рта из 360 градусов
            start_deg = math.degrees(base_angle) + self.mouth_open_angle
            end_deg = math.degrees(base_angle) + (360 - self.mouth_open_angle)
            
            for i in range(num_points + 1):
                angle = math.radians(start_deg + (end_deg - start_deg) * i / num_points)
                x = self.x + self.radius * math.cos(angle)
                y = self.y + self.radius * math.sin(angle)
                points.append((x, y))
            
            pg.draw.polygon(window, YELLOW, points)


    def handle_keys(self, event):
        # Метод, который вызывается в Game.py для WASD управления
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a: # Влево
                self.next_vel_x, self.next_vel_y = -PACMAN_SPEED, 0
            elif event.key == pg.K_d: # Вправо
                self.next_vel_x, self.next_vel_y = PACMAN_SPEED, 0
            elif event.key == pg.K_w: # Вверх
                self.next_vel_x, self.next_vel_y = 0, -PACMAN_SPEED
            elif event.key == pg.K_s: # Вниз
                self.next_vel_x, self.next_vel_y = 0, PACMAN_SPEED

    def is_at_center(self):
        # Проверка, находится ли Пакман в центре текущей клетки
        inner_pos_x = (self.x - CENTERING_W) % SQUARE_SIZE
        inner_pos_y = (self.y - CENTERING_H) % SQUARE_SIZE
        margin = PACMAN_SPEED 
        return abs(inner_pos_x - SQUARE_SIZE // 2) <= margin and abs(inner_pos_y - SQUARE_SIZE // 2) <= margin

    def can_move(self, vx, vy):
        board_array = self.board.get_board()
        col = int((self.x - CENTERING_W) // SQUARE_SIZE)
        row = int((self.y - CENTERING_H) // SQUARE_SIZE)
        
        next_col = col + (1 if vx > 0 else -1 if vx < 0 else 0)
        next_row = row + (1 if vy > 0 else -1 if vy < 0 else 0)

        # Если Пакман выходит за горизонтальные границы (телепорт)
        if next_col < 0 or next_col >= len(board_array[0]):
            # Разрешаем движение только если это горизонтальный туннель (пустое место)
            return True 

        # Стандартная проверка стен
        if 0 <= next_row < len(board_array):
            return board_array[next_row][next_col] != "#"
        return False

    def update(self):
        # 1. Логика поворота и остановки перед стенами (оставляем как есть)
        if (self.next_vel_x != 0 or self.next_vel_y != 0) and self.is_at_center():
            if self.can_move(self.next_vel_x, self.next_vel_y):
                col = int((self.x - CENTERING_W) // SQUARE_SIZE)
                row = int((self.y - CENTERING_H) // SQUARE_SIZE)
                self.x = CENTERING_W + col * SQUARE_SIZE + SQUARE_SIZE // 2
                self.y = CENTERING_H + row * SQUARE_SIZE + SQUARE_SIZE // 2
                
                self.vel_x, self.vel_y = self.next_vel_x, self.next_vel_y
                self.next_vel_x, self.next_vel_y = 0, 0

        if not self.can_move(self.vel_x, self.vel_y) and self.is_at_center():
            self.vel_x, self.vel_y = 0, 0

        # Обновляем координаты
        self.x += self.vel_x
        self.y += self.vel_y

        # --- НОВАЯ ЛОГИКА ТЕЛЕПОРТАЦИИ ---
        # Определяем границы
        cols_count = len(self.board.get_board()[0])
        left_bound = CENTERING_W
        right_bound = CENTERING_W + cols_count * SQUARE_SIZE

        # Телепортация на одну клетку раньше
        # Раньше: self.x < left_bound - SQUARE_SIZE // 2
        if self.x < left_bound + SQUARE_SIZE // 2: 
            self.x = right_bound - SQUARE_SIZE // 2
            
        # Раньше: self.x > right_bound + SQUARE_SIZE // 2
        elif self.x > right_bound - SQUARE_SIZE // 2:
            self.x = left_bound + SQUARE_SIZE // 2
        # 1. Если есть запланированный поворот и мы в центре клетки
        if (self.next_vel_x != 0 or self.next_vel_y != 0) and self.is_at_center():
            if self.can_move(self.next_vel_x, self.next_vel_y):
                # Идеально выравниваем перед поворотом
                col = int((self.x - CENTERING_W) // SQUARE_SIZE)
                row = int((self.y - CENTERING_H) // SQUARE_SIZE)
                self.x = CENTERING_W + col * SQUARE_SIZE + SQUARE_SIZE // 2
                self.y = CENTERING_H + row * SQUARE_SIZE + SQUARE_SIZE // 2
                
                # Применяем новую скорость
                self.vel_x, self.vel_y = self.next_vel_x, self.next_vel_y
                self.next_vel_x, self.next_vel_y = 0, 0

        # 2. Если впереди стена — останавливаемся
        if not self.can_move(self.vel_x, self.vel_y) and self.is_at_center():
            self.vel_x, self.vel_y = 0, 0

        # Обновляем координаты
        self.x += self.vel_x
        self.y += self.vel_y

        # Логика поедания точек
        board_array = self.board.get_board()
        col = int((self.x - CENTERING_W) // SQUARE_SIZE)
        row = int((self.y - CENTERING_H) // SQUARE_SIZE)

        if 0 <= row < len(board_array) and 0 <= col < len(board_array[0]):
            cell = board_array[row][col]
            if cell == ".":
                board_array[row][col] = " "
                self.score.add(10) # Вызов метода из score.py
            elif cell == "o":
                board_array[row][col] = " "
                self.score.add(50) # Вызов метода из score.py

        if self.vel_x != 0 or self.vel_y != 0: # Анимируем только в движении
            if self.opening:
                self.mouth_open_angle += self.animation_speed
                if self.mouth_open_angle >= 45: self.opening = False
            else:
                self.mouth_open_angle -= self.animation_speed
                if self.mouth_open_angle <= 0: self.opening = True
        else:
            self.mouth_open_angle = 0 # Закрываем рот при остановке 