import pygame

class Ground:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tileSize = 20
        self.spritesImage = pygame.image.load('Assets/Textures&trees/sprite_083.png')
        self.tile = None
        # self.sprites = []
        self.rect = self.spritesImage.get_rect()
        self.rect.topleft = [self.x, self.y]


    def createTile(self):
        self.tile = pygame.Surface([self.tileSize, self.tileSize])
        self.tile.blit(self.spritesImage, (0, 0))

    def drawTile(self):
        


class World:
    def __init__(self):
        self.tileMap = None

