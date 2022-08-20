import pygame
from common.settings import *
from common.ui_utils import *
from common.entity import Entity


class Item(Entity):
    def __init__(self, x, y, width, height, color, name, surf):
        super().__init__(x, y, width, height, color, name)
        self.surf = surf
        self.rect = self.surf.get_rect()

    def apply_effect(self, player):
        player.fire_rate = 50

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

    # This method is necessary as to not call the parent's method
    def update(self):
        pass

