import pygame

from Library import *
from Settings import *

# Game initialization
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])


player = Player(SCREEN, [20, 200], 7)



# Game running area
RUN = True
while RUN:

    # Set game FPS
    CLOCK.tick(FPS)

    # Draw Background
    drawBackground(SCREEN, GREY)


    # Temp Ground
    drawLine(SCREEN, BLACK, [0, WINDOW_HEIGHT - 100], [WINDOW_WIDTH, WINDOW_HEIGHT - 100], 2)
    pygame.draw.rect(SCREEN, BLACK, [20, 200, 10, 10])
    player.update()


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
