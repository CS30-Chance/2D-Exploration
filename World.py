import pygame
from Settings import *
import csv

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

    def drawGround(self):
        self.surface.blit(self.spritesImage, [self.x, self.y])
        # pygame.draw.rect(self.surface, 'green', self.rect, 1)
        


class World:
    def __init__(self, surface):
        # todo use tile-map csv to load world
        self.tileMapFile = 'TileMap.csv'
        self.surface = surface
        self.tileMap = csv.reader(open(self.tileMapFile, 'r'))
        self.tilesList = []
        self.groundTiles = []

        # load tiles into list
        for y_Pos, r in enumerate(self.tileMap):
            temp = []
            for x_Pos, c in enumerate(r):
                temp.append(c)

                # if is ground tile, add to ground tile list
                if c == '1':
                    self.groundTiles.append([x_Pos, y_Pos])

            self.tilesList.append(temp)

    def buildGround(self):
        ground = []
        for cord in self.groundTiles:
            tempGround = Ground(self.surface, cord[0], cord[1])
            ground.append(tempGround)
        return ground


