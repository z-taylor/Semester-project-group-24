import pygame
import sys
import random
from pygame.locals import *

TILE_SIZE = 50
JUMP_HEIGHT = 20
Y_GRAVITY = 1
X_SPEED = 5
meteor_min_size = 20
meteor_max_size = 50
meteor_initial_spawn_time = 500
spawn_time = meteor_initial_spawn_time
clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption('Platform Game')
screen = pygame.display.set_mode((1000, 1000))

meteor_timer = pygame.time.get_ticks()
game_start_time = pygame.time.get_ticks()
survival_time = 0
best_time = 0
last_spawn_time_reduction = 0
game_over = False

class SpacePebble:
    def __init__(self):
        self.size = random.randint(meteor_min_size, meteor_max_size)
        self.rect = self.spawn_meteor()
        self.dx, self.dy = self.set_speed()

    def spawn_meteor(self):
        side = random.choice(['left', 'right'])
        if side == 'left':
            return pygame.Rect(-self.size, random.randint(0, 1000 - self.size), self.size, self.size)
        else:
            return pygame.Rect(1000, random.randint(0, 1000 - self.size), self.size, self.size)

    def set_speed(self):
        speed_factor = random.randint(2, 5)
        if self.rect.top <= 0:
            return random.uniform(-2, 2), speed_factor
        elif self.rect.bottom >= 1000:
            return random.uniform(-2, 2), -speed_factor
        elif self.rect.left <= 0:
            return speed_factor, random.uniform(-2, 2)
        else:
            return -speed_factor, random.uniform(-2, 2)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumping = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, keys, world):
        dx = 0
        dy = 0

        if keys[pygame.K_a]:
            dx = -X_SPEED
        if keys[pygame.K_d]:
            dx = X_SPEED
        if keys[pygame.K_SPACE] and not self.jumping:
            self.vel_y = -JUMP_HEIGHT
            self.jumping = True


        self.vel_y += Y_GRAVITY
        dy += self.vel_y


        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y > 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jumping = False
                elif self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

class World:
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('360_F_417154464_XWjVtPxASXXlFIPUvQtoMOeJ8ky38Q6W.jpg')
        goal_img = pygame.image.load('goal.png')

        for row_index, row in enumerate(data):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE
                    img_rect.y = row_index * TILE_SIZE
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(goal_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE
                    img_rect.y = row_index * TILE_SIZE
                    self.tile_list.append((img, img_rect))

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

world = World(world_data)
player = Player(500, 8 * TILE_SIZE - 50)
meteors = []

#main
running = True
while running:
    screen.fill((0, 0, 0))

    world.draw()

    keys = pygame.key.get_pressed()
    player.move(keys, world)
    player.draw(screen)

    if pygame.time.get_ticks() - meteor_timer > spawn_time:
        meteors.append(SpacePebble())
        meteor_timer = pygame.time.get_ticks()

    for meteor in meteors[:]:
        meteor.move()
        meteor.draw()

        if meteor.rect.colliderect(player.rect):
            game_over = True
            best_time = max(survival_time, best_time)

    elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000
    if elapsed_time > 0 and elapsed_time % 10 == 0 and last_spawn_time_reduction != elapsed_time:
        if spawn_time > 1000:
            spawn_time -= 500
        last_spawn_time_reduction = elapsed_time

    if game_over:
        print("Game Over! Best Time: ", best_time)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
