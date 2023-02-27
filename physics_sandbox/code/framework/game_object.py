import pygame 
import math
from ..settings import *
from .ui_utils import *


class GameManagerObject:
    def __init__(
        self,
        center_pos: tuple[int, int] = (100, 100),
        topleft_pos: tuple[int, int] | None = None,
        dim: tuple[int, int] = (100, 100),
        surf: pygame.Surface | None = None,
        name: str = "GameManagerObject",
        rect_color: tuple[int, int, int] = RED,
        ) -> None:
        """This is the __init__ method of a class representing a game object in the framework.

        Arguments:
            center_pos: A tuple of two integers representing the center position of the game object on the screen. The default value is (100, 100).
            topleft_pos: A tuple of two integers representing the top-left position of the game object on the screen. This argument is optional and the default value is None.
            dim: A tuple of two integers representing the width and height of the game object. This argument is optional and the default value is None.
            surf: A Pygame surface representing the sprite image of the game object. This argument is optional and the default value is None.
            name: A string representing the name of the game object. The default value is "GameManagerObject".
            rect_color: A tuple of three integers representing the color of the rectangular area that surrounds the game object. The default value is RED (255, 0, 0).
        """        
        
        self.name = name
        self.surf = surf
        self.has_sprite = surf is not None
        self.rect_color = rect_color
        
        if not self.has_sprite:
            if topleft_pos is None:
                self.rect = pygame.Rect(center_pos, dim)
                self.rect.center = center_pos
            else:
                self.rect = pygame.Rect(topleft_pos, dim)
        else:
            self.rect = surf.get_rect(center=center_pos)
            
        self.screen = pygame.display.get_surface()
        self.velx = 0
        self.vely = 0
        self.velmax = 10
        self.active = True
        self.layer = 0
            
    def draw(
        self, 
        surface: pygame.Surface | None = None
        ) -> None:    
        
        """This is a method of a class representing a game object in the Pygame library. The method is used to draw the game object on the screen.
        
        Arguments:
            surface: A Pygame surface where the game object will be drawn. This argument is optional and the default value is None. If not specified, the game object will be drawn on the display screen.
        """            
    
        drawing_surf = surface or self.screen
        if self.has_sprite:
            drawing_surf.blit(self.surf, self.rect)
        else:
            pygame.draw.rect(drawing_surf, self.rect_color, self.rect)
            
    def update(self) -> None:
        """Update method for the game object. If active, this method is called every frame and is used to update the game object's position and other properties.
        """            
        
        if self.active:
            if self.velx == 0 or self.vely == 0:
                self.rect.x += self.velx
                self.rect.y += self.vely
            else:
                self.rect.x += self.velx / math.sqrt(2)
                self.rect.y += self.vely / math.sqrt(2)
                
    def write_name(self) -> None:
        """Writes the name of the game object on the rect center.
        """            
        
        write_text(self.name, self.rect.center, font_size=15, color=(255, 255, 255))
            