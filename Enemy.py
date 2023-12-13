from Library import *

class Enemy_FlyingEye(SpriteEntity):
    def __init__(self, surface, position: [int, int], speed):
        SpriteEntity.__init__(self, surface, position)

        self.speed = speed
        self.health = 70

        self.flightSpriteSheetPNG = pygame.image.load('Assets/Monster/Flying eye/Flight.png')
        self.takeHitSpriteSheetPNG = pygame.image.load('Assets/Monster/Flying eye/Take Hit.png')

        # load flight animation
        self.animationList.append(
            loadSprite(self.flightSpriteSheetPNG, 150, 150, 8, 1, BLACK))

        # load takeHit animation
        self.animationList.append(
            loadSprite(self.takeHitSpriteSheetPNG, 150, 150, 4, 1, BLACK))


        self.loadSpriteSheet()

        self.actions = {
            'idle': 0,
            'takeHit': 1,
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
                # self.animationCycle += 1


                # todo enemy attacking animation check
                if self.actionState == self.actions['takeHit']:
                    self.updateActionState(self.actions['idle'])

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
