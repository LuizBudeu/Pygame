import pygame
from utils.settings import *
from utils.ui_utils import *
from entity import Entity


class Bullet(Entity):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.vel_mod = 8