from Library import *

class EnemyClass(SpriteEntity):
    def __init__(self, surface, position: [int, int], speed, movementRange: [int, int]):
        SpriteEntity.__init__(self, surface, position)
        self.alive = True
        self.invincibleFrame = InvincibleFrame
        self.invincibleTimer = self.invincibleFrame

        self.wayPoint = [movementRange[0] * TILE_SIZE, movementRange[1] * TILE_SIZE]

        self.speed = speed
        self.maxHealth = None
        self.health = None
        self.walking = True

        self.actions = {
            'idle': 0,
            'takeHit': 1,
            'death': 2,
            'walk': 3,
        }

    def draw(self, x_modifier=0, y_modifier=0):
        self.surface.blit(self.image, [self.rect.x + x_modifier, self.rect.y + y_modifier, self.rect.w, self.rect.h])

        # self.surface.blit(self.maskImage, self.rect)

        # draw hit box
        pygame.draw.rect(self.surface, RED, self.rect, 1)


    def updateAnimationFrame(self):
        self.image = self.animationList[self.actionState][self.frameIndex]
        if pygame.time.get_ticks() - self.lastFrame >= self.animationCoolDown:
            self.lastFrame = pygame.time.get_ticks()
            self.frameIndex += 1
            if self.frameIndex + 1 > len(self.animationList[self.actionState]):
                self.frameIndex = 0

                if self.actionState == self.actions['takeHit']:
                    # kill enemy if health < 0
                    if self.health <= 0:
                        self.updateActionState(self.actions['death'])
                        return 0

                    self.updateActionState(self.actions['idle'])
                    self.walking = True
                elif self.actionState == self.actions['death']:
                    self.alive = False

        # flip sprite when needed
        self.image = pygame.transform.flip(self.image, self.flip, False)



class FlyingEye(EnemyClass):
    def __init__(self, surface, position: [int, int], speed, movementRange):
        EnemyClass.__init__(self, surface, position, speed, movementRange)

        self.animationScale = 1

        self.maxHealth = 70
        self.health = self.maxHealth

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
        center = self.rect.center
        if self.walking:
            self.updateActionState(self.actions['idle'])
            self.rect.x += self.speed * self.direction
            if center[0] + self.speed * self.direction < self.wayPoint[0] or \
                    center[0] + self.speed * self.direction > self.wayPoint[1]:
                self.direction *= -1
                self.flip = not self.flip

    def update(self, x_modifier=0, y_modifier=0):

        # update invincibleFrame
        self.invincibleTimer -= 1

        self.move()
        self.updateMask()
        self.updateAnimationFrame()
        self.draw(x_modifier, y_modifier)



class Skeleton(EnemyClass):
    def __init__(self, surface, position: [int, int], speed, movementRange):
        EnemyClass.__init__(self, surface, position, speed, movementRange)

        self.animationScale = 1.5

        self.maxHealth = 2
        self.health = self.maxHealth


        self.IdleSpriteSheetPNG = pygame.image.load('Assets/Monster/Skeleton/Idle.png')
        self.takeHitSpriteSheetPNG = pygame.image.load('Assets/Monster/Skeleton/Take Hit.png')
        self.deathSpriteSheetPNG = pygame.image.load('Assets/Monster/Skeleton/Death.png')
        self.walkingSpriteSheetPNG = pygame.image.load('Assets/Monster/Skeleton/Walk.png')

        # load idle animation
        self.animationList.append(
            loadSprite(self.IdleSpriteSheetPNG, 150, 150, 4, self.animationScale, BLACK))

        # load takeHit animation
        self.animationList.append(
            loadSprite(self.takeHitSpriteSheetPNG, 150, 150, 4, self.animationScale, BLACK))

        # load Death animation
        self.animationList.append(
            loadSprite(self.deathSpriteSheetPNG, 150, 150, 4, self.animationScale, BLACK))

        # load Walk animation
        self.animationList.append(
            loadSprite(self.walkingSpriteSheetPNG, 150, 150, 4, self.animationScale, BLACK))

        self.loadSpriteSheet()

    def move(self):
        center = self.rect.center
        if self.walking:
            self.updateActionState(self.actions['walk'])
            self.rect.x += self.speed * self.direction
            if center[0] + self.speed * self.direction < self.wayPoint[0] or \
                    center[0] + self.speed * self.direction > self.wayPoint[1]:
                self.direction *= -1
                self.flip = not self.flip


    def update(self, x_modifier=0, y_modifier=0):
        # update invincibleFrame
        self.invincibleTimer -= 1

        self.move()
        self.updateMask()
        self.updateAnimationFrame()
        self.draw(x_modifier, y_modifier)




