from World import *
from Player import Player
from Enemy import *

# Game initialization
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])


player = Player(SCREEN, [2, 4], 7)
enemy_flying_eye = FlyingEye(SCREEN, [7, 7], 5)
enemy_skeleton = Skeleton(SCREEN, [17, 11], 2)



# create world
world = World(SCREEN)
GroundTiles = world.buildGround()
Tiles.extend(GroundTiles)

Enemy.append(enemy_flying_eye)
Enemy.append(enemy_skeleton)

# Game running area
RUN = True
while RUN:
    # Set game FPS
    CLOCK.tick(FPS)

    # Draw Background
    drawBackground(SCREEN, GREY)

    # Draw Ground
    for ground in GroundTiles:
        ground.drawGround()


    # update object that player collide with
    player.WorldObjects = Tiles
    # update enemy list
    player.enemyList = Enemy


    # update player/enemy
    player.update()

    for index, e in enumerate(Enemy):
        e.update()

        # kill enemy
        if not e.alive:
            Enemy.pop(index)

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.moveLeft = True
            if event.key == pygame.K_d:
                player.moveRight = True
            if event.key == pygame.K_f:
                if player.specialAttackCooldownTimer <= 0:
                    # player special attack cool down
                    player.specialAttacking = True
                    player.specialAttackCooldownTimer = player.specialAttackCooldown
            if event.key == pygame.K_SPACE:
                if not player.inAir:
                    player.jump = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            player.attacking = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moveLeft = False
            if event.key == pygame.K_d:
                player.moveRight = False


    # Update game window
    pygame.display.update()

pygame.quit()
