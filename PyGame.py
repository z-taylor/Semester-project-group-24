import pygame
import sys
from pygame.locals import *

pygame.init()

# Game window setup
pygame.display.set_caption('Platform Game')
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

# Constants
TILE_SIZE = 100
JUMP_HEIGHT = 25
Y_GRAVITY = 1
X_SPEED = 5

jumping = False


class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))  # Player size
        self.image.fill((255, 0, 0))  # Red color
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

        if keys[pygame.K_a]:  # Move left
            dx = -X_SPEED
        if keys[pygame.K_d]:  # Move right
            dx = X_SPEED
        if keys[pygame.K_SPACE] and not self.jumping:  # Jump
            self.vel_y = -JUMP_HEIGHT
            self.jumping = True

        # Gravity
        self.vel_y += Y_GRAVITY
        dy += self.vel_y

        # Check for collision
        for tile in world.tile_list:
            # Check for collision horizontal
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0

            # Check for collision verticle
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                # falling
                if self.vel_y > 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jumping = False  # Allow jumping again after landing
                # jumping
                elif self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0

        # player position update
        self.rect.x += dx
        self.rect.y += dy


#tiles class
class World:
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('360_F_417154464_XWjVtPxASXXlFIPUvQtoMOeJ8ky38Q6W.jpg')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


# World data
world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],  # Bottom row of tiles
]

# Initialize player and world
world = World(world_data)

#Starting position
player = Player(500, 8 * TILE_SIZE - 50)

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))

    world.draw()

    keys = pygame.key.get_pressed()

    player.move(keys, world)

    player.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

    clock.tick(60)

pygame.quit()
