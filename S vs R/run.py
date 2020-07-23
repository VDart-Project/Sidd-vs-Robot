# Imports
import pygame
from pygame import mixer
import random
import math


pygame.init()

screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')
instruc = pygame.image.load('howto.png')
warehouse = pygame.image.load('factory.png')
game_over = pygame.image.load('over.png')

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title & icon
pygame.display.set_caption("Dino Run")
icon = pygame.image.load('fossil.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('person.png')
playerx = 50
playery = 200
playery_change = 0

# Enemies
# Enemy1
cactusimg = []
cactusx = []
cactusy = []
cactusx_change = []
num_of_cactus = 4

for i in range(num_of_cactus):
    cactusimg.append(pygame.image.load('rob.png'))
    cactusx.append(random.randint(400, 736))
    cactusy.append(random.randint(100, 450))
    cactusx_change.append(3)

# Enemy2
robotimg = []
robotx = []
roboty = []
robotx_change = []
num_of_robot = 4

for i in range(num_of_robot):
    robotimg.append(pygame.image.load('robt.png'))
    robotx.append(random.randint(400, 736))
    roboty.append(random.randint(100, 450))
    robotx_change.append(3)

# Vdart logo bullet
fireimg = pygame.image.load('logo.png')
firex = 0
firey = 200
firex_change = 50
firey_change = 0
fire_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10


def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def cactus(x, y, i):
    screen.blit(cactusimg[i], (x, y))


def robot(x, y, i):
    screen.blit(robotimg[i], (x, y))


def fire_fire(x, y):
    global fire_state
    fire_state = "fire"
    screen.blit(fireimg, (x + 16, y + 10))


def iscollision(robotx, roboty, firex, firey):
    distance = math.sqrt((math.pow(robotx - firex, 2)) + (math.pow(roboty - firey, 2)))
    if distance < 35:
        return True
    else:
        return False


def ifcollision(cactusx, cactusy, firex, firey):
    distance = math.sqrt((math.pow(cactusx - firex, 2)) + (math.pow(cactusy - firey, 2)))
    if distance < 35:
        return True
    else:
        return False


running = True
starting = True
second = False
game = False
over = False

while running:

    while starting:
        screen.fill((128, 128, 128))
        screen.blit(background, (0, 0))

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starting = False
                pygame.quit()
                quit()
        first = pygame.key.get_pressed()

        if first[pygame.K_p]:
            second = True
            starting = False
        pygame.display.update()

    while second:
        screen.fill((128, 128, 128))
        screen.blit(instruc, (0, 0))

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                second = False
                pygame.quit()
                quit()
        play = pygame.key.get_pressed()

        if play[pygame.K_a]:
            game = True
            second = False
        pygame.display.update()

    while game:
        screen.fill((128, 128, 128))

        screen.blit(warehouse, (0, 0))

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()
                quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playery_change = -8
                if event.key == pygame.K_DOWN:
                    playery_change = +8
                if event.key == pygame.K_SPACE:
                    if fire_state == "ready":
                        bullet_sound = mixer.sound('laser.wav')
                        bullet_sound.play()
                        firey = playery
                        fire_fire(firex, firey)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playery_change = 0

        playery += playery_change

        if playery <= 100:
            playery = 100
        elif playery >= 450:
            playery = 450

        if firex >= 800:
            firex = 150
            fire_state = "ready"

        if fire_state == "fire":
            fire_fire(firex, firey)
            firex += firex_change

        collision = iscollision(firex, firey, cactusx[i], cactusy[i], )
        if collision:
            firex = 150
            fire_state = "ready"
            score_value += 1
            cactusx[i] = random.randint(400, 736)
            cactusy[i] = random.randint(100, 450)


            cactusx[i] += cactusx_change[i]

            cactusx_change[i] = -2.4
            collision = iscollision(firex, firey, cactusx[i], cactusy[i], )
            if collision:
                collision_sound = mixer.Sound('explosive.wav')
                collision_sound.play()
                firex = 150
                fire_state = "ready"
                score_value += 1
                cactusx[i] = random.randint(400, 736)
                cactusy[i] = random.randint(100, 450)
            cactus(cactusx[i], cactusy[i], i)

        explosion = ifcollision(firex, firey, robotx[i], roboty[i], )
        if explosion:
            firex = 150
            fire_state = "ready"
            score_value += 1
            robotx[i] = random.randint(400, 736)
            roboty[i] = random.randint(100, 450)

            robotx[i] += robotx_change[i]

            robotx_change[i] = -2.4
            explosion = ifcollision(firex, firey, robotx[i], roboty[i], )
            if explosion:
                collision_sound = mixer.sound('explosive.wav')
                collision_sound.play()
                firex = 150
                fire_state = "ready"
                score_value += 1
                robotx[i] = random.randint(400, 736)
                roboty[i] = random.randint(100, 450)
            robot(robotx[i], roboty[i], i)

            for i in range(num_of_cactus) and range(num_of_robot):
                if cactusx[i] < 50 or robotx[i] < 50:
                    for j in range(num_of_cactus) and range(num_of_robot):
                        cactusx[j] = 2000
                        robotx[j] = 2000
                        over = True
                        game = False
                    break

        player(playerx, playery)
        show_score(textx, texty)
        pygame.display.update()

    while over:
        screen.fill((128, 128, 128))
        screen.blit(game_over, (0, 0))

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starting = False
                pygame.quit()
                quit()
        again = pygame.key.get_pressed()

        if again[pygame.K_t]:
            starting = True

            over = False
        pygame.display.update()
