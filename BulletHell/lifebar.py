import pygame
from common.settings import *


class Lifebar:
    def __init__(self, x, y, width, height, color1=GREEN, color2=RED, max_health=10000):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dimension = (self.width, self.height)
        self.color1 = color1
        self.color2 = color2

        self.max_health = max_health
        self.health = max_health

        self.rrect = pygame.Rect(x, y, width, height)
        self.grect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color2, self.rrect)
        pygame.draw.rect(screen, self.color1, self.grect)

    def take_damage(self, damage):
        self.grect.width -= damage / self.max_health

    def set_center_position(self, center):
        self.x = center[0] - self.width / 2
        self.y = center[1] - self.height / 2
        self.rrect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.grect = pygame.Rect(self.x, self.y, self.width, self.height)
