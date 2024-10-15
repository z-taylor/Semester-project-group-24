import pygame, sys, math, tkinter as tk, time
from pygame.locals import *

#get the resolution of the active display
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

#initiate pygame & window
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
menuFont = pygame.font.Font(None, int((height/18)-4))
doubleMenuFont = pygame.font.Font(None, int((height/9)-4))
fps = pygame.font.Font(None, 72)
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption('Raycasting test')

#map
map = ('########'
       '# #    #'
       '# #  ###'
       '#      #'
       '##     #'
       '#  ### #'
       '#   #  #'
       '########')

#user settings
mouseSensitivity = 0.1
fovMulti = 1
resMulti = 1
distanceMulti = 1
devMode = False
render3d = True
showFPS = False

#set constants
resMultiplier = (2560*1440) / (width*height)
mapSize = int(math.sqrt(len(map)))
tileWidth = int(width / mapSize)
tileHeight = int(height / mapSize)
fov = (math.pi / 3) * fovMulti
halfFov = fov / 2
castedRays = int(100 * resMulti)
maxDepth = int(math.sqrt( ((width)**2)*distanceMulti + ((height)**2)*distanceMulti ))
stepAngle = fov/castedRays
moveSpeed = 10

#set global variables
playerX = (width / 2) / 2
playerY = (width / 2) / 2
playerAngle = math.pi
actionCount = 0
rects = []

def drawMap(rects):
    rects.clear()
    screen.fill((0,0,0))
    white, black = (255, 255, 255), (0, 0, 0)
    for row in range(mapSize):
        for square in range(mapSize):
            Square = row * mapSize + square
            color = white if map[Square] == '#' else black
            rect = (square * tileWidth, row * tileHeight, tileWidth, tileHeight)
            pygame.draw.rect(screen, color, rect)
            if color==white:
                rects.append(pygame.Rect(rect))
    #draw player        
    pygame.draw.circle(screen, (0, 255, 0), (int(playerX), int(playerY)), 12)
    #show fov, direction, & rendering distance
    pygame.draw.line(screen, (0, 0, 255), (playerX, playerY), ((playerX - math.sin(playerAngle - halfFov)*250), (playerY+math.cos(playerAngle - halfFov)*250)), 3)
    pygame.draw.line(screen, (0, 0, 255), (playerX, playerY), ((playerX - math.sin(playerAngle + halfFov)*250), (playerY+math.cos(playerAngle + halfFov)*250)), 3)
    pygame.draw.line(screen, (0, 0, 255), (playerX, playerY), ((playerX - math.sin(playerAngle)*maxDepth), (playerY+math.cos(playerAngle)*maxDepth)), 3)

def drawMenu(actionCount, mouseSensitivity, fovMulti, resMulti, distanceMulti, devMode, render3d, showFPS):
    mouse = pygame.mouse.get_pos()
    mouseButtons = pygame.mouse.get_pressed()
    if  actionCount > 0 and not mouseButtons[0]:
        actionCount = 0
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
    mouseSensitivityText = menuFont.render(f"Mouse sensitivity: {round((mouseSensitivity*10), 1)}", True, pygame.Color('White'))
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

    if not devMode:
        #not dev mode FOV
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), fovMultiRect)
        fovMultiText = menuFont.render(f"FOV: {int(round((fov * (180/math.pi)), 0))}", True, pygame.Color('White'))
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
        
        #not dev mode resolution
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), resMultiRect)
        resMultiText = menuFont.render(f"Resolution: {int(castedRays*resMulti)}", True, pygame.Color('White'))
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

        #not dev mode distance
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), distanceMultiRect)
        distanceMultiText = menuFont.render(f"Rendering distance: {int(maxDepth*distanceMulti)}", True, pygame.Color('White'))
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
    devModeText = menuFont.render(f"Dev mode: {(str(devMode) + " (All numbers rounded to 5 decimals)" if devMode else devMode )}", True, pygame.Color('White'))
    menuSurf.blit(devModeText, (devModeRect.x + 2, devModeRect.y + 2))
    if devModeRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
            devMode = True if devMode == False else False
            actionCount+=1
    
    if devMode:
        #dev mode FOV
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), fovMultiRect)
        fovMultiText = menuFont.render(f"FOV: {round((fov * (180/math.pi)), 5)} degrees or {round(fov, 5)} radians", True, pygame.Color('White'))
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
        
        #dev mode resolution
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), resMultiRect)
        resMultiText = menuFont.render(f"Casted rays: {round((castedRays*resMulti), 5)} rounded to {int(castedRays*resMulti)}", True, pygame.Color('White'))
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

        #dev mode distance
        pygame.draw.rect(menuSurf, (100, 100, 100, 255), distanceMultiRect)
        distanceMultiText = menuFont.render(f"Render: {round((maxDepth*distanceMulti), 5)} pixels rounded to {int(maxDepth*distanceMulti)}", True, pygame.Color('White'))
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

        #dev mode only render3d
        pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if render3dRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), render3dRect)
        render3dText = menuFont.render(f"Render 3d: {render3d}", True, pygame.Color('White'))
        menuSurf.blit(render3dText, (render3dRect.x + 2, render3dRect.y + 2))
        if render3dRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
            render3d = True if render3d == False else False
            actionCount+=1
        
        #dev mode only showFPS
        pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if showFPSRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), showFPSRect)
        showFPStext = menuFont.render(f"Show FPS: {showFPS}", True, pygame.Color('White'))
        menuSurf.blit(showFPStext, (showFPSRect.x + 2, showFPSRect.y + 2))
        if showFPSRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
            showFPS = True if showFPS == False else False
            actionCount+=1
    
    pygame.draw.rect(menuSurf, ((150, 150, 150, 255) if exitRect.collidepoint(mouse) and not mouseButtons[0] else (100, 100, 100, 255)), exitRect)
    exitText = menuFont.render("Save and exit", True, pygame.Color('White'))
    menuSurf.blit(exitText, (exitRect.x + 2, exitRect.y + 2))
    if exitRect.collidepoint(mouse) and mouseButtons[0] and actionCount<1:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        actionCount+=1
    
    screen.blit(menuSurf, (0,0))
    return actionCount, mouseSensitivity, fovMulti, resMulti, distanceMulti, devMode, render3d, showFPS

def raycast(playerAngle, halfFov, fov, castedRays, playerX, playerY, rects, render3d, width, height):
    #draw ceiling and floor
    if render3d:
        pygame.draw.rect(screen, (175, 175, 175), (0, 0, width, (height/2)))
        pygame.draw.rect(screen, (100, 100, 100), (0, (height/2), width, (height/2)))
    startingAngle = playerAngle - halfFov
    angleIncrement = fov/castedRays
    angle = startingAngle
    largeStep = 20
    smallStep = 1
    for ray in range(castedRays):
        found_collision = False
        lastValidTarget = (0, 0)
        for depth in range(0, maxDepth, largeStep):
            targetX = playerX - math.sin(angle) * depth
            targetY = playerY + math.cos(angle) * depth
            if 0 <= targetX < width and 0 <= targetY < height:
                for rect in rects:
                    if rect.collidepoint((targetX, targetY)):
                        found_collision = True
                        lastValidTarget = (targetX, targetY)
                        break
            if found_collision:
                break
            else:
                lastValidTarget = (targetX, targetY)
        if found_collision:
            while depth > 0:
                depth -= smallStep
                targetX = playerX - math.sin(angle) * depth
                targetY = playerY + math.cos(angle) * depth
                if 0 <= targetX < width and 0 <= targetY < height:
                    collided = False
                    for rect in rects:
                        if rect.collidepoint((targetX, targetY)):
                            collided = True
                            break
                    if not collided:
                        lastValidTarget = (targetX, targetY)
                        break
                else:
                    break
        if found_collision:
            if not render3d:
                pygame.draw.line(screen, (255, 0, 0), (playerX, playerY), lastValidTarget)
        angle += angleIncrement
        if render3d:
            #draw walls
            projectionMulti = 150
            distX, distY = lastValidTarget
            distance = math.sqrt( (playerX-distX)**2 + (playerY-distY)**2 )
            distance = 1 if distance==0 else distance
            rectWidth, rectHeight = (int(width/castedRays)), int((height * projectionMulti) / distance)
            rectX, rectY = (rectWidth * ray), ((height - rectHeight) // 2)
            shade = 150 / (distance * 0.005)
            shade = min(max(shade, 0), 150)
            if ray == castedRays - 1:
                rectWidth = width - rectX
            pygame.draw.rect(screen, (shade, shade, shade), (rectX, rectY, rectWidth, rectHeight))
    
focus = True
menu = False
menuCloseFrame = False
while True:
    playerAngleDegrees = playerAngle * (180/math.pi)
    #set user changable constants
    fov = (math.pi / 3) * fovMulti
    halfFov = fov / 2
    castedRays = int(100 * resMulti)
    maxDepth = int(math.sqrt( (((width)**2)*distanceMulti) + (((height)**2)*distanceMulti) ))
    stepAngle = fov/castedRays
    #mouse things
    if not menu:
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(((width/2),(height/2)))
        if not menuCloseFrame:
            mouseX, mouseY = pygame.mouse.get_rel()
            mouseX = (mouseX * mouseSensitivity) * (math.pi / -180)
            playerAngle += mouseX
        else:
            pygame.mouse.get_rel()
            menuCloseFrame = False
    else:
        pygame.mouse.set_visible(True)
    #movement
    keys = pygame.key.get_pressed()
    movement = {
        pygame.K_w: (0, moveSpeed),
        pygame.K_a: (moveSpeed, 0),
        pygame.K_s: (0, -moveSpeed),
        pygame.K_d: (-moveSpeed, 0),
    }
    for key, (dx, dy) in movement.items():
        if keys[key]:
            x = dx * math.cos(playerAngle) - dy * math.sin(playerAngle)
            y = dx * math.sin(playerAngle) + dy * math.cos(playerAngle)
            #playerX += x
            #playerY += y
            newPlayerX = playerX + x
            newPlayerY = playerY + y
            if 6<=newPlayerX<=(width - 6):
                playerX = newPlayerX
            if 6<=newPlayerY<=(height - 6):
                playerY = newPlayerY
    #quit conditions
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                if menu:
                    menu=False
                    pygame.mouse.set_visible(False)
                    pygame.mouse.set_pos(((width/2),(height/2)))
                    menuCloseFrame = True
                elif not menu:
                    menu = True
            #sys.exit(0)
        #if event.type == pygame.ACTIVEEVENT:
        #    if event.gain == 0:  # Window lost focus
        #        focus = False
        #    else:  # Window regained focus
        #        focus = True
        #        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        #        drawMap()
        #        pygame.display.flip()
    #draw the map on screen
    if focus:
        drawMap(rects)
        raycast(playerAngle, halfFov, fov, castedRays, playerX, playerY, rects, render3d, width, height)
    if menu:
        actionCount, mouseSensitivity, fovMulti, resMulti, distanceMulti, devMode, render3d, showFPS = drawMenu(actionCount, mouseSensitivity, fovMulti, resMulti, distanceMulti, devMode, render3d, showFPS)
    if showFPS:
        fpsText = fps.render(f"FPS: {int(clock.get_fps())}", True, pygame.Color('green'))
        screen.blit(fpsText, (0, 0))
    pygame.display.flip()
    clock.tick(60)