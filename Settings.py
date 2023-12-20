# General Game Settings
import pygame.image

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
FPS = 60

# ANIMATION_COOLDOWN = 70

# Color declaration
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# World Settings
TILE_SIZE = 35
# todo change level width/length base on tileMap.csv
LEVEL_WIDTH = 47 * TILE_SIZE
LEVEL_HEIGHT = 31 * TILE_SIZE

GRAVITY = 0.8
InvincibleFrame = 70

# global tiles list
Tiles = []

# global enemy list
Enemy = []
