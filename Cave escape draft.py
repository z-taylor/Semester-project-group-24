import pygame, random, sys, tkinter as tk
from pygame.locals import *

# get the resolution of the active display, then get scaling factors
root = tk.Tk()
width, height, hrznRes, vertRes = root.winfo_screenwidth(), root.winfo_screenheight(), root.winfo_screenwidth(), root.winfo_screenheight()
root.destroy()
widthMulti, heightMulti = (width / 1000), (height / 850)

pygame.mixer.init()
coin_sound = pygame.mixer.Sound('coin1.mp3')
jump_sound = pygame.mixer.Sound('jump.mp3')

TILE_SIZE = 50
JUMP_HEIGHT = int(20 * heightMulti)
Y_GRAVITY = 1
X_SPEED = int(5 * widthMulti)
meteor_min_size = int(20 * heightMulti)
meteor_max_size = int(50 * heightMulti)
meteor_initial_spawn_time = 500
spawn_time = meteor_initial_spawn_time
clock = pygame.time.Clock()

background = pygame.image.load('background.png')
scaled_background = pygame.transform.scale(background,(width, height))


def draw(self, screen):
    screen.blit(self.image, self.rect)


score = 0

pygame.init()

pygame.display.set_caption('Platform Game')
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
menuFont = pygame.font.Font(None, int((height / 18) - 4))
doubleMenuFont = pygame.font.Font(None, int((height / 9) - 4))
gameOverFont = pygame.font.Font(None, int((height / 6) - 4))

meteor_timer = pygame.time.get_ticks()
game_start_time = pygame.time.get_ticks()
survival_time = 0
best_time = 0
last_spawn_time_reduction = 0
game_over = False


def drawGameOver(reset, quit):
    gameOverSurf = pygame.Surface((width, height))
    gameOverBackground = pygame.image.load("background.png")
    gameOverBackground = pygame.transform.scale(gameOverBackground, (width, height))
    gameOverSurf.blit(gameOverBackground, (0, 0))
    smallHeight = height / 6
    mouse = pygame.mouse.get_pos()

    gameOverTitleText = gameOverFont.render("Game over!", True, pygame.Color('White'))
    gameOverScoreText = gameOverFont.render(f"You collected {score}/5 coins", True, pygame.Color('White'))
    gameOverResetText = gameOverFont.render("Try again?", True, pygame.Color('White'))
    gameOverQuitText = gameOverFont.render("Quit?", True, pygame.Color('White'))

    gameOverTitleSurf = pygame.Surface((gameOverTitleText.get_width(), smallHeight), pygame.SRCALPHA)
    gameOverScoreSurf = pygame.Surface((gameOverScoreText.get_width(), smallHeight), pygame.SRCALPHA)
    gameOverResetSurf = pygame.Surface((gameOverResetText.get_width(), smallHeight), pygame.SRCALPHA)
    gameOverQuitSurf = pygame.Surface((gameOverQuitText.get_width(), smallHeight), pygame.SRCALPHA)
    
    collisionRect1 = pygame.Rect((width / 2 - gameOverResetText.get_width() / 2), smallHeight * 3,gameOverResetText.get_width(), smallHeight)
    collisionRect2 = pygame.Rect((width / 2 - gameOverQuitText.get_width() / 2), smallHeight * 4,gameOverQuitText.get_width(), smallHeight)

    gameOverTitleSurf.fill((0, 0, 0, 0))
    gameOverScoreSurf.fill((0, 0, 0, 0))
    gameOverResetSurf.fill((0, 0, 0, 128) if collisionRect1.collidepoint(mouse) else (0, 0, 0, 0))
    gameOverQuitSurf.fill((0, 0, 0, 128) if collisionRect2.collidepoint(mouse) else (0, 0, 0, 0))

    gameOverTitleSurf.blit(gameOverTitleText, (0, 0))
    gameOverScoreSurf.blit(gameOverScoreText, (0, 0))
    gameOverResetSurf.blit(gameOverResetText, (0, 0))
    gameOverQuitSurf.blit(gameOverQuitText, (0, 0))

    gameOverSurf.blit(gameOverTitleSurf, ((width / 2 - gameOverTitleText.get_width() / 2), smallHeight * 1))
    gameOverSurf.blit(gameOverScoreSurf, ((width / 2 - gameOverScoreText.get_width() / 2), smallHeight * 2))
    gameOverSurf.blit(gameOverResetSurf, ((width / 2 - gameOverResetText.get_width() / 2), smallHeight * 3))
    gameOverSurf.blit(gameOverQuitSurf, ((width / 2 - gameOverQuitText.get_width() / 2), smallHeight * 4))

    screen.blit(gameOverSurf, (0, 0))

    mouseButtons = pygame.mouse.get_pressed()
    if collisionRect1.collidepoint(mouse) and mouseButtons[0]:
        reset = True
    elif collisionRect2.collidepoint(mouse) and mouseButtons[0]:
        quit = True

    return reset, quit


def drawMenu(actionCount, help, menuTicker, hrznRes, vertRes, resAdjust):
    mouse = pygame.mouse.get_pos()
    mouseButtons = pygame.mouse.get_pressed()
    if not mouseButtons[0]:
        actionCount = 0  # action count will prevent buttons from being pressed repeatedly while the mouse button is held down, since the menu function is called 60 times/second
        menuTicker = 0
    if mouseButtons[0]:
        menuTicker += 1
    menuSurf = pygame.Surface((width, height), pygame.SRCALPHA)
    menuSurf.fill((0, 0, 0, 128))
    menuBaseRect = pygame.Rect(int(width / 4), int(height / 4), int(width / 2),int(height / 2))  # each menu item height will be height/24
    pygame.draw.rect(menuSurf, (255, 255, 255, 255), menuBaseRect)

    itemWidth = menuBaseRect.width
    smallItemWidth = int(menuBaseRect.width / 20)
    itemHeight = int(menuBaseRect.height / 10)
    doubleItemHeight = int(menuBaseRect.height / 5)

    menuTitleRect = pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 0), itemWidth, doubleItemHeight)
    resolutionRect = pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 2), itemWidth, itemHeight)
    hrznResRect = pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 3), (smallItemWidth * 18), itemHeight)
    hrznResUpRect = pygame.Rect(menuBaseRect.left + (smallItemWidth * 18), menuBaseRect.top + (itemHeight * 3),smallItemWidth, itemHeight)
    hrznResDnRect = pygame.Rect(menuBaseRect.left + (smallItemWidth * 19), menuBaseRect.top + (itemHeight * 3),smallItemWidth, itemHeight)
    vertResRect = pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 4), (smallItemWidth * 18), itemHeight)
    vertResUpRect = pygame.Rect(menuBaseRect.left + (smallItemWidth * 18), menuBaseRect.top + (itemHeight * 4),smallItemWidth, itemHeight)
    vertResDnRect = pygame.Rect(menuBaseRect.left + (smallItemWidth * 19), menuBaseRect.top + (itemHeight * 4),smallItemWidth, itemHeight)
    resAdjustRect = pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 5), itemWidth, itemHeight)
    helpRect = pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 6), itemWidth, itemHeight)
    exitRect = pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 9), itemWidth, itemHeight)
    #helpTitleRect = pygame.Rect(menuBaseRect.left, menuBaseRect.top + (itemHeight * 0), (smallItemWidth * 19),doubleItemHeight)
    #helpTitleRect_ = pygame.Rect((menuBaseRect.right - smallItemWidth), menuBaseRect.top + (itemHeight * 1),(smallItemWidth * 1), itemHeight)
    #helpTitleXrect = pygame.Rect((menuBaseRect.right - smallItemWidth), menuBaseRect.top + (itemHeight * 0),(smallItemWidth * 1), itemHeight)

    if not help:
        # menu title
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), menuTitleRect)
        menuTitleText = doubleMenuFont.render("Options menu", True, pygame.Color('White'))
        menuSurf.blit(menuTitleText, (menuTitleRect.x + 2, menuTitleRect.y + 2))

        # Screen resolution
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), resolutionRect)
        resolutionText = menuFont.render(f"Screen resolution: {width}x{height}", True, pygame.Color('White'))
        menuSurf.blit(resolutionText, (resolutionRect.x + 2, resolutionRect.y + 2))

        # Horizontal resolution
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), hrznResRect)
        hrznResText = menuFont.render(f"Horizontal resolution: {hrznRes}", True, pygame.Color('White'))
        menuSurf.blit(hrznResText, (hrznResRect.x + 2, hrznResRect.y + 2))
        # Horizontal resolution up
        pygame.draw.rect(menuSurf, (
            (150, 150, 150, 255) if hrznResUpRect.collidepoint(mouse) and not mouseButtons[0] else (
                100, 100, 100, 255)), hrznResUpRect)
        hrznResUpText = menuFont.render("+", True, pygame.Color('White'))
        menuSurf.blit(hrznResUpText, (hrznResUpRect.x + 2, hrznResUpRect.y + 2))
        if hrznResUpRect.collidepoint(mouse) and mouseButtons[0] and (actionCount < 1 or menuTicker > 60):
            hrznRes += 1
            actionCount += 1
        # Horizontal resolution down
        pygame.draw.rect(menuSurf, (
            (150, 150, 150, 255) if hrznResDnRect.collidepoint(mouse) and not mouseButtons[0] else (
                100, 100, 100, 255)), hrznResDnRect)
        hrznResDnText = menuFont.render("-", True, pygame.Color('White'))
        menuSurf.blit(hrznResDnText, (hrznResDnRect.x + 2, hrznResDnRect.y + 2))
        if hrznResDnRect.collidepoint(mouse) and mouseButtons[0] and (actionCount < 1 or menuTicker > 60):
            hrznRes -= 1
            actionCount += 1

        # Vertical resolution
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), vertResRect)
        vertResText = menuFont.render(f"Vertical resolution: {vertRes}", True, pygame.Color('White'))
        menuSurf.blit(vertResText, (vertResRect.x + 2, vertResRect.y + 2))
        # Vertical resolution up
        pygame.draw.rect(menuSurf, (
            (150, 150, 150, 255) if vertResUpRect.collidepoint(mouse) and not mouseButtons[0] else (
                100, 100, 100, 255)), vertResUpRect)
        vertResUpText = menuFont.render("+", True, pygame.Color('White'))
        menuSurf.blit(vertResUpText, (vertResUpRect.x + 2, vertResUpRect.y + 2))
        if vertResUpRect.collidepoint(mouse) and mouseButtons[0] and (actionCount < 1 or menuTicker > 60):
            vertRes += 1
            actionCount += 1
        # Vertical resolution down
        pygame.draw.rect(menuSurf, (
            (150, 150, 150, 255) if vertResDnRect.collidepoint(mouse) and not mouseButtons[0] else (
                100, 100, 100, 255)), vertResDnRect)
        vertResDnText = menuFont.render("-", True, pygame.Color('White'))
        menuSurf.blit(vertResDnText, (vertResDnRect.x + 2, vertResDnRect.y + 2))
        if vertResDnRect.collidepoint(mouse) and mouseButtons[0] and (actionCount < 1 or menuTicker > 60):
            vertRes -= 1
            actionCount += 1

        # Adjust resolution
        pygame.draw.rect(menuSurf, (
            (150, 150, 150, 255) if resAdjustRect.collidepoint(mouse) and not mouseButtons[0] else (
                100, 100, 100, 255)), resAdjustRect)
        resAdjustText = menuFont.render("Adjust scaling", True, pygame.Color('White'))
        menuSurf.blit(resAdjustText, (resAdjustRect.x + 2, resAdjustRect.y + 2))
        if resAdjustRect.collidepoint(mouse) and mouseButtons[0] and (actionCount < 1 or menuTicker > 60):
            resAdjust = True
            actionCount += 1

        # Help
        #pygame.draw.rect(menuSurf, (
        #    (150, 150, 150, 255) if helpRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)),
        #                 helpRect)
        #helpText = menuFont.render(f"Help", True, pygame.Color('White'))
        #menuSurf.blit(helpText, (helpRect.x + 2, helpRect.y + 2))
        #if helpRect.collidepoint(mouse) and mouseButtons[0] and (actionCount < 1 or menuTicker > 60):
        #    help = True
        #    actionCount += 1

        # Exit
        pygame.draw.rect(menuSurf, (
            (150, 150, 150, 255) if exitRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)),
                         exitRect)
        exitText = menuFont.render("Quit game", True, pygame.Color('White'))
        menuSurf.blit(exitText, (exitRect.x + 2, exitRect.y + 2))
        if exitRect.collidepoint(mouse) and mouseButtons[0] and (actionCount < 1 or menuTicker > 60):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            actionCount += 1
    #else:
    #    # help menu title
    #    pygame.draw.rect(menuSurf, (100, 100, 100, 255), helpTitleRect)
    #    pygame.draw.rect(menuSurf, (100, 100, 100, 255), helpTitleRect_)
    #    helpTitleText = doubleMenuFont.render("Help menu", True, pygame.Color('White'))
    #    menuSurf.blit(helpTitleText, (helpTitleRect.x + 2, helpTitleRect.y + 2))
    #    pygame.draw.rect(menuSurf, (
    #        (150, 150, 150, 255) if helpTitleXrect.collidepoint(mouse) and not mouseButtons[0] else (
    #            100, 100, 100, 255)), helpTitleXrect)
    #    helpTitleXtext = menuFont.render("X", True, pygame.Color('White'))
    #    text_width, text_height = helpTitleXtext.get_size()
    #    menuSurf.blit(helpTitleXtext, ((helpTitleXrect.left + (helpTitleXrect.width - text_width) / 2), (helpTitleXrect.top + (helpTitleXrect.height - text_height) / 2)))
    #    if helpTitleXrect.collidepoint(mouse) and mouseButtons[0] and (actionCount < 1 or menuTicker > 60):
    #        help = False
    #        actionCount += 1
    screen.blit(menuSurf, (0, 0))
    return actionCount, help, menuTicker, hrznRes, vertRes, resAdjust


class Coin:
    def __init__(self, x, y):
        self.image = pygame.image.load('coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


coins = [Coin(100 * widthMulti, 500 * heightMulti), Coin(300 * widthMulti, 400 * heightMulti),
         Coin(500 * widthMulti, 300 * heightMulti), Coin(800 * widthMulti, 700 * heightMulti), Coin(540 * widthMulti, 140*heightMulti)]


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
        elif self.rect.bottom >= (1000 * heightMulti):
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
        self.image = pygame.image.load('Human.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x * widthMulti
        self.rect.y = y * heightMulti
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
                jump_sound.play()

            self.vel_y += Y_GRAVITY
            dy += self.vel_y

            for tile in world.tile_list:
                if (tile[1].colliderect(self.rect)) and (
                        ((self.rect.bottom >= tile[1].top) and (self.rect.bottom - tile[1].top >= 1)) or (
                        (self.rect.top <= tile[1].bottom) and (tile[1].bottom - self.rect.top >= 1))):
                    self.rect.move_ip(0, -1)
                elif (tile[1].colliderect(self.rect)) and (
                        ((self.rect.right >= tile[1].left) and (self.rect.right - tile[1].left >= 1)) or (
                        (self.rect.left <= tile[1].right) and (tile[1].right - self.rect.left >= 1))):
                    self.rect.move_ip(0, -1)
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
            new_rect = self.rect.move(dx, dy)
            if 0 <= new_rect.x <= width - self.rect.width and 0 <= new_rect.y <= height - self.rect.height:
                self.rect.x += dx
            self.rect.y += dy
            # print(self.rect.x, self.rect.y)

        if world.goal_tile and world.goal_tile.colliderect(self.rect) and score==5:
            print("You win")  # Maybe have a "you win" screen
            pygame.quit()
            sys.exit()


class World:
    def __init__(self, data):
        self.tile_list = []
        self.goal_tile = None  # Makes goal tile different
        dirt_img = pygame.image.load('dirt.jpg')
        goal_img = pygame.image.load('goal.png')
        self.goal_img = pygame.transform.scale(goal_img, (
            TILE_SIZE * widthMulti, TILE_SIZE * heightMulti))  # Scale goal image to tile size

        for row_index, row in enumerate(data):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE * widthMulti, TILE_SIZE * heightMulti))
                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE * widthMulti
                    img_rect.y = row_index * TILE_SIZE * heightMulti
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    goal_rect = self.goal_img.get_rect()
                    goal_rect.x = col_index * TILE_SIZE * widthMulti
                    goal_rect.y = row_index * TILE_SIZE * heightMulti
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
player = Player(3.125, 770.3125)
meteors = []
actionCount = 0  # used to stop menu buttons from being spammed while mouse button is initially pressed
menuTicker = 0  # used to let buttons be held down to repeat the action while stopping main variables from being updated
help = False

# main loop
running = True
menu = False
resAdjust = False
escPress = 0
ticker = 0
reset = False
quit = False
pygame.mouse.set_visible(False)
while running:
    screen.fill((0, 0, 0))
    screen.blit(scaled_background, (0, 0))


    if not game_over:
        world.draw()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        escPress += 1
    elif not keys[pygame.K_ESCAPE] and escPress > 0:
        escPress = 0
        menu = not menu
        pygame.mouse.set_visible(menu)

    if not menu:
        player.move(keys, world)
        if not game_over:
            player.draw(screen)

    if (pygame.time.get_ticks() - meteor_timer > spawn_time) and not (menu or game_over):
        if score > 1 or ticker > 300:
            meteors.append(SpacePebble())
        meteor_timer = pygame.time.get_ticks()

    if not game_over:
        for meteor in meteors[:]:
            meteor.move()
            meteor.draw()

            if meteor.rect.colliderect(player.rect):
                game_over = True
                best_time = max(survival_time, best_time)

    elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000

    for coin in coins[:]:  # COINCOIN
        coin.draw(screen)
        if player.rect.colliderect(coin.rect):
            coins.remove(coin)
            score += 1
            print(f"Score: {score}")
            coin_sound.play()

    if menu:
        actionCount, help, menuTicker, hrznRes, vertRes, resAdjust = drawMenu(actionCount, help, menuTicker, hrznRes,
                                                                              vertRes, resAdjust)

    if (width != hrznRes or height != vertRes) and resAdjust == True:
        width, height = hrznRes, vertRes
        widthMulti, heightMulti = (width / 1000), (height / 850)
        JUMP_HEIGHT, Y_GRAVITY, X_SPEED, meteor_min_size, meteor_max_size = int(20 * heightMulti), int(
            1 * heightMulti), int(5 * widthMulti), int(20 * heightMulti), int(50 * heightMulti)
        world = World(world_data)
        resAdjust = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    score_text = menuFont.render(f"Coins: {score}/5", True, pygame.Color('White'))  ##COINCOIN
    screen.blit(score_text, (10, 10))
    objective_text = menuFont.render(f"Collect all 5 coins and reach the flag.", True, pygame.Color('White'))
    screen.blit(objective_text, ((width/2) - (objective_text.get_width()/2), 10))

    ticker += 1
    clock.tick(60)
    if game_over:
        coins.clear()
        meteors.clear()
        reset, quit = drawGameOver(reset, quit)
        pygame.mouse.set_visible(game_over)
    pygame.display.flip()
    if quit:
        break
    if reset:
        game_over = not game_over
        reset = not reset
        pygame.mouse.set_visible(game_over)
        score = 0
        player = Player(3.125, 770.3125)
        coins = [Coin(100 * widthMulti, 500 * heightMulti), Coin(300 * widthMulti, 400 * heightMulti),
                 Coin(500 * widthMulti, 300 * heightMulti), Coin(800 * widthMulti, 700 * heightMulti),
                 Coin(540 * widthMulti, 140 * heightMulti)]

pygame.quit()
