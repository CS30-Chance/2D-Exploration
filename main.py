from World import pygame, json
from World import WINDOW_WIDTH, WINDOW_HEIGHT, Tiles, FPS
from World import drawBackground, HealthBar, saveEntity, writeText, WHITE
from World import World

# Game initialization
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
# backgrounds
Background = []
# load all background layers
for b in range(11):
    pic = pygame.image.load(f'Assets/Background layers/{b}.png').convert_alpha()
    Background.append(pic)

# create world
world = World(SCREEN)

# LEVEL_HEIGHT = len(world.tilesList) * TILE_SIZE
# LEVEL_WIDTH = len(world.tilesList[0]) * TILE_SIZE
# print(LEVEL_HEIGHT, LEVEL_WIDTH)
GroundTiles = world.buildGround()
Tiles.extend(GroundTiles)


# screen scrolling value
scroll = 0
scrollLeft = False
scrollRight = False


player = world.loadPlayer(SCREEN)
# create health bar
playerHealthBar = HealthBar(player, [30, 20, 200, 30])
playerExp = writeText(str(player.EXP), [900, 40], WHITE)

# create enemies
Enemy = world.loadEnemy(SCREEN)


# Game running area
RUN = True
while RUN:
    # Set game FPS
    CLOCK.tick(FPS)

    # note print test area
    # print('player access point', id(player.enemyList))
    # print(player.EXP)

    # Draw Background
    drawBackground(SCREEN, Background,
                   H_scrollValue=player.x_shift * 0.01,
                   V_scrollValue=player.y_shift * 0.005)

    # Draw Ground
    for ground in GroundTiles:
        ground.drawGround(x_modifier=player.x_shift, y_modifier=player.y_shift)

    # update player and player enemyList
    player.update()
    player.enemyList = Enemy

    for index, e in enumerate(Enemy):
        # note enemy shift
        e.update(x_modifier=player.x_shift, y_modifier=player.y_shift)
        # kill enemy
        if not e.alive:
            # gain EXP
            player.EXP += e.EXP
            Enemy.pop(index)


    # UI
    playerHealthBar.draw()
    playerExp = writeText(str(player.EXP), [900, 40], WHITE)
    SCREEN.blit(playerExp[0], playerExp[1])

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameInfo = saveEntity(player, Enemy)
            with open('gameFile.json', 'w') as JsonFile:
                json.dump(gameInfo, JsonFile, ensure_ascii=False, indent=4)
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
