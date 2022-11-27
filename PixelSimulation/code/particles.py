import pygame 
from .particle_types import ParticleTypes
from .common.settings import *
from .common.funcs import *


colors: dict[ParticleTypes, tuple[int, int, int]] = {
    ParticleTypes.SAND: (196, 180, 33),
    ParticleTypes.WATER: (11, 125, 212),
    ParticleTypes.WOOD: (139, 69, 19),
}


class Particle:
    def __init__(self, i: int, j: int, type: ParticleTypes):
        """Base particle class. Particle types inherit from this class.

        Args:
            i (int): i index.
            j (int): j index.
            type (ParticleTypes): particle type.
        """
        self.i = i 
        self.j = j
        x, y = ij_to_pos(i, j)
        self.rect = pygame.Rect(x, y, WINDOW_SIZE[0]//GRID_SIZE, WINDOW_SIZE[1]//GRID_SIZE)
        self.type = type
        self.previ = None 
        self.prevj = None
        self.stationary = False
        
    def update(self):
        """Updates the particle. 

        Raises:
            NotImplementedError: Base particle does not implement update method.
        """
        raise NotImplementedError("This method must be implemented in a subclass.")
    
    def draw(self, screen: pygame.Surface):
        """Draws the particle to the screen.

        Args:
            screen (pygame.Surface): game screen.
        """
        pygame.draw.rect(screen, colors[self.type], self.rect)


class Sand(Particle):
    def __init__(self, i: int, j: int):
        """Sand particle at index i, j.

        Args:
            i (int): i index.
            j (int): j index.
        """
        super().__init__(i, j, ParticleTypes.SAND)
        self.frame_velocity = 10

    def update(self, grid: list[list[int]], frame_count: int = 0):
        if not self.stationary:
            self.previ = self.i
            self.prevj = self.j
        
        if 0 < self.i+1 < GRID_SIZE and 0 < self.j+1 < GRID_SIZE:
            if grid[self.i][self.j+1] == 0:
                self.j += 1
                # print('sand falling')
            elif grid[self.i-1][self.j+1] == 0:
                self.i -= 1
                self.j += 1
                # print('left')
            elif grid[self.i+1][self.j+1] == 0:
                self.i += 1
                self.j += 1
                # print('right')
            else: 
                self.stationary = True
        else:
            self.stationary = True
        
        self.rect.topleft = ij_to_pos(self.i, self.j)
        # print(self.i, self.j)

class Water(Particle):
    def __init__(self, i: int, j: int):
        """Water particle at index i, j.

        Args:
            i (int): i index.
            j (int): j index.
        """
        super().__init__(i, j, ParticleTypes.WATER)

    def update(self, grid):
        pass
    

class Wood(Particle):
    def __init__(self, i: int, j: int):
        """Wood particle at index i, j.

        Args:
            i (int): i index.
            j (int): j index.
        """
        super().__init__(i, j, ParticleTypes.WOOD)

    def update(self, grid):
        pass