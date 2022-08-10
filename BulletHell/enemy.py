import pygame
import math
from utils.settings import *
from utils.ui_utils import *
from entity import Entity
from bullet import Bullet


class Enemy(Entity):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.vel_mod = 2
        self.fire_rate = 250

    def shoot(self, entities, player):
        bullet = Bullet(self.center[0], self.center[1], 10, 10, REDDISHBROWN)
        bullet.set_center_position((self.center[0], self.center[1]))
        angle = self.get_bullet_direction(player)
        bullet.velx = bullet.vel_mod * math.cos(angle)
        bullet.vely = bullet.vel_mod * math.sin(angle)
        entities.append(bullet)

    def get_bullet_direction(self, player):
        center = self.get_center_position()
        player_center = player.get_center_position()
        angle = math.atan2(player_center[1] - center[1], player_center[0] - center[0])
        return angle