import pygame
import math
from common.settings import *
from common.ui_utils import *
from common.entity import Entity
from bullet import Bullet
from lifebar import Lifebar


class Enemy(Entity):
    def __init__(self, x, y, width, height, color, name, max_health):
        super().__init__(x, y, width, height, color, name, max_health)
        self.vel_mod = 2
        self.fire_rate = 250

    def shoot(self, entities, player):
        bullet = Bullet(self.rect.centerx, self.rect.centery, 10, 10, REDDISHBROWN, 'bullet')
        bullet.set_center_position((self.rect.centerx, self.rect.centery))
        angle = self.get_bullet_direction(player)
        bullet.velx = bullet.vel_mod * math.cos(angle)
        bullet.vely = bullet.vel_mod * math.sin(angle)
        entities[bullet.id] = bullet

    def get_bullet_direction(self, player):
        center = self.get_center_position()
        player_center = player.get_center_position()
        angle = math.atan2(player_center[1] - center[1], player_center[0] - center[0])
        return angle

    def show_lifebars(self, screen):
        self.lifebar = Lifebar(self.x, self.y, 50, 10, max_health=self.max_health)
        self.lifebar.take_damage(self.max_health - self.health)
        self.lifebar.set_center_position((self.rect.centerx, self.rect.centery - 30))
        self.lifebar.draw(screen)

    