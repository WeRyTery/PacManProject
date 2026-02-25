from pathlib import Path

# Board params
WIDTH, HEIGHT = 1280, 720
ROWS, COLUMNS = 60, 60

# Board borders
CENTERING_H = HEIGHT * 0.05
CENTERING_W = WIDTH * 0.25

# Square parameters
SQUARE_SIZE = WIDTH // COLUMNS

# Circle parameters
CIRCLE_SIZE = WIDTH // COLUMNS
CIRCLE_Y_OFFSET = 10
CIRCLE_X_OFFSET = 10
REGULAR_RADIUS = 2
SPECIAL_RADIUS = 5

# Rewards
FRUIT_POSITION = [17, 14]
SECONDS_TO_FRUIT_SPAWN = 10

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 157, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PINK = (255, 182, 193)
SCARED_GHOST_COLOR = (33, 33, 255)

# Game Settings
PACMAN_SPEED = 1.5
GHOST_SPEED = 1.5
PACMAN_LIVES = 3
SCARED_TIME = 7000
FLASHING_TIME = 2000   
FLASH_INTERVAL = 200

# Buttons
BUTTON_X = WIDTH // 2.5
BUTTON_Y = HEIGHT // 3
BUTTON_WIDTH = WIDTH // 5
BUTTON_HEIGHT = HEIGHT // 10

# Files
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
FRUIT_DIR = BASE_DIR / "sprites" / "Pac-Man-Pixel-PNG-Image-File.png"
SAVE_DIR = BASE_DIR / "user" / 'saves' / "score_save.json"
SOUND_DIR = BASE_DIR / "sounds"