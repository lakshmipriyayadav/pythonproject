import pygame
import random
import math
from pygame import mixer

#intialization
pygame.init()


#Create the screen
screen = pygame.display.set_mode((800,600))

#Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#Background
background = pygame.image.load('bacgroundbts.png')
#Caaption and logo
pygame.display.set_caption("BTS ARMY FANS VS BTS HATERS")
icon = pygame.image.load('kpop (3).png')
pygame.display.set_icon(icon)

#PLAYER
armyImage = pygame.image.load('teenager.png')
armyX = 370
armyY = 480
armyX_change = 0


#ENEMY
hatersImage = []
hatersX = []
hatersY = []
hatersX_change = []
hatersY_change = []
num_of_enimies = 6
for i in range (num_of_enimies):
    hatersImage.append(pygame.image.load('ghost.png'))
    hatersX.append(random.randint(0,736))
    hatersY.append(random.randint(50, 150))
    hatersX_change.append(4)
    hatersY_change.append(40)

#ready = we cant see the bullet
#fire = bullet is being fired and is moving

#BULLET
purpleheartImg = pygame.image.load('heart (1).png')
purpleheartX = 50
purpleheartY = 480
purpleheartX_change = 0
purpleheartY_change = 10
purpleheart_state = "ready"

#score
score_value = 0
font =pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#gameover
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = font.render("ARMY WON" , True ,(255,255,255))
    screen.blit(over_text , (200,250))

def show_score(x ,y):
    score = font.render("SCORE:" + str(score_value), True, (255,255,255))
    screen.blit(score, (x , y))

def bullet(x, y):
    global purpleheart_state
    purpleheart_state = "fire"
    screen.blit(purpleheartImg,(x, y))

def player(x, y):
    screen.blit(armyImage, (x,y))


def enemy(x, y , i):
    screen.blit(hatersImage[i], (x,y))


def isCollision(hatersX, hatersY, pupleheartX, purplrheartY):
    distance = math.sqrt(math.pow(hatersX-pupleheartX,2)) + (math.pow(hatersY - purpleheartY,2))
    if distance < 27:
        return True
    else:
        return False
#Game loop
running = True
while running:
    #RGB is red, green ,blue
    screen.fill((255,255,255))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                armyX_change= -4
            if event.key == pygame.K_RIGHT:
                armyX_change= 4
            if event.key == pygame.K_SPACE:
                if purpleheart_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    purpleheartX = armyX
                    bullet(purpleheartX, purpleheartY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                armyX_change = 0

    #5 + 0.5 = 5.5
    #5 += 0.5
    armyX += armyX_change

    if armyX <= 0:
        armyX = 0
    elif armyX >= 736:
        armyX = 736

   #ENEMY MOVEMENT
    for i in range(num_of_enimies):
        #game over
        if hatersY[i] >440:
            for j in range(num_of_enimies):
                hatersY[j] = 2000
            game_over_text()
            break
        hatersX[i] += hatersX_change[i]
        if hatersX[i] <= 0:
           hatersX_change[i]= 0.8
           hatersY[i] += hatersY_change[i]
        elif hatersX[i] >= 736:
           hatersX_change[i] = -0.8
           hatersY[i] += hatersY_change[i]

        # COLLISION
        collision = isCollision(hatersX[i], hatersY[i], purpleheartX, purpleheartY)
        if collision:
           explosionSound = mixer.Sound("explosion.wav")
           explosionSound.play()
           purpleheartY = 480
           purpleheart_state = "ready"
           score_value += 1
           hatersX[i] = (random.randint(0, 736))
           hatersY[i] = (random.randint(50, 150))
        enemy(hatersX[i], hatersY[i], i)

    #BULLET MOVEMENT
    if purpleheartY <= 0:
        purpleheartY = 480
        purpleheart_state = "ready"

    if purpleheart_state == "fire":
        bullet(purpleheartX, purpleheartY)
        purpleheartY -= purpleheartY_change





    player(armyX , armyY)
    show_score(textX ,textY)
    pygame.display.update()