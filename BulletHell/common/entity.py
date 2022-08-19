import pygame
import math
from .settings import *
from lifebar import Lifebar



class Entity:
    unique_id = 0

    def __init__(self, x, y, width, height, color, name="unnamed_entity", max_health=999999):
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
        self.lifebar = None
        self.max_health = max_health
        self.health = max_health

    def update(self):
        if self.velx == 0 or self.vely == 0:
            self.x += self.velx
            self.y += self.vely
        else:
            self.x += self.velx / math.sqrt(2)
            self.y += self.vely / math.sqrt(2)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_center_position(self, center):
        self.x = center[0] - self.width / 2
        self.y = center[1] - self.height / 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

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

    def hit(self, other_rect):
        if self.rect.colliderect(other_rect):
            return True
        return False

    def out_of_bounds(self):
        if self.x + self.width + 10 < 0 or self.x > WINDOW_SIZE[0] + 10:
            return True
        elif self.y + self.height + 10 < 0 or self.y > WINDOW_SIZE[1] + 10:
            return True
        else:
            return False

    def take_damage(self, damage):
        self.health -= damage 
        if self.health <= 0:
            self.health = 0

    def alive(self):
        if self.health <= 0:
            return False
        else:
            return True

    def show_lifebars(self, screen):
        self.lifebar = Lifebar(self.x, self.y, 40, 6, self.max_health)
        self.lifebar.take_damage(self.max_health - self.health)  
        self.lifebar.set_center_position((self.rect.centerx, self.rect.centery - 30))
        self.lifebar.draw(screen)