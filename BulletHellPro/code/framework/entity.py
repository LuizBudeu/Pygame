import pygame
from .game_object import GameObject
from .lifebar import Lifebar
from ..settings import *


class Entity(GameObject):    
    def __init__(
            self, 
            max_health: int = 100, 
            invulnerable: bool = False,
            show_lifebar: bool = True,
            *args, 
            **kwargs
        ) -> None:
        """Entity class. GameObject with health and lifebar, can be hit if not invulnerable.

        Args:
            max_health (int, optional): _description_. Defaults to 100.
            invulnerable (bool, optional): _description_. Defaults to False.
        """        
        
        super().__init__(*args, **kwargs)
        self.max_health = max_health
        self.health = max_health
        self.invulnerable = invulnerable
        if show_lifebar:
            self.lifebar = Lifebar(self.max_health, (self.rect.centerx, self.rect.centery - 30), dim=self.rect.size)

        
    def show_hitbox(self) -> None:
        """Shows the hitbox rect of the entity.
        """
        pygame.draw.rect(self.screen, WHITE, self.rect, 1)
        
    def hit(self, other_rect: pygame.Rect) -> None:
        """Checks if the entity is hit by another rect.

        Args:
            other_rect (pygame.Rect): Other rect to check collision with.

        Returns:
            bool: True if hit, False otherwise.
        """        
        
        if self.rect.colliderect(other_rect):
            return True
        return False
    
    def out_of_bounds(self) -> None:
        """Checks if the entity is out of bounds.

        Returns:
            bool: True if out of bounds, False otherwise.
        """        
        
        if self.rect.x + self.rect.w + 10 < 0 or self.rect.x > WINDOW_SIZE[0] + 10:
            return True
        elif self.rect.y + self.rect.h + 10 < 0 or self.rect.y > WINDOW_SIZE[1] + 10:
            return True
        else:
            return False
        
    def take_damage(self, damage: int) -> None:
        """Takes damage if not invulnerable.

        Args:
            damage (int): Damage to take.
        """        
        
        if not self.invulnerable:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                
        if hasattr(self, 'lifebar'):
            self.lifebar.take_damage(damage)
                
    def show_lifebars(self) -> None:
        """Shows the lifebar of the entity.
        """        
        
        self.lifebar.draw()
