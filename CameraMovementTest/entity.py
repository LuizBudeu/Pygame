import pygame
import math
from utils.settings import *



class Entity:
    unique_id = 0

    def __init__(self, x, y, width, height, color, name="unnamed_entity"):
        self.name = name
        self.id = Entity.unique_id
        Entity.unique_id += 1

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dimension = (self.width, self.height)
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.velx = 0
        self.vely = 0
        self.vel_mod = 0

    def update(self):
        if self.velx == 0 or self.vely == 0:
            self.rect.x += self.velx
            self.rect.y += self.vely
        else:
            self.rect.x += self.velx / math.sqrt(2)
            self.rect.y += self.vely / math.sqrt(2)

    def set_center_position(self, center):
        self.rect.center = center

    def get_center_position(self):
        return self.rect.center

    def get_topleft_position(self):
        return self.rect.topleft

    def set_topleft_position(self, topleft):
        self.rect.topleft = topleft

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def show_hitbox(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 2)
