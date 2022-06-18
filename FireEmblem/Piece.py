import pygame
from constants import *



class Piece:
    def __init__(self, screen, classe, pos, color='black'):
        self.screen = screen
        self.classe = classe
        self.pos = pos
        self.surf = pygame.transform.scale(pygame.image.load(f'assets/{color}_{self.classe}.PNG'), (60, 60))
        x, y = pos[0]+SQUARE_SIZE//2, pos[1]+SQUARE_SIZE//2
        self.rect = self.surf.get_rect(center = (x, y))

    def draw(self):
        self.screen.blit(self.surf, self.rect)



