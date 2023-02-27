import pygame
from pygame import Vector2

from ..settings import *
from ..framework import *


class Force:
    def __init__(self, name: str, value: Vector2, one_time: bool = True) -> None:
        self.name: str = name
        self.value: Vector2 = value
        self.one_time: bool = one_time
        
    def __str__(self) -> str:
        return f"Force({self.name}, {self.value}, {self.one_time})"
    
    def __repr__(self) -> str:
        return f"Force({self.name}, {self.value}, {self.one_time})"
    
    def magnitude(self) -> float:
        return self.value.magnitude()
    
    def direction(self) -> Vector2:
        return self.value.normalize()
    