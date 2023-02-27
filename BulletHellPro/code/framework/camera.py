import pygame
from pygame import Vector2 as Vec

from ..settings import *


class Camera:
    def __init__(self) -> None:
        """Initialize the camera"""
        
        self.screen_pos = Vec()
        self.pos = self.screen_pos
        self.vel = Vec()
        self.velmax = 3
        self.screen = pygame.display.get_surface()
        
    def update(self) -> None:
        """Update the camera position"""
        
        self.screen_pos += self.vel
        self.pos = -self.screen_pos
        # print(self.pos, self.screen_pos)
    
    def draw_origin(self):
        """Draw the origin (0, 0)"""
        
        pygame.draw.circle(self.screen, RED, self.screen_pos, 10)
        
    