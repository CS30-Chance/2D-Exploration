from Library import *
from Settings import *

# Game initialization
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])


player = Player(SCREEN, [20, 200], 7)
enemy_flying_eye = Enemy_FlyingEye(SCREEN, [400, 200], 5)



# Game running area
RUN = True
while RUN:
    # Set game FPS
    CLOCK.tick(FPS)

    # Draw Background
    drawBackground(SCREEN, GREY)


    # Temp Ground
    drawLine(SCREEN, BLACK, [0, WINDOW_HEIGHT - 100], [WINDOW_WIDTH, WINDOW_HEIGHT - 100], 2)

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
