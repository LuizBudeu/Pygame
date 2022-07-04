import pygame
from settings import *


class Button:
    def __init__(self, screen, text = "Insert text here", font_size = 20, dim = (200, 100), center_pos = (100, 50), bg_color = (154, 171, 170), bg_tocolor = (110, 122, 122)):
        self.font = pygame.font.Font("freesansbold.ttf", font_size)

        self.screen = screen
        self.text = text
        self.bg_color = bg_color
        self.bg_tocolor = bg_tocolor

        self.rect = pygame.Rect(center_pos[0] - dim[0]//2, center_pos[1] - dim[1]//2, dim[0], dim[1])

    def draw(self):
        mx, my = get_mouse_pos()
        if self.hovering(mx, my):
            pygame.draw.rect(self.screen, self.bg_tocolor, self.rect)
        else:
            pygame.draw.rect(self.screen, self.bg_color, self.rect)

        text_surface = self.font.render(self.text, True, DARKGRAY)
        text_rect = text_surface.get_rect(center = self.rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def hovering(self, mx, my):
        if self.rect.collidepoint(mx, my):
            return True
        return False



def write_text(screen, text='Insert text here', size=50, color=(196, 190, 0), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), topleft_pos = None):
    font = pygame.font.Font("freesansbold.ttf", size)
    text_surf = font.render(text, True, color)
    if not topleft_pos:
        text_rect = text_surf.get_rect(center=center_pos)
    else:
        text_rect = text_surf.get_rect(topleft=topleft_pos)
    screen.blit(text_surf, text_rect)

        