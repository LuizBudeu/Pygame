import pygame
from .particles import Sand, Water, Wood
from .particle_types import ParticleTypes
from .common.settings import *
from .common.funcs import *
from .common.ui_utils import *


rel: dict[ParticleTypes, Sand|Water|Wood] = {
    ParticleTypes.SAND: Sand,
    ParticleTypes.WATER: Water,
    ParticleTypes.WOOD: Wood,
}


class ParticleManager:
        def __init__(self, particles: list, grid: list[list[int]]):
            """Manages all the particles.

            Args:
                particles (list[ParticleTypes.SAND | ParticleTypes.WATER | ParticleTypes.WOOD]): game particles list.
                grid (list[list[int]]): GRID_SIZE x GRID_SIZE matrix.
            """
            self.particles = particles
            self.grid = grid
    
        def create_particle(self, type: ParticleTypes, mx: int = None, my: int = None, i: int = None, j: int = None):
            """Creates a particle at the given position (i, j or x, y).

            Args:
                type (ParticleTypes): particle type.
                mx (int, optional): mouse x position. Defaults to None.
                my (int, optional): mouse y position. Defaults to None.
                i (int, optional): i index. Defaults to None.
                j (int, optional): j index. Defaults to None.
            """
            if i is None and j is None:
                i, j = pos_to_ij(mx, my)
            self.particles.append(rel[type](i, j))
            
        def handle_particles(self, screen: pygame.Surface):
            """Handles all the particles.

            Args:
                screen (pygame.Surface): game screen.
            """
            for particle in self.particles:
                particle.update(self.grid)
                particle.draw(screen)
                pos = ij_to_pos(particle.i, particle.j)
                # write_text(screen, f"{particle.stationary}", 20, (255, 255, 255), pos)
        