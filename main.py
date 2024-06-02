import random
import pygame


def snap(snap_pos):
    return 50 * round(snap_pos / 50)


pygame.init()

screen = pygame.display.set_mode((500, 450))
clock = pygame.time.Clock()
deltaTime = 0

player_x = 100
player_y = 200
x_velocity = 0
y_velocity = 0

speed = 2
tick = 0

x_positions = [25, 75, 125, 175, 225, 275, 325, 375, 425, 475]
y_positions = [25, 75, 125, 175, 225, 275, 325, 375, 425]

fruits = []

allowed = False

tails = [(player_x, player_y), (player_x - 50, player_y), (
player_x - 100, player_y)]  #, (player_x - 150, player_y), (player_x - 200, player_y), (player_x - 250, player_y)]

# 0             - 50              = -50 = LEFT
# (len(tails) - 1) - (len(tails) - 2) < 0

class Res(Exception): pass

running = True
while running:
    # EVENTS
    tick += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # DRAW BACKGROUND
    for x in range(6):
        for y in range(10):
            pygame.draw.rect(screen, "#deeced", pygame.Rect(x * 50 * 2 + 50, y * 50 * 2, 50, 50))
            pygame.draw.rect(screen, "#deeced", pygame.Rect(x * 50 * 2, y * 50 * 2 + 50, 50, 50))

    for x in range(6):
        for y in range(10):
            pygame.draw.rect(screen, "#d1e4e6", pygame.Rect(x * 50 * 2 + 50, y * 50 * 2 + 50, 50, 50))
            pygame.draw.rect(screen, "#d1e4e6", pygame.Rect(x * 50 * 2, y * 50 * 2, 50, 50))

    # CREATE FOOD
    if len(fruits) < 5:
        random_pos = (random.choice(x_positions), random.choice(y_positions))
        while True:
            try:
                for i in tails:
                    if random_pos == i:
                        raise Res

                break
            except Res:
                random_pos = (random.choice(x_positions), random.choice(y_positions))
                continue
        fruits.append(random_pos)


    for pos in fruits:
        pygame.draw.circle(screen, "red", pos, 25)

    # CONTROLS
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and y_velocity == 0 and allowed:
        allowed = False
        x_velocity = 0
        y_velocity = -speed
    if keys[pygame.K_DOWN] and y_velocity == 0 and allowed:
        allowed = False
        x_velocity = 0
        y_velocity = speed
    if keys[pygame.K_LEFT] and x_velocity == 0 and allowed:
        allowed = False
        x_velocity = -speed
        y_velocity = 0
    if keys[pygame.K_RIGHT] and x_velocity == 0 and allowed:
        allowed = False
        x_velocity = speed
        y_velocity = 0

    # MOVEMENT
    if x_velocity == 0:
        player_x = snap(player_x)
    elif y_velocity == 0:
        player_y = snap(player_y)

    # CREATE TAIL
    if x_velocity != 0 or y_velocity != 0:
        for i in range(len(tails) - 1, 0, -1):
            if i != 0:
                if tick == 10:
                    pygame.draw.rect(screen, "#ecd613", pygame.Rect(tails[i - 1][0], tails[i - 1][1], 50, 50))
                    tails[i] = (tails[i - 1][0], tails[i - 1][1])
                else:
                    pygame.draw.rect(screen, "#ecd613", pygame.Rect(tails[i][0], tails[i][1], 50, 50))

    tails[0] = (player_x, player_y)
    pygame.draw.rect(screen, "#ecd613", pygame.Rect(tails[0][0], tails[0][1], 50, 50))

    # CHECKS
    for i in fruits:
        if snap(player_x) + 25 == i[0] and snap(player_y) + 25 == i[1]:
            fruits.remove(i)
            tails.append((tails[len(tails) - 1][0], tails[len(tails) - 1][1]))

    if player_x > 475 or player_y > 425 or player_x < 0 or player_y < 0:
        break

    if tick == 10:
        allowed = True
        player_x += x_velocity * 25
        player_y += y_velocity * 25
        tick = 0

        if x_velocity != 0 or y_velocity != 0:
            for i in tails:
                if player_x == i[0] and player_y == i[1]:
                    exit(0)

    # FRAME
    pygame.display.flip()
    deltaTime = clock.tick(60) / 1000

pygame.quit()
