import pygame
from ..settings import *


class Lifebar:
    def __init__(
        self,
        max_health: int,
        center_pos: tuple[int, int] = (100, 100),
        topleft_pos: tuple[int, int] | None = None,
        dim: tuple[int, int] = (100, 100),
        color_fg: tuple[int, int, int] = GREEN,
        color_bg: tuple[int, int, int] = RED,
        ) -> None:
        """Creates a lifebar. Can specify center position or topleft position.

        Args:
            max_health (int): Maximum health of the lifebar.
            center_pos (tuple[int, int], optional): Center position. Defaults to (100, 100).
            topleft_pos (tuple[int, int] | None, optional): Topleft position. Defaults to None.
            dim (tuple[int, int], optional): Rect dimension. Defaults to (100, 100).
            color_fg (tuple[int, int, int], optional): Foreground color. Defaults to GREEN.
            color_bg (tuple[int, int, int], optional): Background color. Defaults to RED.
        """        
        
        self.dim = dim
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.max_health = max_health
        self.health = max_health
        self.screen = pygame.display.get_surface()
        
        if topleft_pos is None:
            self.rect_fg = pygame.Rect(center_pos, dim)
            self.rect_fg.center = center_pos
            self.rect_bg = pygame.Rect(center_pos, dim)
            self.rect_bg.center = center_pos
        else:
            self.rect_fg = pygame.Rect(topleft_pos, dim)
            self.rect_bg = pygame.Rect(topleft_pos, dim)

    def draw(self) -> None:
        """Draws the lifebar on the screen.
        """        
        
        pygame.draw.rect(self.screen, self.color_bg, self.rrect)
        pygame.draw.rect(self.screen, self.color_fg, self.rect_fg)

    def update(self) -> None:
        """Updates the foreground rect width based on health.
        """        
        
        fg_width = self.health / self.max_health * self.width
        self.rect_fg = pygame.Rect((self.rect_fg.center), fg_width, self.rect.h)

    def take_damage(self, damage: int) -> None:
        """Takes damage and updates the lifebar.

        Args:
            damage (int): Damage to take.
        """        
        
        self.health -= damage 
        if self.health <= 0:
            self.health = 0
        
        self.update()
