import pygame
import csv
import json
from Settings import *


def drawBackground(surface, backgrounds, H_scrollValue=0, V_scrollValue=0):
    """Fill Background (TEST USE !!!)"""


    for index, i in enumerate(backgrounds):
        pic = pygame.transform.scale(i, (WINDOW_WIDTH * 1.5, WINDOW_HEIGHT * 1.5))
        surface.blit(pic, (0 + index * H_scrollValue,
                           -pic.get_height() / 3 + index * V_scrollValue * 0.2))
    return None


def drawLine(surface, color, start: [int, int], end: [int, int], lineWidth: int):
    """Draw line on surface"""
    pygame.draw.line(surface, color, start, end, lineWidth)
    return None


def getImage(src, frame, width, height, scale, colorKey=None, vertical_offset=0):
    """For loadSprite function"""
    # srcImage = pygame.image.load(src)
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(src, (0, 0), (frame * width, vertical_offset * height, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    if colorKey is not None:
        image.set_colorkey(colorKey)

    return image


def loadSprite(file, width: int, height: int, frameCount: int, scale, colorKey=None, vertical_offset=0):
    """Load sprite from spriteSheet to list"""
    sprite = []
    for f in range(frameCount):
        frame = getImage(file, f, width, height, scale, colorKey, vertical_offset).convert_alpha()
        sprite.append(frame)
    return sprite


def saveEntity(player, enemyList):
    """Save player as JSON"""
    playerInfo = {
        'position': [player.rect.center[0]/TILE_SIZE,
                     player.rect.center[1]/TILE_SIZE],
        'speed': player.speed,
        'exp': player.EXP
    }

    enemyInfo = []
    for e in enemyList:
        temp = {
            'type': e.type,
            'position': [e.rect.center[0]/TILE_SIZE,
                         e.rect.center[1]/TILE_SIZE],
            'speed': e.speed,
            'moveRange': [e.wayPoint[0]/TILE_SIZE,
                          e.wayPoint[1]/TILE_SIZE]

        }
        enemyInfo.append(temp)

    Dict = {'player': playerInfo,
            'enemy': enemyInfo}

    return Dict

def writeText(Text: str, Pos: list[int], Color, fontSize=20):
    """Create text"""
    font = pygame.font.Font('freesansbold.ttf', fontSize)
    text = font.render(Text, True, Color)
    textRect = text.get_rect()
    textRect.center = Pos
    return text, textRect

class SpriteEntity(pygame.sprite.Sprite):
    def __init__(self, surface, position: [int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.animationList = []
        self.animationCoolDown = 70
        self.lastFrame = pygame.time.get_ticks()

        self.frameIndex = 0
        self.colorKey = BLACK
        self.flip = False
        self.actionState = 0

        self.position = [position[0] * TILE_SIZE, position[1] * TILE_SIZE]
        self.direction = 1
        self.moveRight = False
        self.moveLeft = False

        self.image = None
        self.rect = None

        self.mask = None
        self.maskImage = None

    def loadSpriteSheet(self):
        self.image = self.animationList[self.actionState][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.mask = pygame.mask.from_surface(self.image)
        self.maskImage = self.mask.to_surface()
        self.maskImage.set_colorkey(self.colorKey)

    def updateMask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.maskImage = self.mask.to_surface()
        self.maskImage.set_colorkey(BLACK)

    def maskCollisionDetection(self, Obstacle):
        """Detect collision between object, must be sprite class"""
        x_overlap = Obstacle.rect.x - self.rect.x
        y_overlap = Obstacle.rect.y - self.rect.y
        # Detect rect collision first for optimization
        if pygame.Rect.colliderect(self.rect, Obstacle.rect):
            if self.mask.overlap(Obstacle.mask, (x_overlap, y_overlap)):
                return True
        return False

    def updateActionState(self, newState):
        if self.actionState != newState:
            self.frameIndex = 0
            self.actionState = newState


class HealthBar:
    def __init__(self, Entity, rect):
        self.entity = Entity
        self.surface = self.entity.surface

        self.outlineColor = BLACK
        self.baseColor = RED
        self.lineWidth = 3
        self.rect = pygame.rect.Rect(rect)

        self.heartImg = pygame.image.load('Assets/heart.png').convert_alpha()
        self.heartImg = pygame.transform.scale_by(self.heartImg, [3, 3])
        self.heartImg.set_colorkey(WHITE)
        self.heartRect = self.heartImg.get_rect()

        # self.healthBarImg = pygame.transform.scale_by(self.healthBarImg, [self.scale, self.scale])

    def drawBase(self):
        width = self.rect.w
        widthModifier = self.entity.health / self.entity.maxHealth
        width *= widthModifier
        pygame.draw.rect(self.entity.surface, self.baseColor, [self.rect.x, self.rect.y, width, self.rect.h])

    def drawOutline(self):
        pygame.draw.rect(self.entity.surface, self.outlineColor, self.rect, self.lineWidth)

    def drawHeart(self):
        self.heartRect.center = [self.rect.x, self.rect.centery]

        self.surface.blit(self.heartImg, self.heartRect)

    def draw(self):
        self.drawBase()
        self.drawOutline()
        self.drawHeart()
