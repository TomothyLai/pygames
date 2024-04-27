import pygame
import os
import random
from bullet_class import Bullet
from bullet_class import Enemy
pygame.init()
WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("first game")
FLOOR_POSITION = 400
MAX_BULLETS = 10
ENEMY_HIT = pygame.USEREVENT + 1
ENEMY_DEAD = pygame.USEREVENT + 2
#Colours
WHITE = (255, 255, 255)
FLOOR_COLOUR = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
RED = (255, 0, 0)
#Frames per second
FPS = 60
VELOCITY = 5
JUMP_VELOCITY = 15
GRAVITY = 10
CHARACTER_WIDTH, CHARACTER_HEIGHT = 100, 200

#getting images
MAIN_CHARACTER_IMAGE = pygame.image.load(os.path.join("assets", "character.png"))
MAIN_CHARACTER = pygame.transform.scale(MAIN_CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
ENEMY_IMAGE = pygame.image.load(os.path.join("assets", "enemy.png"))
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
font = pygame.font.SysFont(None, 24)
WIN_NOTIFICATION = font.render("ENEMY HAS DIED!!!", True, RED)
#JUMP_SOUND = pygame.mixer.Sound(os.path.join("assets", "jump_sound.mp3"))

def draw_window(player, enemy, player_bullets):
    WINDOW.fill(WHITE)
    WINDOW.blit(MAIN_CHARACTER, (player.x, player.y))
    WINDOW.blit(ENEMY, (enemy.x, enemy.y))
    pygame.draw.rect(WINDOW, FLOOR_COLOUR, (0, FLOOR_POSITION + CHARACTER_HEIGHT, WIDTH, HEIGHT - FLOOR_POSITION))
    for bullet in player_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    if check_for_win(enemy):
        WINDOW.blit(WIN_NOTIFICATION, (50, 50))
    pygame.display.update()

def player_movement(keys_pressed, player, cooldown, time_after_air):
    if keys_pressed[pygame.K_d] and player.x < WIDTH:
        player.x += VELOCITY
    if keys_pressed[pygame.K_a] and player.x > 0:
        player.x -= VELOCITY
    if keys_pressed[pygame.K_w] and not cooldown:
        return True
    if player.y < FLOOR_POSITION:
        player.y += GRAVITY * time_after_air
    return False
def enemy_movement(keys_pressed, enemy, cooldown, time_after_air):
    if keys_pressed[pygame.K_LEFT] and enemy.x > 0:
        enemy.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and enemy.x < WIDTH:
        enemy.x += VELOCITY
    if keys_pressed[pygame.K_UP] and not cooldown:
        return True
    if enemy.y < FLOOR_POSITION:
        enemy.y += GRAVITY * time_after_air
    return False

def handle_bullet_collisions(player_bullets, enemy):
    for bullet in player_bullets:
        if enemy.colliderect(bullet):
            player_bullets.remove(bullet)
            enemy.got_hit()
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
        elif bullet.x < 0 or bullet.x > WIDTH:
            player_bullets.remove(bullet)
        if bullet.direction == "LEFT":
            bullet.x -= bullet.VELOCITY
        else:
            bullet.x += bullet.VELOCITY
    return False

def check_for_win(enemy):
    if enemy.get_health() <= 0:
        return True
def main():
    clock = pygame.time.Clock()
    run = True
    player = pygame.Rect(100, FLOOR_POSITION, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    enemy = Enemy(WIDTH - 100, FLOOR_POSITION, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    player_jump_cooldown = False
    enemy_jump_cooldown = False
    count_player_time_in_air = False
    count_enemy_time_in_air = False
    count_player_time_after_air = False
    count_enemy_time_after_air = False
    player_time_in_air = 0
    enemy_time_in_air = 0
    player_time_after_air = 0
    enemy_time_after_air = 0
    player_bullets = []
    last_player_direction = "RIGHT"
    while run:
        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()
        jumped_player = player_movement(keys_pressed, player, player_jump_cooldown, player_time_after_air)
        jumped_enemy = enemy_movement(keys_pressed, enemy, enemy_jump_cooldown, enemy_time_after_air)
        if jumped_player:
            player_jump_cooldown = True
            count_player_time_in_air = True
        if jumped_enemy:
            enemy_jump_cooldown = True
            count_enemy_time_in_air = True
        if count_player_time_in_air:
            player_time_in_air += 3/FPS
            player.y -= JUMP_VELOCITY - GRAVITY * player_time_in_air
            if player_time_in_air > JUMP_VELOCITY/GRAVITY:
                count_player_time_in_air = False
                player_time_in_air = 0
                count_player_time_after_air = True
        if count_enemy_time_in_air:
            enemy_time_in_air += 3/FPS
            enemy.y -= JUMP_VELOCITY - GRAVITY * enemy_time_in_air
            if enemy_time_in_air > JUMP_VELOCITY/GRAVITY:
                count_enemy_time_in_air = False
                enemy_time_in_air = 0
                count_enemy_time_after_air = True
        if count_enemy_time_after_air:
            enemy_time_after_air += 3/FPS
            if enemy_time_after_air > 2:
                enemy_jump_cooldown = False
                count_enemy_time_after_air = False
                enemy_time_after_air = 0
        if count_player_time_after_air:
            player_time_after_air += 3/FPS
            if player_time_after_air > 2:
                player_jump_cooldown = False
                count_player_time_after_air = False
                player_time_after_air =  0
        handle_bullet_collisions(player_bullets, enemy)
        draw_window(player, enemy, player_bullets)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_bullets) < MAX_BULLETS:
                        player_bullet = Bullet(player.x + player.width//2, player.y + player.height//2 - 2, 10, 5, last_player_direction)
                        player_bullets.append(player_bullet)

                if event.key == pygame.K_d:
                    last_player_direction = "RIGHT"
                if event.key == pygame.K_a:
                    last_player_direction = "LEFT"
            if event.type == pygame.event.Event(ENEMY_HIT):
                print("Hit")


    pygame.quit()
if __name__ == "__main__":
    main()