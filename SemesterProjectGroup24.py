#HARD REQUIREMENTS
    #Must use at least 10 different Surface objects.
    #It must access at least 5 different files, for either reading or writing.
    #It must play at least 2 different sounds.
    #    If these sounds come from files on disk, they also towards the requirement above
    #It must either take inputs from the keyboard, mouse, or a controller.
    #It must feature some sort of movement (i.e.: surfaces moving across other surfaces)
    #The user must be able to quit the game without pressing the X button at the top right or stopping the project running the game.
    #There must be a way for the game to “end”.
    #If the game is some sort of puzzle, the puzzle must be solvable, and the game must acknowledge that the puzzle has been solved.
    #If the game has win and lose conditions, those must be implemented.
    #Either of the above must either close the game or allow the user to restart it
#SOFT REQUIREMENTS
    #Game instructions are present in the game and are in correct English
    #Game does not crash or stall
    #Game shows no obvious flaws, such as dropped inputs or rogue Surfaces
import pygame, random, sys, tkinter as tk
from pygame.locals import *

#get the resolution of the active display, then get scaling factors
root = tk.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.destroy()
scaleFactor, widthMulti, heightMulti = (height/1000), (width/1000), (height/850)

TILE_SIZE = 50
JUMP_HEIGHT = int(20*scaleFactor)
Y_GRAVITY = int(1*scaleFactor)
X_SPEED = int(5*scaleFactor)
meteor_min_size = int(20*scaleFactor)
meteor_max_size = int(50*scaleFactor)
meteor_initial_spawn_time = 500
spawn_time = meteor_initial_spawn_time
clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption('Platform Game')
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
menuFont = pygame.font.Font(None, int((height/18)-4))
doubleMenuFont = pygame.font.Font(None, int((height/9)-4))

meteor_timer = pygame.time.get_ticks()
game_start_time = pygame.time.get_ticks()
survival_time = 0
best_time = 0
last_spawn_time_reduction = 0
game_over = False

def drawMenu(actionCount):
    mouse = pygame.mouse.get_pos()
    mouseButtons = pygame.mouse.get_pressed()
    if  actionCount > 0 and not mouseButtons[0]:
        actionCount = 0 #action count will prevent buttons from being pressed repeatedly while the mouse button is held down, since the menu function is called 60 times/second
    menuSurf = pygame.Surface((width, height), pygame.SRCALPHA)
    menuSurf.fill((0, 0, 0, 128))
    menuBaseRect = pygame.Rect(int(width/4), int(height/4), int(width/2), int(height/2)) #each menu item height will be height/24
    pygame.draw.rect(menuSurf, (255, 255, 255, 255), menuBaseRect)
    itemWidth = menuBaseRect.width
    smallItemWidth = int(menuBaseRect.width/20)
    itemHeight = int(menuBaseRect.height / 12)
    doubleItemHeight = int(menuBaseRect.height / 6)
    menuTitleRect =          pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 0), itemWidth, doubleItemHeight)
    mouseSensitivityRect =   pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 2), (smallItemWidth * 18), itemHeight)
    mouseSensitivityUpRect = pygame.Rect(menuBaseRect.left + (smallItemWidth * 18), menuBaseRect.top + (itemHeight * 2), smallItemWidth, itemHeight)
    mouseSensitivityDnRect = pygame.Rect(menuBaseRect.left + (smallItemWidth * 19), menuBaseRect.top + (itemHeight * 2), smallItemWidth, itemHeight)
    fovMultiRect =           pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 3), (smallItemWidth * 18), itemHeight)
    fovMultiUpRect =         pygame.Rect(menuBaseRect.left + (smallItemWidth * 18), menuBaseRect.top + (itemHeight * 3), smallItemWidth, itemHeight)
    fovMultiDnRect =         pygame.Rect(menuBaseRect.left + (smallItemWidth * 19), menuBaseRect.top + (itemHeight * 3), smallItemWidth, itemHeight)
    resMultiRect =           pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 4), (smallItemWidth * 18), itemHeight)
    resMultiUpRect =         pygame.Rect(menuBaseRect.left + (smallItemWidth * 18), menuBaseRect.top + (itemHeight * 4), smallItemWidth, itemHeight)
    resMultiDnRect =         pygame.Rect(menuBaseRect.left + (smallItemWidth * 19), menuBaseRect.top + (itemHeight * 4), smallItemWidth, itemHeight)
    distanceMultiRect =      pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 5), (smallItemWidth * 18), itemHeight)
    distanceMultiUpRect =    pygame.Rect(menuBaseRect.left + (smallItemWidth * 18), menuBaseRect.top + (itemHeight * 5), smallItemWidth, itemHeight)
    distanceMultiDnRect =    pygame.Rect(menuBaseRect.left + (smallItemWidth * 19), menuBaseRect.top + (itemHeight * 5), smallItemWidth, itemHeight)
    devModeRect =            pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 6), itemWidth, itemHeight)
    render3dRect =           pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 7), itemWidth, itemHeight)
    showFPSRect =            pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 8), itemWidth, itemHeight)
    exitRect =               pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 11), itemWidth, itemHeight)
    
    #menu title
    pygame.draw.rect(menuSurf, (100, 100, 100, 255), menuTitleRect)
    menuTitleText = doubleMenuFont.render("Options menu", True, pygame.Color('White'))
    menuSurf.blit(menuTitleText, (menuTitleRect.x + 2, menuTitleRect.y + 2))
    
    #mouse sensitivity
    pygame.draw.rect(menuSurf, (100, 100, 100, 255), mouseSensitivityRect)
    mouseSensitivityText = menuFont.render(f"Mouse sensitivity: {"placeholder text"}", True, pygame.Color('White'))
    menuSurf.blit(mouseSensitivityText, (mouseSensitivityRect.x + 2, mouseSensitivityRect.y + 2))
    #mouse sensitivity up
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if mouseSensitivityUpRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), mouseSensitivityUpRect)
    mouseSensitivityUpText = menuFont.render("+", True, pygame.Color('White'))
    menuSurf.blit(mouseSensitivityUpText, (mouseSensitivityUpRect.x + 2, mouseSensitivityUpRect.y + 2))
    if mouseSensitivityUpRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        mouseSensitivity += 0.01
        actionCount+=1
    #mouse sensitivity down
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if mouseSensitivityDnRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), mouseSensitivityDnRect)
    mouseSensitivityDnText = menuFont.render("-", True, pygame.Color('White'))
    menuSurf.blit(mouseSensitivityDnText, (mouseSensitivityDnRect.x + 2, mouseSensitivityDnRect.y + 2))
    if mouseSensitivityDnRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        mouseSensitivity -= 0.01
        actionCount+=1

    #FOV
    pygame.draw.rect(menuSurf, (100, 100, 100, 255), fovMultiRect)
    fovMultiText = menuFont.render(f"FOV: {"placeholder text"}", True, pygame.Color('White'))
    menuSurf.blit(fovMultiText, (fovMultiRect.x + 2, fovMultiRect.y + 2))
    #fov up
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if fovMultiUpRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), fovMultiUpRect)
    fovMultiUpText = menuFont.render("+", True, pygame.Color('White'))
    menuSurf.blit(fovMultiUpText, (fovMultiUpRect.x + 2, fovMultiUpRect.y + 2))
    if fovMultiUpRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        fovMulti += 0.1
        actionCount+=1
    #fov down
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if fovMultiDnRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), fovMultiDnRect)
    fovMultiDnText = menuFont.render("-", True, pygame.Color('White'))
    menuSurf.blit(fovMultiDnText, (fovMultiDnRect.x + 2, fovMultiDnRect.y + 2))
    if fovMultiDnRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        fovMulti -= 0.1
        actionCount+=1
    
    #resolution
    pygame.draw.rect(menuSurf, (100, 100, 100, 255), resMultiRect)
    resMultiText = menuFont.render(f"Resolution: {"placeholder text"}", True, pygame.Color('White'))
    menuSurf.blit(resMultiText, (resMultiRect.x + 2, resMultiRect.y + 2))
    #resolution up
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if resMultiUpRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), resMultiUpRect)
    resMultiUpText = menuFont.render("+", True, pygame.Color('White'))
    menuSurf.blit(resMultiUpText, (resMultiUpRect.x + 2, resMultiUpRect.y + 2))
    if resMultiUpRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        resMulti += 0.1
        actionCount+=1
    #resolution down
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if resMultiDnRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), resMultiDnRect)
    resMultiDnText = menuFont.render("-", True, pygame.Color('White'))
    menuSurf.blit(resMultiDnText, (resMultiDnRect.x + 2, resMultiDnRect.y + 2))
    if resMultiDnRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        resMulti -= 0.1
        actionCount+=1

    #distance
    pygame.draw.rect(menuSurf, (100, 100, 100, 255), distanceMultiRect)
    distanceMultiText = menuFont.render(f"Rendering distance: {"placeholder text"}", True, pygame.Color('White'))
    menuSurf.blit(distanceMultiText, (distanceMultiRect.x + 2, distanceMultiRect.y + 2))
    #distance up
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if distanceMultiUpRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), distanceMultiUpRect)
    distanceMultiUpText = menuFont.render("+", True, pygame.Color('White'))
    menuSurf.blit(distanceMultiUpText, (distanceMultiUpRect.x + 2, distanceMultiUpRect.y + 2))
    if distanceMultiUpRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        distanceMulti += 0.1
        actionCount+=1
    #distance down
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if distanceMultiDnRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), distanceMultiDnRect)
    distanceMultiDnText = menuFont.render("-", True, pygame.Color('White'))
    menuSurf.blit(distanceMultiDnText, (distanceMultiDnRect.x + 2, distanceMultiDnRect.y + 2))
    if distanceMultiDnRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        distanceMulti -= 0.1
        actionCount+=1

    #dev mode
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if devModeRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), devModeRect)
    devModeText = menuFont.render(f"Dev mode: {"placeholder text"}", True, pygame.Color('White'))
    menuSurf.blit(devModeText, (devModeRect.x + 2, devModeRect.y + 2))
    if devModeRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
            devMode = True if devMode == False else False
            actionCount+=1
    
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if exitRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), exitRect)
    exitText = menuFont.render("Save and exit", True, pygame.Color('White'))
    menuSurf.blit(exitText, (exitRect.x + 2, exitRect.y + 2))
    if exitRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        actionCount+=1
    
    screen.blit(menuSurf, (0,0))
    return actionCount

class SpacePebble:
    def __init__(self):
        self.size = random.randint(meteor_min_size, meteor_max_size)
        self.rect = self.spawn_meteor()
        self.dx, self.dy = self.set_speed()

    def spawn_meteor(self):
        side = random.choice(['left', 'right'])
        if side == 'left':
            return pygame.Rect(-self.size, (random.randint(0, height - self.size)), self.size, self.size)
        else:
            return pygame.Rect(width, random.randint(0, height - self.size), self.size, self.size)

    def set_speed(self):
        speed_factor = random.randint(2, 5)
        if self.rect.top <= 0:
            return random.uniform(-2, 2), speed_factor
        elif self.rect.bottom >= (1000*scaleFactor):
            return random.uniform(-2, 2), -speed_factor
        elif self.rect.left <= 0:
            return speed_factor, random.uniform(-2, 2)
        else:
            return -speed_factor, random.uniform(-2, 2)

    def move(self):
        if not menu:
            self.rect.x += self.dx
            self.rect.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumping = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, keys, world):
        if not menu:
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

        if world.goal_tile and world.goal_tile.colliderect(self.rect):
            print("You win") # Maybe have a "you win" screen
            pygame.quit()
            sys.exit()

class World:
    def __init__(self, data):
        self.tile_list = []
        self.goal_tile = None  # Makes goal tile different
        dirt_img = pygame.image.load('dirt.jpg')
        goal_img = pygame.image.load('goal.png')
        self.goal_img = pygame.transform.scale(goal_img, (TILE_SIZE*widthMulti, TILE_SIZE*heightMulti))  # Scale goal image to tile size

        for row_index, row in enumerate(data):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE*widthMulti, TILE_SIZE*heightMulti))
                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE*widthMulti
                    img_rect.y = row_index * TILE_SIZE*heightMulti
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    goal_rect = self.goal_img.get_rect()
                    goal_rect.x = col_index * TILE_SIZE*widthMulti
                    goal_rect.y = row_index * TILE_SIZE*heightMulti
                    self.goal_tile = goal_rect

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        if self.goal_tile:
            screen.blit(self.goal_img, self.goal_tile)


world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # grid of map that can be edited
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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)
player = Player(500, 8 * (TILE_SIZE*scaleFactor) - 50)
meteors = []
actionCount = 0 #used to stop menu buttons from being spammed while mouse button is held down

#main loop
running = True
menu = False
pygame.mouse.set_visible(False)
while running:
    screen.fill((0, 0, 0))

    world.draw()

    keys = pygame.key.get_pressed()
    player.move(keys, world)
    player.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu = not menu
                pygame.mouse.set_visible(menu)

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


    if game_over:
        print("Game Over!") # Maybe a "game over" screen
        break

    if menu:
        drawMenu(actionCount)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()