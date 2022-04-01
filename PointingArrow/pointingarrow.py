import pygame, sys
import math



pygame.init()
screen = pygame.display.set_mode((600, 600))    
clock = pygame.time.Clock()
pygame.display.set_caption("Pointing arrow")



ORIGIN = (screen.get_width()//2, screen.get_height()//2)
LENGTH = 200



def calculatePoint(mx, my):
    try:
        a = math.atan((ORIGIN[1] - my)/(mx - ORIGIN[0]))

        if mx - ORIGIN[0] > 0 and ORIGIN[1] - my > 0:
            if 0 < a < math.pi:
                return int(ORIGIN[0] + LENGTH*math.cos(a)), int(ORIGIN[1] - LENGTH*math.sin(a))
        
        else:
            if mx - ORIGIN[0] < 0:
                return ORIGIN[0], ORIGIN[1] - LENGTH
            elif ORIGIN[1] - my < 0:
                return ORIGIN[0] + LENGTH, ORIGIN[1]

    except:
        pass
    
def drawArrow(mx, my):
    pygame.draw.line(screen, (255, 255, 255), ORIGIN, calculatePoint(mx, my), 5)


while True:
    screen.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()
    drawArrow(mx, my)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



    pygame.display.update()
    clock.tick(60)
