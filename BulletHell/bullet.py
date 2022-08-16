import pygame
from common.settings import *
from common.ui_utils import *
from common.entity import Entity


class Bullet(Entity):
    def __init__(self, x, y, width, height, color, name):
        super().__init__(x, y, width, height, color, name)
        self.vel_mod = 8