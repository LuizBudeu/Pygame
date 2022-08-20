import pygame 
from common.settings import *


class Camera:
    def __init__(self, screen):
        self.screen = screen
        self.offset = pygame.math.Vector2(100, 100)

    def center_target_position(self, target):
        self.offset.x = target.rect.centerx - WINDOW_SIZE[0] // 2
        self.offset.y = target.rect.centery - WINDOW_SIZE[1] // 2

    def draw(self, entities):
        self.center_target_position(entities[0])

        for entity in entities.values():
            offset_pos = entity.rect.topleft - self.offset
            pygame.draw.rect(self.screen, entity.color, (offset_pos, entity.dimension))



