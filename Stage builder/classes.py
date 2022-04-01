import pygame
from constants import *
from funcs import *

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 20)




class Button:
    def __init__(self, screen, text, pos, color, tocolor):
        self.screen = screen
        self.text = text
        self.pos = pos
        self.color = color
        self.tocolor = tocolor

        self.rect = pygame.Rect(pos[0], pos[1], 160, 100)

    def draw(self):
        mx, my = getMousePos()
        if self.hoveringButton(mx, my):
            pygame.draw.rect(self.screen, self.tocolor, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)

        text_surface = font.render(self.text, True, DARKGRAY)
        text_rect = text_surface.get_rect(center = self.rect.center)
        self.screen.blit(text_surface, text_rect)

    
    def hoveringButton(self, mx, my):
        if self.rect.collidepoint(mx, my):
            return True
        
        return False


    



