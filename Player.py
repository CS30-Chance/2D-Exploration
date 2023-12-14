from Library import *


class Player(SpriteEntity):
    def __init__(self, Surface, Position: [int, int], Speed):
        SpriteEntity.__init__(self, Surface, Position)

        self.maxHealth = 100
        self.health = self.maxHealth
        self.speed = Speed

        self.WorldObjects = None
        self.enemyList = []

        # self.animationCoolDown = 1000

        self.jump = False
        self.inAir = False
        self.y_velocity = 0
        self.attacking = False
        self.specialAttacking = False
        self.specialAttackDamage = 50

        self.specialAttackCooldown = 200
        self.specialAttackCooldownTimer = 0

        self.baseAttackDamage = 20

        # Create hitBox
        self.hitBoxWidth = 50
        self.hitBoxHeight = 70
        self.hitBox = pygame.rect.Rect([self.position[0], self.position[1], self.hitBoxWidth, self.hitBoxHeight])


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

        # Load fall into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 3, 1.5, BLACK, 3))

        # Load attack1 into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 11, 1.5, BLACK, 7))

        # Load airAttack into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 8, 1.5, BLACK, 5))

        # Load specialAttack into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 18, 1.5, BLACK, 10))

        # Load takeHit into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 6, 1.5, BLACK, 12))

        # Load death into animation list
        self.animationList.append(
            loadSprite(self.spriteSheetPNG, 288, 128, 12, 1.5, BLACK, 14))

        # Load other animation properties
        self.loadSpriteSheet()

        self.actions = {
            'idle': 0,
            'run': 1,
            'jump': 2,
            'fall': 3,
            'attack1': 4,
            'airAttack': 5,
            'specialAttack': 6,
            'takeHit': 7,
            'death': 8,
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

        # add jumping
        if self.jump and not self.inAir:
            self.jump = False
            self.inAir = True
            self.y_velocity = -20

        # Gravity
        self.y_velocity += GRAVITY
        if self.y_velocity > 10:
            self.y_velocity = 10

        dy += self.y_velocity

        # note Can't move when attack
        if self.attacking or self.specialAttacking:
            dx = 0
            dy = 0


        for element in self.WorldObjects:
            dx, dy = self.collisionDetection(element, dx, dy)


        self.rect.x += dx
        self.rect.y += dy

    def collisionDetection(self, Object, dx, dy):
        distanceX = dx
        distanceY = dy

        # dx section
        DeltaHitBox = pygame.Rect(self.hitBox)
        # print('original hb', DeltaHitBox)
        DeltaHitBox.x += dx
        # print('hb + dx', DeltaHitBox)
        # warning is also changes hitbox
        # Check horizontal collision
        if pygame.Rect.colliderect(DeltaHitBox, Object.rect):
            if self.hitBox.x < Object.rect.x:
                distanceX = Object.rect.left - self.hitBox.right
            elif self.hitBox.x > Object.rect.x:
                distanceX = Object.rect.right - self.hitBox.left

        # vertical section
        DeltaHitBox = pygame.Rect(self.hitBox)
        DeltaHitBox.y += dy
        # Check vertical collision
        if pygame.Rect.colliderect(DeltaHitBox, Object.rect):
            if self.hitBox.y < Object.rect.y:
                self.inAir = False  # landed
                distanceY = Object.rect.top - self.hitBox.bottom
            elif self.hitBox.y > Object.rect.y:
                self.y_velocity = 0  # reset y velocity d
                distanceY = Object.rect.bottom - self.hitBox.top


        return distanceX, distanceY


    def updateAction(self):
        if self.inAir:
            if self.attacking:
                self.updateActionState(self.actions['airAttack'])
            elif self.y_velocity < 0:
                self.updateActionState(self.actions['jump'])
            else:
                self.updateActionState(self.actions['fall'])
        elif self.specialAttacking:
            self.updateActionState(self.actions['specialAttack'])
        elif self.attacking:
            self.updateActionState(self.actions['attack1'])
        elif self.moveRight or self.moveLeft:
            self.updateActionState(self.actions['run'])
        else:
            self.updateActionState(self.actions['idle'])

    def dealingDamage(self, enemy):
        if self.maskCollisionDetection(enemy):
            if self.specialAttacking:
                return self.specialAttackDamage
            elif self.attacking:
                return self.baseAttackDamage
        return 0

    def attack(self, enemyList):
        for enemy in enemyList:
            damage = self.dealingDamage(enemy)
            if damage != 0:
                if enemy.invincibleTimer <= 0:
                    enemy.health -= damage
                    enemy.updateActionState(enemy.actions['takeHit'])
                    enemy.invincibleTimer = enemy.invincibleFrame

    def updateAnimationFrame(self):
        self.image = self.animationList[self.actionState][self.frameIndex]
        if pygame.time.get_ticks() - self.lastFrame >= self.animationCoolDown:
            self.lastFrame = pygame.time.get_ticks()
            self.frameIndex += 1
            if self.frameIndex + 1 > len(self.animationList[self.actionState]):
                self.frameIndex = 0
                # self.animationCycle += 1

                # check if is attacking, if so, end after animation ended
                if self.attacking or self.specialAttacking:
                    self.attacking = False
                    self.specialAttacking = False
                    self.updateActionState(self.actions['idle'])

        # flip sprite when needed
        self.image = pygame.transform.flip(self.image, self.flip, False)


    def draw(self):
        # draw image to screen
        self.surface.blit(self.image, self.rect)

        # draw mask
        # self.surface.blit(self.maskImage, (self.rect.x, self.rect.y))

        # draw rect box
        pygame.draw.rect(self.surface, GREEN, self.rect, 1)

        # draw hitBox
        pygame.draw.rect(self.surface, BLUE, self.hitBox, 1)


    def update(self):
        # note decrease special attack cool down
        self.specialAttackCooldownTimer -= 1

        # update hitBox
        self.hitBox.bottom = self.rect.bottom
        self.hitBox.centerx = self.rect.centerx

        self.updateAction()
        self.updateMask()
        self.updateAnimationFrame()
        self.attack(self.enemyList)
        self.move()
        self.draw()
