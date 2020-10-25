import pygame
import random
import collision
import math

# Init the PyGame
pygame.init()

# Define the screen
screenY = 600
screenX = 800
screen = pygame.display.set_mode((screenX, screenY))
background = pygame.image.load('resources/bg.png')
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('resources/spaceship.png')
pygame.display.set_icon(icon)
font = pygame.font.Font('freesansbold.ttf', 24)

scoreTextX = 5
scoreTextY = 5

# Define player
playerImg = pygame.image.load('resources/sprite.png')
playerDeadImg = pygame.image.load('resources/playerdead.png')
playerHealthImg = pygame.image.load('resources/shield.png')
playerX = 370
playerY = 480
playerX_Change = 0
playerY_Change = 0

# Player attributes
playerMoveSpeed = 1
playerSpriteDim = 64
playerHealth = 5
playerKills = 0
playerScore = 0
playerLastScore = 0
fireMode = 1

healthPosX = []
healthPosy = []

for i in range(playerHealth):
    offsetX = 620
    offsetY = 5
    healthPosX.append(offsetX + ((i + 1) * 30))
    healthPosy.append(offsetY)

# Shot
singleShotImg = pygame.image.load('resources/singleshot.png')
doubleShotImg = pygame.image.load('resources/doubleshot.png')
tripleShotImg = pygame.image.load('resources/tripleshot.png')
shotX = 0
shotY = 0
shotSpeed = 3
shotFired = False

# Define Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []

# Enemy Attributes
enemyAmount = 6
enemySpeed = 0.75
enemySpriteDim = 64
enemyDeadImg = pygame.image.load('resources/enemydead.png')

# Enemy Shot
enemyShotImg = pygame.image.load('resources/enemyshot.png')
enemyShotX = 0
enemyShotY = 0
enemyShotSpeed = 2
enemyShotFired = False

for i in range(enemyAmount):
    enemyImg.append(pygame.image.load('resources/invader.png'))
    enemyX.append(random.randint(0, screenX - 64))
    enemyY.append(30)
    enemyX_Change.append(enemySpeed)
    enemyY_Change.append(30)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def shot(x, y):
    global shotFired
    shotFired = True
    if fireMode == 1:
        screen.blit(singleShotImg, (x, y))
    if fireMode == 2:
        screen.blit(doubleShotImg, (x, y))
    if fireMode == 3:
        screen.blit(tripleShotImg, (x, y))


def enemyShot(x, y):
    global enemyShotFired
    enemyShotFired = True
    screen.blit(enemyShotImg, (x, y))


def enemyDead(x, y, ticks):
    x = 0
    while x < ticks:
        screen.blit(enemyDeadImg, (x, y))
        x + 1


def playerDead(x, y, ticks):
    x = 0
    while x < ticks:
        screen.blit(playerDeadImg, (x, y))
        x + 1


def updateScore(x, y):
    score = font.render("Score: " + str(playerScore), True, (255, 255, 0))
    lastScore = font.render("Previous Score: " + str(playerLastScore), True, (255, 255, 0))
    screen.blit(score, (x, y))
    screen.blit(lastScore, (x, y + 29))


def updateHealth(x, y):
    screen.blit(playerHealthImg, (x, y))


def fireEnemyShot(i):
    if not enemyShotFired:
        global enemyShotX
        global enemyShotY
        enemyShotX = math.ceil(enemyX[i])
        enemyShotY = math.ceil(enemyY[i])
        enemyShot(math.ceil(enemyShotX), math.ceil(enemyShotY))


# Main game loop
running = True
while running:
    screen.fill((0, 0, 32))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():

        # Game exit functionality
        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_Change -= playerMoveSpeed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_Change += playerMoveSpeed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                playerY_Change -= playerMoveSpeed
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                playerY_Change += playerMoveSpeed
            if event.key == pygame.K_SPACE:
                if not shotFired:
                    shotX = playerX
                    shotY = playerY
                    shot(playerX, playerY)
            if event.key == pygame.K_1:
                fireMode = 1
            if event.key == pygame.K_2:
                fireMode = 2
            if event.key == pygame.K_3:
                fireMode = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_Change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                playerY_Change = 0

    # Player movement
    if not playerX + playerX_Change >= screenX - playerSpriteDim and not playerX + playerX_Change < 0:
        playerX += playerX_Change
    if not playerY + playerY_Change >= screenY - playerSpriteDim and not playerY + playerY_Change < 0:
        playerY += playerY_Change

    # Shot Movement
    if shotFired:
        shotY -= shotSpeed
        shot(shotX, shotY)
        if shotY <= -20:
            shotFired = False
    else:
        shotX = playerX
        shotY = playerY

    # Enemy Shot Fired
    if enemyShotFired:
        enemyShotY += enemyShotSpeed
        enemyShot(enemyShotX, enemyShotY)
        if enemyShotY > screenY:
            enemyShotFired = False
            playerScore += 10

    # Enemy movement
    for i in range(enemyAmount):
        if random.randint(1, 100) > 90:
            fireEnemyShot(i)

        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = enemySpeed
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= screenX - enemySpriteDim:
            enemyX_Change[i] = enemySpeed * -1
            enemyY[i] += enemyY_Change[i]

    for i in range(enemyAmount):
        # Collider Checks
        shotCollided = collision.hasCollided(enemyX[i], enemyY[i], shotX, shotY)
        enemyShotCollided = collision.hasCollided(playerX, playerY, enemyShotX, enemyShotY)
        playerCollided = collision.hasCollided(enemyX[i], enemyY[i], playerX, playerY)
        if shotCollided and shotFired:
            shotY = playerY
            shotFired = False
            playerScore += 100
            enemyX[i] = random.randint(0, screenX - 64)
            enemyY[i] = 30

        if playerCollided or enemyShotCollided:
            if enemyShotCollided:
                enemyShotFired = False
                enemyShotY = 30
            playerHealth -= 1
            playerX = 370
            playerY = 480
            if playerHealth <= 0:
                playerHealth = 5
                playerLastScore = playerScore
                playerScore = 0

        enemy(enemyX[i], enemyY[i], i)

    for i in range(playerHealth):
        updateHealth(healthPosX[i], healthPosy[i])

    player(playerX, playerY)
    updateScore(scoreTextX, scoreTextY)
    pygame.display.update()
