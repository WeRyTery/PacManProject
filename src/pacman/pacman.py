import pygame as pg
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

    def draw(self, window):
        pg.draw.circle(window, YELLOW, (int(self.x), int(self.y)), self.radius)

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