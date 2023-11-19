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

class Player(pygame.sprite.Sprite):
    def __init__(self, Surface, Position: [int, int], Speed):
        pygame.sprite.Sprite.__init__(self)
        # self.x = Position[0]
        # self.y = Position[1]
        self.surface = Surface

        self.animationList = []
        self.animationState = ['idle', 'run']
        self.animationCoolDown = 70
        self.lastFrame = pygame.time.get_ticks()
        self.frameIndex = 0

        self.maxHealth = 100
        self.health = self.maxHealth
        self.speed = Speed

        self.direction = 1
        self.moveRight = False
        self.moveLeft = False
        self.flip = False

        self.actionState = 0

        # Load idle and run sprite into animation list
        self.animationList.append(
            loadSprite('Assets/fire_knight/spritesheets/SpriteSheet.png',
                       288, 128, 8, 1.5, BLACK))

        self.animationList.append(
            loadSprite('Assets/fire_knight/spritesheets/SpriteSheet.png',
                       288, 128, 8, 1.5, BLACK, 1))


        self.image = self.animationList[self.actionState][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.width = 93
        self.rect.height = 70
        # self.rect.center = Position


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

    def update(self):
        self.updateAnimation()
        self.move()
        self.draw()


    def draw(self):

        # print(self.image)
        # self.character = pygame.Surface((64, 47))
        # self.character.blit(self.image, (0, 0), (100, 80, 64, 47))
        # print(self.character)
        # self.rect = self.character.get_rect()

        img = pygame.transform.flip(self.image, self.flip, False)
        # TODO Fix hitbox/Rect, create dynamic hitbox
        
        # print(mask)
        self.surface.blit(img, self.rect, [150, 123, 93, 70])
        pygame.draw.rect(self.surface, 'green', self.rect, 1)
        pygame.draw.rect(self.surface, 'red', [150, 123, 93, 70], 1)











