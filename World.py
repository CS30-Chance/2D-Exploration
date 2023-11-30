import pygame
from Settings import *

class Ground:
    def __init__(self, surface, x, y):
        self.surface = surface
        self.tileSize = TILE_SIZE
        self.x = x * self.tileSize
        self.y = y * self.tileSize
        self.image = pygame.image.load('Assets/Textures&trees/sprite_083.png')
        self.spritesImage = pygame.transform.scale(self.image, [self.tileSize, self.tileSize])
        self.rect = self.spritesImage.get_rect()
        self.rect.topleft = [self.x, self.y]

    def drawTile(self):
        self.surface.blit(self.spritesImage, [self.x, self.y])
        pygame.draw.rect(self.surface, 'green', self.rect, 1)
        


class World:
    def __init__(self):
        # todo use tile-map csv to load world
        self.tileMap = None

