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


def getImage(src, frame, width, height, scale, colorKey, vertical_offset=0):
    """For loadSprite function"""
    srcImage = pygame.image.load(src)
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(srcImage, (0, 0), (frame * width, vertical_offset * height, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colorKey)
    return image


def loadSprite(file: str, width: int, height: int, frameCount: int, scale, colorKey, vertical_offset=0):
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
        self.animationState = None
        self.animationCoolDown = 70
        self.lastFrame = pygame.time.get_ticks()
        self.frameIndex = 0

        self.colorKey = BLACK

        self.position = position
        self.direction = 1
        self.moveRight = False
        self.moveLeft = False
        self.flip = False

        self.actionState = 0

        self.image = None
        self.rect = None
        # self.rect.center = None

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

    def updateAnimation(self):
        if self.moveLeft or self.moveRight:
            self.actionState = 1
            self.animationCoolDown = 90
        else:
            self.actionState = 0
            self.animationCoolDown = 70

        self.image = self.animationList[self.actionState][self.frameIndex]
        if pygame.time.get_ticks() - self.lastFrame >= self.animationCoolDown:
            self.lastFrame = pygame.time.get_ticks()
            self.frameIndex += 1
            if self.frameIndex + 1 >= len(self.animationList[self.actionState]):
                self.frameIndex = 0

        

class Player(SpriteEntity):
    def __init__(self, Surface, Position: [int, int], Speed):
        SpriteEntity.__init__(self, Surface, Position)

        self.maxHealth = 100
        self.health = self.maxHealth
        self.speed = Speed

        # Load idle and run sprite into animation list
        self.animationList.append(
            loadSprite('Assets/fire_knight/spritesheets/SpriteSheet.png',
                       288, 128, 8, 1.5, BLACK))

        self.animationList.append(
            loadSprite('Assets/fire_knight/spritesheets/SpriteSheet.png',
                       288, 128, 8, 1.5, BLACK, 1))

        # Load other animation properties
        self.loadSpriteSheet()

    def updateMask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.maskImage = self.mask.to_surface()
        self.maskImage = pygame.transform.flip(self.maskImage, self.flip, False)
        self.maskImage.set_colorkey(BLACK)



    def move(self):
        dx = 0
        dy = 0

        if self.moveLeft:
            dx -= self.speed
            self.flip = True
            self.direction = -1

        if self.moveRight:
            dx += self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        self.updateMask()
        self.updateAnimation()
        self.move()
        self.draw()


    def draw(self):

        # Flip sprite when needed
        img = pygame.transform.flip(self.image, self.flip, False)
        # TODO Fix hitbox/Rect, create dynamic hitbox

        # draw image to screen
        self.surface.blit(img, self.rect)

        # draw mask
        # self.surface.blit(self.maskImage, (self.rect.x, self.rect.y))


        pygame.draw.rect(self.surface, 'green', self.rect, 1)











