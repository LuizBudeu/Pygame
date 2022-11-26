import pygame
from .particles import Sand, Water, Wood
from .particle_types import ParticleTypes
from .common.settings import *
from .common.funcs import *


rel = {
    ParticleTypes.SAND: Sand,
    ParticleTypes.WATER: Water,
    ParticleTypes.WOOD: Wood,
}


class ParticleManager:
        def __init__(self, particles: list, grid: list[list]):
            self.particles = particles
            self.grid = grid
    
        def create_particle(self, mx: int, my: int, type: ParticleTypes):
            i, j = pos_to_ij(mx, my)
            self.particles.append(rel[type](i, j))
            
        def handle_particles(self, screen: pygame.Surface):
            for particle in self.particles:
                particle.update()
                particle.draw(screen)
        