# DECLARAÇÃO DE IMPORTS
import pygame, sys, os, random
from constants import *
from funcs import *
from stages import *
from classes import *




# INICIALIZAÇÕES
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)    
clock = pygame.time.Clock()
pygame.display.set_caption("Raft Wars")
    


def main(stage):
    enemies = [Fighter(screen, stage["ENEMIES_POS"][i], "enemy") for i in range(stage["NUM_OF_ENEMIES"])]
    #enemies = [Fighter(screen, (1100, LAUNCH_POINT[1] - 20), "enemy"), Fighter(screen, (1200, LAUNCH_POINT[1] - 20), "enemy")]
    ally = Fighter(screen, (LAUNCH_POINT[0] - 40, LAUNCH_POINT[1] - 20), "ally")
    ball = None
    powerMeter = PowerMeter(screen)
    turnList = [i for i in range(len(enemies) + 1)]
    turn = turnList[0]
    


    # MAIN LOOP
    while True:
        screenUpdate(screen, enemies, ally, ball, powerMeter, turn)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    powerMeter.changing = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if turn % (len(enemies) + 1) == 0 and ally.alive:
                        powerX, powerY = calculatePower(powerMeter.inner_width)
                        ball = Ball(screen, velx = powerX/1.8, vely = -powerY/1.8)
                        
                    resetPowerMeter(powerMeter)
                    



        if ball != None:
            # Check ball boundaries
            if ball.posx >= WINDOW_SIZE[0] + 10 or ball.posy >= WINDOW_SIZE[1] + 10 or ball.posx <= -20:
                ball = None
                turn += 1

        # Reset turn
        if turn >= (len(enemies) + 1):
            turn = 0

        # Enemies' turn
        if turn != 0 and ball == None:
            if enemies[turn-1].alive:
                ball = Ball(screen, -random.randint(15, 20), -random.randint(15, 20))
                ball.posx = enemies[turn-1].posx - 10
                ball.posy = enemies[turn-1].posy + 20 
            else:
                turn += 1




        pygame.display.update()
        clock.tick(60) 




if __name__ == '__main__':
    main(Stage2)


