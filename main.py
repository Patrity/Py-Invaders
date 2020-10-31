import pygame
from enum import IntEnum

import json
import pygame_textinput
import random
import collision
import math
import highscores

# Init the PyGame
pygame.init()
input = pygame_textinput.TextInput("Player Name")
clock = pygame.time.Clock()
game_started = False

# Define the screen
screen_y = 600
screen_x = 800
screen = pygame.display.set_mode((screen_x, screen_y))
background = pygame.image.load('resources/bg.png')
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('resources/spaceship.png')
pygame.display.set_icon(icon)
font = pygame.font.Font('freesansbold.ttf', 24)
banner = pygame.image.load('resources/banner.png')
start_button = pygame.image.load('resources/start.png')
high_score_button = pygame.image.load('resources/trophy.png')
github_buttom = pygame.image.load('resources/github.png')

score_text_X = 5
score_text_y = 5

# Define player
player_img = pygame.image.load('resources/sprite.png')
player_dead_img = pygame.image.load('resources/playerdead.png')
player_health_img = pygame.image.load('resources/shield.png')
player_x = 370
player_y = 480
playerX_Change = 0
playerY_Change = 0
player_name = "player"

# Player attributes
player_move_speed = 10
player_sprite_dim = 64
player_health = 5
player_kills = 0
player_score = 0
player_last_score = 0
fire_mode = 1

health_pos_x = []
health_pos_y = []

for i in range(player_health):
    offsetX = 620
    offsetY = 5
    health_pos_x.append(offsetX + ((i + 1) * 30))
    health_pos_y.append(offsetY)

# Shot
single_shot_img = pygame.image.load('resources/singleshot.png')
double_shot_img = pygame.image.load('resources/doubleshot.png')
triple_shot_img = pygame.image.load('resources/tripleshot.png')
shot_x = 0
shot_y = 0
shot_speed = 30
shot_fired = False

# Define Enemies
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

# Enemy Attributes
enemy_count = 6
enemy_speed = 7.5
enemy_sprite_dim = 64
enemy_dead_img = pygame.image.load('resources/enemydead.png')

# Enemy Shot
enemy_shot_img = pygame.image.load('resources/enemyshot.png')
enemy_shot_x = 0
enemy_shot_y = 0
enemy_shot_speed = 15
enemy_shot_fired = False

for i in range(enemy_count):
    enemy_img.append(pygame.image.load('resources/invader.png'))
    enemy_x.append(random.randint(0, screen_x - 64))
    enemy_y.append(30)
    enemy_x_change.append(enemy_speed)
    enemy_y_change.append(30)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def shot(x, y):
    global shot_fired
    shot_fired = True
    if fire_mode == 1:
        screen.blit(single_shot_img, (x, y))
    if fire_mode == 2:
        screen.blit(double_shot_img, (x, y))
    if fire_mode == 3:
        screen.blit(triple_shot_img, (x, y))


def enemy_shot(x, y):
    global enemy_shot_fired
    enemy_shot_fired = True
    screen.blit(enemy_shot_img, (x, y))


def enemy_dead(x, y, ticks):
    x = 0
    while x < ticks:
        screen.blit(enemy_dead_img, (x, y))
        x + 1


def player_dead(x, y, ticks):
    x = 0
    while x < ticks:
        screen.blit(player_dead_img, (x, y))
        x + 1


def update_score(x, y):
    score = font.render("Score: " + str(player_score), True, (255, 255, 0))
    last_score = font.render("Previous Score: " + str(player_last_score), True, (255, 255, 0))
    name_text = font.render("Name: " + player_name, True, (255, 255, 0))
    screen.blit(score, (x, y))
    screen.blit(last_score, (x, y + 29))
    screen.blit(name_text, (x, y + 58))


def update_health(x, y):
    screen.blit(player_health_img, (x, y))


def respawn_enemy(index):
    enemy_x[index] = random.randint(0, screen_x - 64)
    enemy_y[index] = 30


def respawn_all_enemies():
    for index in range(enemy_count):
        enemy_x[index] = random.randint(0, screen_x - 64)
        enemy_y[index] = 30


def fire_enemy_shot(i):
    if not enemy_shot_fired:
        global enemy_shot_x
        global enemy_shot_y
        enemy_shot_x = math.ceil(enemy_x[i])
        enemy_shot_y = math.ceil(enemy_y[i])
        enemy_shot(math.ceil(enemy_shot_x), math.ceil(enemy_shot_y))


class GameState(IntEnum):
    PREGAME = 1
    HIGHSCORES = 2
    GAME = 3


# Main game loop
running = True
game_state = GameState.PREGAME
while running:
    screen.fill((0, 0, 32))
    screen.blit(background, (0, 0))

    events = pygame.event.get()
    for event in events:
        # Game exit functionality
        if event.type == pygame.QUIT:
            running = False
        # Start Game
        if game_state == GameState.PREGAME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = event.pos
                if 277 < click_x < 520 and 435 < click_y < 510:
                    game_state = GameState.GAME
        # Game Controls
        elif game_state == GameState.GAME:
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    game_state == GameState.PREGAME
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_Change -= player_move_speed
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_Change += player_move_speed
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    playerY_Change -= player_move_speed
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    playerY_Change += player_move_speed
                if event.key == pygame.K_SPACE:
                    if not shot_fired:
                        shot_x = player_x
                        shot_y = player_y
                        shot(player_x, player_y)
                if event.key == pygame.K_1:
                    fire_mode = 1
                if event.key == pygame.K_2:
                    fire_mode = 2
                if event.key == pygame.K_3:
                    fire_mode = 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    playerX_Change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    playerY_Change = 0

    if game_state == GameState.PREGAME:
        screen.blit(banner, (150, 50))
        screen.blit(start_button, (150, 400))
        if player_last_score > 0:
            last_score_text = font.render("Game Over!", True, (255, 255, 0))
            screen.blit(last_score_text, (320, screen_y / 2 - 90))
            last_score_text = font.render("Previous Score: " + str(player_last_score), True, (255, 255, 0))
            screen.blit(last_score_text, (280, screen_y / 2 - 60))

        enter_name_text = font.render("Enter Name: ", True, (255, 255, 0))
        screen.blit(enter_name_text, (330, screen_y / 2 + 25))
        pygame.draw.rect(screen, (255, 255, 255), (300, screen_y / 2 + 55, 200, 30))
        screen.blit(input.get_surface(), (300, screen_y / 2 + 60))
        screen.blit(high_score_button, (700, 500))
        if input.update(events):
            game_state = GameState.GAME
        player_name = input.get_text()


    else:
    elif game_state == GameState.GAME:
        # Player movement
        if not player_x + playerX_Change >= screen_x - player_sprite_dim and not player_x + playerX_Change < 0:
            player_x += playerX_Change
        if not player_y + playerY_Change >= screen_y - player_sprite_dim and not player_y + playerY_Change < 0:
            player_y += playerY_Change

        # Shot Movement
        if shot_fired:
            shot_y -= shot_speed
            shot(shot_x, shot_y)
            if shot_y <= -20:
                shot_fired = False
        else:
            shot_x = player_x
            shot_y = player_y

        # Enemy Shot Fired
        if enemy_shot_fired:
            enemy_shot_y += enemy_shot_speed
            enemy_shot(enemy_shot_x, enemy_shot_y)
            if enemy_shot_y > screen_y:
                enemy_shot_fired = False
                player_score += 10

        # Enemy movement
        for i in range(enemy_count):
            if random.randint(1, 100) > 90:
                fire_enemy_shot(i)

            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = enemy_speed
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= screen_x - enemy_sprite_dim:
                enemy_x_change[i] = enemy_speed * -1
                enemy_y[i] += enemy_y_change[i]

            # Enemy reaches the bottom of the screen, respawn the enemy and deduct 50 points
            if enemy_y[i] >= (screen_y - enemy_sprite_dim):
                enemy_x[i] = random.randint(0, screen_x - 64)
                enemy_y[i] = 30
                player_health -= 1
                player_score -= 50

        for i in range(enemy_count):
            # Collider Checks
            shotCollided = collision.has_collided(enemy_x[i], enemy_y[i], shot_x, shot_y)
            enemyShotCollided = collision.has_collided(player_x, player_y, enemy_shot_x, enemy_shot_y)
            playerCollided = collision.has_collided(enemy_x[i], enemy_y[i], player_x, player_y)
            if shotCollided and shot_fired:
                shot_y = player_y
                shot_fired = False
                player_score += 100
                respawn_enemy(i)

            if playerCollided or enemyShotCollided:
                if enemyShotCollided:
                    enemy_shot_fired = False
                    enemy_shot_y = 30
                player_health -= 1
                player_x = 370
                player_y = 480
                if player_health <= 0:
                    game_state = GameState.PREGAME
                    player_health = 5
                    player_last_score = player_score
                    player_score = 0
                    respawn_all_enemies()
                    highscores.post(player_name, player_last_score)

            enemy(enemy_x[i], enemy_y[i], i)

        for i in range(player_health):
            update_health(health_pos_x[i], health_pos_y[i])

        player(player_x, player_y)
        update_score(score_text_X, score_text_y)

    pygame.display.update()
    clock.tick(30)
