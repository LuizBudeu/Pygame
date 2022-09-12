import pygame
import math
from .common.settings import *
from .common.ui_utils import *
from .common.entity import Entity
from .bullet import Bullet


class Enemy(Entity):
    def __init__(self, x, y, width, height, color, name, max_health):
        super().__init__(x, y, width, height, color, name, max_health)
        self.vel_mod = 2
        self.fire_rate = 250
        self.intangible = False
        self.taken_damage = False
        self.max_hit_frames = 15
        self.current_hit_frames = self.max_hit_frames
        self.vision_range = WINDOW_SIZE[1] // 2

    def shoot(self, entities, player):
        if self.alive() and player.alive():
            if self.distance_to(player) < self.vision_range:
                bullet = Bullet(self.rect.centerx, self.rect.centery,
                                10, 10, REDDISHBROWN, 'enemy_bullet')
                bullet.set_center_position(self.rect.center)
                angle = self.get_bullet_direction(player)
                bullet.velx = bullet.vel_mod * math.cos(angle)
                bullet.vely = bullet.vel_mod * math.sin(angle)
                entities[bullet.id] = bullet

    def get_bullet_direction(self, player):
        center = self.get_center_position()
        player_center = player.get_center_position()
        angle = math.atan2(
            player_center[1] - center[1], player_center[0] - center[0])
        return angle

    def take_damage(self, damage, hit_sound, explosion_sound):
        if self.alive():
            self.taken_damage = True
            self.set_intangible(True)
            self.health -= damage
            hit_sound.play()
            if self.health <= 0:
                explosion_sound.play()
                self.name = 'to_be_deleted'

    def set_intangible(self, intangible):
        self.intangible = intangible
        if intangible:
            self.color = WHITE
        else:
            self.color = RED

    def distance_to(self, player):
        center = self.get_center_position()
        player_center = player.get_center_position()
        return math.sqrt((center[0] - player_center[0]) ** 2 + (center[1] - player_center[1]) ** 2)

    def show_range(self, screen):
        pygame.draw.circle(
            screen, RED, self.get_center_position(), self.vision_range, 1)
