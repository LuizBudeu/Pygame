import pygame
from pygame import mixer
import math
from utils.settings import *
from utils.ui_utils import *
from entity import Entity
from bullet import Bullet

class Player(Entity):
    def __init__(self, x, y, width, height, color, name=None):
        super().__init__(x, y, width, height, color, name)
        self.vel_mod = 4
        self.dash_vel_mod = 8
        self.max_dash_frames = 15
        self.current_dash_frames = self.max_dash_frames
        self.fire_rate = 250 # time in ms
        self.intangible = False
        self.dashing = False
        self.dash_cooldown = 1000 # time in ms
        self.can_dash = True

    def shoot(self, entities, bullet_sound):
        bullet = Bullet(self.rect.centerx, self.rect.centery, 10, 10, LIGHTBLUE)
        bullet.set_center_position(self.rect.center)
        angle = self.get_bullet_direction()
        bullet.velx = bullet.vel_mod * math.cos(angle)
        bullet.vely = bullet.vel_mod * math.sin(angle)
        entities[bullet.id] = bullet

        bullet_sound.play()  

    def get_bullet_direction(self):
        mx, my = get_mouse_pos()
        offx = self.rect.centerx - WINDOW_SIZE[0] // 2
        offy = self.rect.centery - WINDOW_SIZE[1] // 2
        mx, my = mx + offx, my + offy
        print(f"mx: {mx}, my: {my}")
        center = self.get_center_position()
        print(center)
        angle = math.atan2(my - center[1], mx - center[0])
        return angle

    def set_intangible(self, intangible):
        self.intangible = intangible
        if intangible:
            self.color = LIGHTYELLOW
        else:
            self.color = YELLOW

    def dash(self, dash_sound):
        if self.current_dash_frames > 0:
            self.set_intangible(True)
            direction = self.get_dash_direction()

            if self.velx == 0 or self.vely == 0:
                self.x += self.dash_vel_mod * direction[0]
                self.y += self.dash_vel_mod * direction[1]
            else:
                self.x += self.dash_vel_mod * direction[0] / math.sqrt(2)
                self.y += self.dash_vel_mod * direction[1] / math.sqrt(2)

            dash_sound.play()

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

    