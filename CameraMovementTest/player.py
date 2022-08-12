import pygame
import math
from utils.settings import *
from entity import Entity

class Player(Entity):
    def __init__(self, x, y, width, height, color, name):
        super().__init__(x, y, width, height, color, name)
        self.vel_mod = 4
