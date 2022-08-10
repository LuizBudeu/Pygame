import pygame
import math
from utils.settings import *
from utils.ui_utils import *
from entity import Entity
from bullet import Bullet

class Player(Entity):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.vel_mod = 4
        self.dash_vel_mod = 8
        self.max_dash_frames = 15
        self.current_dash_frames = self.max_dash_frames
        self.fire_rate = 250 # time in ms
        self.intangible = False
        self.dashing = False

    def shoot(self, entities):
        bullet = Bullet(self.center[0], self.center[1], 10, 10, LIGHTBLUE)
        angle = self.get_bullet_direction()
        bullet.velx = bullet.vel_mod * math.cos(angle)
        bullet.vely = bullet.vel_mod * math.sin(angle)
        entities.append(bullet)

    def get_bullet_direction(self):
        mx, my = get_mouse_pos()
        center = self.get_center_position()
        angle = math.atan2(my - center[1], mx - center[0])
        return angle

    def set_intangible(self, intangible):
        self.intangible = intangible
        if intangible:
            self.color = LIGHTYELLOW
        else:
            self.color = YELLOW

    def dash(self):
        if self.current_dash_frames > 0:
            self.set_intangible(True)
            direction = self.get_dash_direction()
            self.x += self.dash_vel_mod * direction[0]
            self.y += self.dash_vel_mod * direction[1]

    def get_dash_direction(self):
        direction = [0, 0]
        if self.velx > 0:
            direction[0] = 1
        elif self.velx < 0:
            direction[0] = -1
        if self.vely > 0:
            direction[1] = 1
        elif self.vely < 0:
            direction[1] = -1
        return direction

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    