import pygame
import math
from constants import *

pygame.init()
time0 = 0


def showMainMenu(screen):
    pass


def screenUpdate(screen, enemies, ally, ball, powerMeter, turn):
    global time0

    screen.fill(LIGHTBLUE)
    handleEnemies(enemies, turn)
    ally.draw()
    handlePowerMeter(powerMeter)
    drawArrow(screen)

    if ball != None:
        handleBall(ball)

        hitEnemy, enemy = checkEnemyHit(ball, enemies)
        if hitEnemy:
            if enemy.alive:
                time1 = pygame.time.get_ticks()
                if time1 - time0 >= 600:
                    enemy.calculateDamage(ball)
                time0 = pygame.time.get_ticks()

        elif checkAllyHit(ball, ally):
            if turn != 0:
                time1 = pygame.time.get_ticks()
                if time1 - time0 >= 600:
                    ally.calculateDamage(ball)
                time0 = pygame.time.get_ticks()
        



def getMousePos():
    return pygame.mouse.get_pos()


def handleEnemies(enemies, turn):
    drawEnemies(enemies)


def drawEnemies(enemies):
    for enemy in enemies:
        enemy.draw()
            


def handleBall(ball):
    ball.posx += ball.velx
    ball.vely += GRAVITY
    ball.posy += ball.vely 
    ball.draw((round(ball.posx), round(ball.posy)))



def handlePowerMeter(powerMeter):
    powerMeter.draw()
    
    if powerMeter.changing:
        powerMeter.changeStrength()


def resetPowerMeter(powerMeter):
    powerMeter.changing = False
    powerMeter.inner_width = 1


def calculatePoint():
    mx, my = getMousePos()

    try:
        a = math.atan((LAUNCH_POINT[1] - my)/(mx - LAUNCH_POINT[0]))

        if mx - LAUNCH_POINT[0] > 0 and LAUNCH_POINT[1] - my > 0:
            if 0 < a < math.pi:
                return int(LAUNCH_POINT[0] + LINE_LENGTH*math.cos(a)), int(LAUNCH_POINT[1] - LINE_LENGTH*math.sin(a))
        
        else:
            if mx - LAUNCH_POINT[0] < 0:
                return LAUNCH_POINT[0], LAUNCH_POINT[1] - LINE_LENGTH
            elif LAUNCH_POINT[1] - my < 0:
                return LAUNCH_POINT[0] + LINE_LENGTH, LAUNCH_POINT[1]

    except:
        pass
    
def drawArrow(screen):
    endPoint = calculatePoint()

    if endPoint != None:
        pygame.draw.line(screen, (227, 227, 227), LAUNCH_POINT, endPoint, 3)
    else:
        pygame.draw.line(screen, (227, 227, 227), LAUNCH_POINT, (LAUNCH_POINT[0] + LINE_LENGTH, LAUNCH_POINT[1]), 3)


def calculatePower(length):
    mx, my = getMousePos()

    if mx - LAUNCH_POINT[0] != 0:
        a = math.atan((LAUNCH_POINT[1] - my)/(mx - LAUNCH_POINT[0]))

        if mx - LAUNCH_POINT[0] > 0 and LAUNCH_POINT[1] - my > 0:
            if 0 < a < math.pi:
                return int(length*math.cos(a)), int(length*math.sin(a))
        
        else:
            if mx - LAUNCH_POINT[0] < 0:
                return 0, length
            elif LAUNCH_POINT[1] - my < 0:
                return length, 0
    
    else: return 0, length


def checkEnemyHit(ball, enemies): 
    for enemy in enemies:
        if ball.rect.colliderect(enemy):
            return True, enemy

    return False, None
        

def checkAllyHit(ball, ally):
    if ball.rect.colliderect(ally):
        return True 

    return False

