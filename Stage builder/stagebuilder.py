# DECLARAÇÃO DE IMPORTS
import pygame, sys, os
from constants import *
from funcs import *
from stages import *
from classes import *




# INICIALIZAÇÕES
pygame.init()
screen = pygame.display.set_mode(WINDOWS_SIZE)    
clock = pygame.time.Clock()
pygame.display.set_caption("Stage builder")






def main(stage):

    dragging = False
    removing = False
    selectedColor = BROWN
    buttonsDic = {"gb": Button(screen, "Insert new rect", (20, 20), GREENISH, SELECTEDGREENISH),
                  "rb": Button(screen, "Delete rect", (20, 150), REDDISHBROWN, SELECTEDREDDISHBROWN)}



    # MAIN LOOP
    while True:
        screenUpdate(screen, stage, buttonsDic, selectedColor)
        mx, my = getMousePos()



        hoveringR, rect = hoveringRect(mx, my, stage)
        if hoveringR and dragging:
            dragRect(rect, mx, my)

        hoveringB, button = hoveringButton(mx, my, buttonsDic)

        hoveringO, coption = hoveringColorOption(mx, my)



        if removing:
            printRemoval(screen)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if hoveringR:
                        dragging = True

                        if removing:
                            deleteRect(stage, rect)
                            removing = False

                    if hoveringB:
                        if button.text == "Insert new rect":
                            insertNewRect(stage, selectedColor)
                            removing = False

                        if button.text == "Delete rect":
                            if not removing:
                                removing = True

                            else:
                                removing = False

                    if hoveringO:
                        selectedColor = coption



            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False



        pygame.display.update()
        clock.tick(60) 





# REEEE
if __name__ == '__main__':
    main(Stage1)






