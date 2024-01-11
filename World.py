from Library import *
from Enemy import FlyingEye, Skeleton
from Player import Player


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

    def drawGround(self, x_modifier=0, y_modifier=0):
        # sync rect x and y
        self.rect.x = self.x
        self.rect.y = self.y
        self.surface.blit(self.spritesImage, [self.x + x_modifier, self.y + y_modifier])
        # pygame.draw.rect(self.surface, 'green', self.rect, 1)



class World:
    def __init__(self, surface):
        self.tileMapFile = 'TileMap.csv'
        self.surface = surface
        self.tileMap = csv.reader(open(self.tileMapFile, 'r'))
        self.tilesList = []
        self.groundTiles = []
        self.levelHeight = None
        self.levelWidth = None

        self.gameCharacterInfo = json.load(gameINFO)
        self.playerInfo = self.gameCharacterInfo['player']
        self.enemyInfo = self.gameCharacterInfo['enemy']

        # load tiles into list
        for y_Pos, r in enumerate(self.tileMap):
            temp = []
            for x_Pos, c in enumerate(r):
                temp.append(c)

                # if is ground tile, add to ground tile list
                if c == '1':
                    self.groundTiles.append([x_Pos, y_Pos])

            self.tilesList.append(temp)

        # calculate level width and height
        self.levelHeight = len(self.tilesList) * TILE_SIZE
        self.levelWidth = len(self.tilesList[0]) * TILE_SIZE

    def buildGround(self):
        ground = []
        for cord in self.groundTiles:
            tempGround = Ground(self.surface, cord[0], cord[1])
            ground.append(tempGround)
        return ground


    def loadPlayer(self, Surface):
        playerPos = self.playerInfo['position']
        playerSpeed = self.playerInfo['speed']
        return Player(Surface, playerPos, playerSpeed)

    def loadEnemy(self, Surface):
        enemyList = []
        for e in self.enemyInfo:
            enemyType = e['type']
            enemyPos = e['position']
            enemySpeed = e['speed']
            enemyRange = e['moveRange']

            if enemyType == 'f':
                enemy = FlyingEye(Surface, enemyPos, enemySpeed, enemyRange)
            else:
                enemy = Skeleton(Surface, enemyPos, enemySpeed, enemyRange)

            enemyList.append(enemy)
        return enemyList


