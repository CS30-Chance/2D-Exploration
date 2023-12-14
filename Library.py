import pygame
from Settings import *


def drawBackground(surface, color):
    """Fill Background (TEST USE !!!)"""

    surface.fill(color)
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

        # number of cycles current animation has been run
        # note is animation cycle needed????
        # self.animationCycle = 0

        self.position = [position[0] * TILE_SIZE, position[1] * TILE_SIZE]
        self.direction = 1
        self.moveRight = False
        self.moveLeft = False

        self.image = None
        self.rect = None

        self.mask = None
        self.maskImage = None
        # self.maskImage.set_colorkey(self.colorKey)

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
            # self.animationCycle = 0
            self.frameIndex = 0
            self.actionState = newState
