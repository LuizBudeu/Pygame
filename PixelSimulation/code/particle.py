import pygame 
from .particle_types import ParticleTypes
from .common.settings import *


colors = {
    ParticleTypes.SAND: (196, 180, 33),
    ParticleTypes.WATER: (11, 125, 212),
    ParticleTypes.WOOD: (139, 69, 19),
}


class Particle:
    def __init__(self, i, j, type):
        self.rect = pygame.Rect(i*WINDOW_SIZE[0]//GRID_SIZE, j*WINDOW_SIZE[1]//GRID_SIZE, WINDOW_SIZE[0]//GRID_SIZE, WINDOW_SIZE[1]//GRID_SIZE)
        self.type = type
    
    def update(self):
        pass
    
    def draw(self, screen):
        pygame.draw.rect(screen, colors[self.type], self.rect)