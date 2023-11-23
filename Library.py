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
        self.animationCycle = 0

        self.position = position
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
            pygame.draw.rect(self.surface, BLUE, [0, 0, 50, 50])
            if self.mask.overlap(Obstacle.mask, (x_overlap, y_overlap)):
                return True
        return False

    def updateActionState(self, newState):
        if self.actionState != newState:
            self.animationCycle = 0
            self.frameIndex = 0
            self.actionState = newState



class Player(SpriteEntity):
    def __init__(self, Surface, Position: [int, int], Speed):
        SpriteEntity.__init__(self, Surface, Position)

        self.maxHealth = 100
        self.health = self.maxHealth
        self.speed = Speed

        # self.animationCoolDown = 1000

        self.jump = False
        self.inAir = False
        self.y_velocity = 0
        self.attacking = False


        self.spriteSheetPNG = pygame.image.load('Assets/fire_knight/spritesheets/SpriteSheet2.png')

        # Load idle into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 8, 1.5, BLACK))

        # Load run into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 8, 1.5, BLACK, 1))

        # Load jump into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 3, 1.5, BLACK, 2))

        # Load attack1 into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 11, 1.5, BLACK, 7))

        # Load airAttack into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 8, 1.5, BLACK, 5))

        # todo add special attack
        # todo add been hit animation
        # todo add death animation

        # Load other animation properties
        self.loadSpriteSheet()

        self.actions = {
            'idle': 0,
            'run': 1,
            'jump': 2,
            'attack1': 3,
            'airAttack': 4,
        }

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

        # add jumping # warning temp
        if self.jump and not self.inAir:
            self.jump = False
            self.inAir = True
            self.y_velocity = -20

        # Gravity
        self.y_velocity += GRAVITY
        if self.y_velocity > 10:
            self.y_velocity = 10

        dy += self.y_velocity

        # Can't move when attack
        if self.attacking:
            dx = 0
            dy = 0

        # note temp ground collision
        if self.rect.bottom + dy > 440:
            dy = 440 - self.rect.bottom
            self.inAir = False

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        # draw image to screen
        self.surface.blit(self.image, self.rect)

        # draw mask
        # self.surface.blit(self.maskImage, (self.rect.x, self.rect.y))

        # draw rect box
        pygame.draw.rect(self.surface, 'green', self.rect, 1)

    def updateAction(self):
        # Note when attack sequence is interrupt by the jump sequence, attack will restart when landed
        if self.jump:
            # todo add jump and falling animation base on y-velocity
            self.updateActionState(self.actions['jump'])
        elif self.attacking:
            if self.inAir:
                self.updateActionState(self.actions['airAttack'])
            else:
                self.updateActionState(self.actions['attack1'])
        elif self.moveRight or self.moveLeft:
            self.updateActionState(self.actions['run'])
        else:
            self.updateActionState(self.actions['idle'])

    def updateAnimationFrame(self):
        self.image = self.animationList[self.actionState][self.frameIndex]
        if pygame.time.get_ticks() - self.lastFrame >= self.animationCoolDown:
            self.lastFrame = pygame.time.get_ticks()
            self.frameIndex += 1
            if self.frameIndex + 1 > len(self.animationList[self.actionState]):
                self.frameIndex = 0
                self.animationCycle += 1

                # check if is attacking, if so, end after animation ended
                if self.attacking:
                    self.attacking = False
                    self.updateActionState(self.actions['idle'])

                # check if is jumped
                # note use y_velocity to see which jump animation to use up/down
                elif self.actionState is self.actions['jump']:
                    # self.jump = False
                    self.updateActionState(self.actions['idle'])

        # flip sprite when needed
        self.image = pygame.transform.flip(self.image, self.flip, False)


    def update(self):
        self.updateAction()
        self.updateMask()
        self.updateAnimationFrame()
        self.move()
        self.draw()


class Enemy_FlyingEye(SpriteEntity):
    def __init__(self, surface, position: [int, int], speed):
        SpriteEntity.__init__(self, surface, position)

        self.speed = speed

        self.flightSpriteSheetPNG = pygame.image.load('Assets/Monster/Flying eye/Flight.png')

        # load flight animation
        self.animationList.append(
            loadSprite(self.flightSpriteSheetPNG, 150, 150, 8, 1, BLACK))


        self.loadSpriteSheet()

        self.actions = {
            'idle': 1,
        }

    def move(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def updateAnimationFrame(self):
        self.image = self.animationList[self.actionState][self.frameIndex]
        if pygame.time.get_ticks() - self.lastFrame >= self.animationCoolDown:
            self.lastFrame = pygame.time.get_ticks()
            self.frameIndex += 1
            if self.frameIndex + 1 > len(self.animationList[self.actionState]):
                self.frameIndex = 0
                self.animationCycle += 1


                # todo enemy attacking animation check

        # flip sprite when needed
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def draw(self):
        self.surface.blit(self.image, self.rect)

        # self.surface.blit(self.maskImage, self.rect)

        pygame.draw.rect(self.surface, RED, self.rect, 1)


    def update(self):
        self.move()
        self.updateMask()
        self.updateAnimationFrame()
        self.draw()


