from Library import *
from Settings import *

# Game initialization
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])





test_fun()






# Game running area
RUN = True
while RUN:

    # Set game FPS
    CLOCK.tick(Settings.FPS)

    # Draw Background
    drawBackground(SCREEN, GREY)


    # Temp Ground
    drawLine(SCREEN, BLACK, [0, WINDOW_HEIGHT - 100], [WINDOW_WIDTH, WINDOW_HEIGHT - 100], 2)



    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    # Update game window
    pygame.display.update()

pygame.quit()
