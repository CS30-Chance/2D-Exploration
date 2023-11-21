import pygame

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
    player.update()
    enemy_flying_eye.update()
    player.collisionDetection(enemy_flying_eye.mask,
                              enemy_flying_eye.rect.x - player.rect.x,
                              enemy_flying_eye.rect.y - player.rect.y
                              )
    pygame.draw.circle(SCREEN, 'green', [player.rect.x, player.rect.y], 5)


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
                print('jump')

        if event.type == pygame.MOUSEBUTTONDOWN:
            print('attack')


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moveLeft = False
            if event.key == pygame.K_d:
                player.moveRight = False


    # Update game window
    pygame.display.update()

pygame.quit()
