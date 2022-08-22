import pygame 
from common.settings import *


class Camera:
    def __init__(self, screen):
        self.screen = screen
        self.offset = pygame.math.Vector2(100, 100)

    def center_target_position(self, target):
        self.offset.x = target.rect.centerx - WINDOW_SIZE[0] // 2
        self.offset.y = target.rect.centery - WINDOW_SIZE[1] // 2

    def update(self, entity):
        #self.center_target_position(entities[0])

        """ offset_pos = entity.rect.topleft - self.offset
        pygame.draw.rect(self.screen, entity.color, (offset_pos, entity.dimension)) """
        #new_pos = entity.rect.topleft - self.offset
        entity.rect.topleft = entity.rect.topleft - self.offset

        """ entity.rect.x = new_pos[0]
        entity.rect.y = new_pos[1] """

        #entity.rect = pygame.Rect(new_pos, entity.dimension)
        #print(entity.rect.topleft)

    def update_all(self, entities):
        self.center_target_position(entities[0])

        for entity in entities.values():
            entity.rect.topleft = entity.rect.topleft - self.offset



