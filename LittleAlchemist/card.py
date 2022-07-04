import pygame 
from settings import *


class Card:
    def __init__(self, name, level, combo_type, attack, defense, ):
        self.name = name
        self.level = int(level)
        self.combo_type = combo_type
        self.attack = int(attack)
        self.defense = int(defense)

    def draw(self, screen, center_pos=(100, 100), dim=(220, 270), color=YELLOW):
        self.rect = pygame.Rect(center_pos, dim)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
    