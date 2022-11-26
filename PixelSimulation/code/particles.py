import pygame 
from .particle_types import ParticleTypes
from .common.settings import *
from .common.funcs import *


colors = {
    ParticleTypes.SAND: (196, 180, 33),
    ParticleTypes.WATER: (11, 125, 212),
    ParticleTypes.WOOD: (139, 69, 19),
}


class Particle:
    def __init__(self, i: int, j: int, type: ParticleTypes):
        x, y = ij_to_pos(i, j)
        self.rect = pygame.Rect(x, y, WINDOW_SIZE[0]//GRID_SIZE, WINDOW_SIZE[1]//GRID_SIZE)
        self.type = type
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, colors[self.type], self.rect)


class Sand(Particle):
    def __init__(self, i: int, j: int):
        super().__init__(i, j, ParticleTypes.SAND)

    def update(self):
        pass


class Water(Particle):
    def __init__(self, i: int, j: int):
        super().__init__(i, j, ParticleTypes.WATER)

    def update(self):
        pass
    

class Wood(Particle):
    def __init__(self, i: int, j: int):
        super().__init__(i, j, ParticleTypes.WOOD)

    def update(self):
        pass