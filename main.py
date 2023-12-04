from World import *
from Player import Player
from Enemy import *

# Game initialization
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])


player = Player(SCREEN, [20, 200], 7)
enemy_flying_eye = Enemy_FlyingEye(SCREEN, [400, 200], 5)

testTile1 = Ground(SCREEN, 5, 5)
testTile2 = Ground(SCREEN, 6, 5)
testTile3 = Ground(SCREEN, 4, 4)
testTile4 = Ground(SCREEN, 8, 7)
testTile5 = Ground(SCREEN, 20, 10)

Tiles = [testTile1, testTile2, testTile3, testTile4, testTile5]


# Game running area
RUN = True
while RUN:
    # Set game FPS
    CLOCK.tick(FPS)

    # Draw Background
    drawBackground(SCREEN, GREY)


    # Temp Ground
    drawLine(SCREEN, BLACK, [0, WINDOW_HEIGHT - 100], [WINDOW_WIDTH, WINDOW_HEIGHT - 100], 2)
    for tiles in Tiles:
        tiles.drawTile()

    # note update object that player collide with
    player.WorldObjects = Tiles


    # update player/enemy
    player.update()
    enemy_flying_eye.update()

    if player.maskCollisionDetection(enemy_flying_eye):
        pygame.draw.rect(SCREEN, RED, [0, 0, 50, 50])



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
                if player.specialAttackCooldown <= 0:
                    player.specialAttacking = True
                    # warning maybe use other cool down function
                    player.specialAttackCooldown = 200
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
