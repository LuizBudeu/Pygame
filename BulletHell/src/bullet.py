import pygame
import math
from .common.settings import *
from .common.ui_utils import *
from .common.entity import Entity


class Bullet(Entity):
    def __init__(self, x, y, width, height, color, name):
        super().__init__(x, y, width, height, color, name)
        self.vel_mod = 8
        self.inital_pos = (self.x, self.y)
        self.max_distance = WINDOW_SIZE[1]

    def distance_traveled(self):
        return math.sqrt((self.x - self.inital_pos[0]) ** 2 + (self.y - self.inital_pos[1]) ** 2)
