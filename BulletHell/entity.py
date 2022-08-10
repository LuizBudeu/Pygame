import pygame
import math
from utils.settings import *



class Entity:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = (x + self.width / 2, y + self.height / 2)
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.velx = 0
        self.vely = 0
        self.vel_mod = 5

    def update(self):
        if self.velx == 0 or self.vely == 0:
            self.x += self.velx
            self.y += self.vely
        else:
            self.x += self.velx / math.sqrt(2)
            self.y += self.vely / math.sqrt(2)

        self.center = (self.x + self.width / 2, self.y + self.height / 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_center_position(self, center):
        self.x = center[0] - self.width / 2
        self.y = center[1] - self.height / 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_center_position(self):
        return self.x + self.width / 2, self.y + self.height / 2

    def get_topleft_position(self):
        return self.x, self.y

    def set_topleft_position(self, topleft):
        self.x = topleft[0]
        self.y = topleft[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def show_hitbox(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 2)
