from Library import *

class EnemyClass(SpriteEntity):
    def __init__(self, surface, position: [int, int], speed):
        SpriteEntity.__init__(self, surface, position)


        self.alive = True
        self.invincibleFrame = InvincibleFrame
        self.invincibleTimer = self.invincibleFrame

        self.speed = speed
        self.health = None

        self.actions = {
            'idle': 0,
            'takeHit': 1,
            'death': 2,
        }

    def updateHealth(self):
        if self.health <= 0:
            self.updateActionState(self.actions['death'])


    def draw(self):
        self.surface.blit(self.image, self.rect)

        # self.surface.blit(self.maskImage, self.rect)

        pygame.draw.rect(self.surface, RED, self.rect, 1)


    def updateAnimationFrame(self):
        self.image = self.animationList[self.actionState][self.frameIndex]
        if pygame.time.get_ticks() - self.lastFrame >= self.animationCoolDown:
            self.lastFrame = pygame.time.get_ticks()
            self.frameIndex += 1
            if self.frameIndex + 1 > len(self.animationList[self.actionState]):
                self.frameIndex = 0
                # self.animationCycle += 1

                if self.actionState == self.actions['takeHit']:
                    self.updateActionState(self.actions['idle'])
                elif self.actionState == self.actions['death']:
                    self.alive = False

        # flip sprite when needed
        self.image = pygame.transform.flip(self.image, self.flip, False)



class FlyingEye(EnemyClass):
    def __init__(self, surface, position: [int, int], speed):
        EnemyClass.__init__(self, surface, position, speed)

        self.animationScale = 1

        self.health = 70

        self.flightSpriteSheetPNG = pygame.image.load('Assets/Monster/Flying eye/Flight.png')
        self.takeHitSpriteSheetPNG = pygame.image.load('Assets/Monster/Flying eye/Take Hit.png')
        self.deathSpriteSheetPNG = pygame.image.load('Assets/Monster/Flying eye/Death.png')

        # load flight animation
        self.animationList.append(
            loadSprite(self.flightSpriteSheetPNG, 150, 150, 8, self.animationScale, BLACK))

        # load takeHit animation
        self.animationList.append(
            loadSprite(self.takeHitSpriteSheetPNG, 150, 150, 4, self.animationScale, BLACK))

        # load Death animation
        self.animationList.append(
            loadSprite(self.deathSpriteSheetPNG, 150, 150, 4, self.animationScale, BLACK))

        self.loadSpriteSheet()

    def move(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def update(self):
        self.updateHealth()

        # update invincibleFrame
        self.invincibleTimer -= 1

        self.move()
        self.updateMask()
        self.updateAnimationFrame()
        self.draw()



class Skeleton(EnemyClass):
    def __init__(self, surface, position: [int, int], speed):
        EnemyClass.__init__(self, surface, position, speed)

        self.animationScale = 1.5

        self.health = 150

        self.IdleSpriteSheetPNG = pygame.image.load('Assets/Monster/Skeleton/Idle.png')
        self.takeHitSpriteSheetPNG = pygame.image.load('Assets/Monster/Skeleton/Take Hit.png')
        self.deathSpriteSheetPNG = pygame.image.load('Assets/Monster/Skeleton/Death.png')

        # load idle animation
        self.animationList.append(
            loadSprite(self.IdleSpriteSheetPNG, 150, 150, 4, self.animationScale, BLACK))

        # load takeHit animation
        self.animationList.append(
            loadSprite(self.takeHitSpriteSheetPNG, 150, 150, 4, self.animationScale, BLACK))

        # load Death animation
        self.animationList.append(
            loadSprite(self.deathSpriteSheetPNG, 150, 150, 4, self.animationScale, BLACK))

        self.loadSpriteSheet()


    def update(self):
        self.updateHealth()

        # update invincibleFrame
        self.invincibleTimer -= 1

        self.updateMask()
        self.updateAnimationFrame()
        self.draw()




