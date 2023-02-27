from __future__ import annotations

# import pygame
# from pygame import Vector2
# from enum import Enum

# from .settings import *
# from .framework import *


# class Rigidbody:
    
#     class BODY_TYPES(Enum):
#         DYNAMIC: int = 0
#         KINEMATIC: int = 1
#         STATIC: int = 2
    
#     def __init__(
#             self,
#             body_type: BODY_TYPES = BODY_TYPES.DYNAMIC,
#             mass: float = 1., 
#             initial_velocity: Vector2 = Vector2(), 
#             initial_acceleration: Vector2 = Vector2(),
#             is_affected_by_gravity: bool | None = None,
#             gravity_scale: float = 1.,
#             pos: tuple[int, int] = (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2),
#             dim: tuple[int, int] = (100, 100),
#             color: tuple[int, int, int] = RED,
#         ) -> None:
        
#         self.body_type: BODY_TYPES = body_type
#         self.mass: float = mass
#         self.velocity: Vector2 = initial_velocity
#         self.acceleration: Vector2 = initial_acceleration
#         self.gravity_scale: float = gravity_scale
        
#         self.max_x_velocity: float = 10.
        
#         if is_affected_by_gravity is None:
#             if body_type == Rigidbody.BODY_TYPES.STATIC:
#                 is_affected_by_gravity = False
#             else:
#                 is_affected_by_gravity: bool = True
            
#         self.is_affected_by_gravity: bool = is_affected_by_gravity
        
#         self.rect: pygame.Rect = pygame.Rect(pos, dim)
#         self.color: tuple[int, int, int] = color        
        
#         self.external_forces: list[dict] = []
#         if self.is_affected_by_gravity:
#             self.external_forces.append({
#                 "value": Vector2(0, GRAVITY * self.gravity_scale),
#                 "one_time": False,
#             })
            
#         print(self.external_forces)

#     def apply_force(self, force: Vector2) -> None:
#         self.acceleration += force / self.mass
        
#     def add_force(self, force_dict: dict) -> None:
#         if self.body_type != Rigidbody.BODY_TYPES.STATIC:
#             self.external_forces.append(force_dict)

#     def update(self) -> None:
#         if self.body_type != Rigidbody.BODY_TYPES.STATIC:
#             # additional_acceleration: Vector2 = Vector2()
#             # if self.is_affected_by_gravity:
#             #     additional_acceleration = Vector2(0, GRAVITY * self.gravity_scale)

#             # # print(self.acceleration)
#             # self.velocity += self.acceleration + additional_acceleration
#             # print(self.acceleration.y)
            
#             # self.rect.center += self.velocity
            
#             sum_of_forces: Vector2 = self.get_sum_of_forces()
#             print(sum_of_forces)
#             self.apply_force(sum_of_forces)
            
#             self.velocity += self.acceleration
#             self.clamp_velocity(-self.max_x_velocity, self.max_x_velocity)
            
#             self.rect.center += self.velocity
                
#     def draw(self, screen: pygame.Surface) -> None:
#         pygame.draw.rect(screen, self.color, self.rect)
        
#     def colliding_with(self, other) -> bool:
#         return self.rect.colliderect(other.rect)
    
#     def get_sum_of_forces(self) -> Vector2:
#         sum_of_forces: Vector2 = Vector2()
#         for force_dict in self.external_forces:
#             sum_of_forces += force_dict["value"]
            
#             if force_dict["one_time"]:
#                 self.external_forces.remove(force_dict)
                
#         return sum_of_forces
    
#     def clamp_velocity(self, min_value: float, max_value: float) -> None:
#         self.velocity.x = max(min(self.velocity.x, max_value), min_value)
            

import pygame
from pygame import Vector2
from enum import Enum
from .force import Force

from ..settings import *
from ..framework import *


class Rigidbody:
    
    class BODY_TYPES(Enum):
        DYNAMIC: int = 0
        KINEMATIC: int = 1
        STATIC: int = 2
    
    def __init__(
            self,
            body_type: BODY_TYPES = BODY_TYPES.DYNAMIC,
            mass: float = 1., 
            initial_velocity: Vector2 = Vector2(), 
            initial_acceleration: Vector2 = Vector2(),
            is_affected_by_gravity: bool | None = None,
            gravity_scale: float = 1.,
            friction_coefficient: float = 0.1,
            pos: tuple[int, int] = (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2),
            dim: tuple[int, int] = (100, 100),
            color: tuple[int, int, int] = RED,
        ) -> None:
        
        self.body_type: BODY_TYPES = body_type
        self.mass: float = mass
        self.velocity: Vector2 = initial_velocity
        self.acceleration: Vector2 = initial_acceleration
        self.gravity_scale: float = gravity_scale
        self.friction_coefficient: float = friction_coefficient

        if is_affected_by_gravity is None:
            if body_type == Rigidbody.BODY_TYPES.STATIC:
                is_affected_by_gravity = False
            else:
                is_affected_by_gravity: bool = True
            
        self.is_affected_by_gravity: bool = is_affected_by_gravity
        
        self.rect: pygame.Rect = pygame.Rect(pos, dim)
        self.color: tuple[int, int, int] = color        
        
        self.resultant_force_value: Vector2 = Vector2()
        self.external_forces: list[dict] = []
        if self.is_affected_by_gravity:
            self.add_force(Force(
                name = "gravity_force",
                value = self.mass * Vector2(0, GRAVITY * self.gravity_scale),
                one_time = False,
            ))        
        
    def update(self, GameManager) -> None:
        
        if self.body_type != Rigidbody.BODY_TYPES.STATIC:
            
            # if -PRECISION < self.velocity.x < PRECISION and self.velocity.x != 0:
            if self.velocity.x != 0:
                self.add_force(Force(
                    name = "friction_force",
                    value = self.mass * Vector2(-GRAVITY * self.gravity_scale, 0) * self.friction_coefficient * self.velocity.x / abs(self.velocity.x),
                    one_time = True,  # Para todo loop adiciona a força, mas one_time remove
                ))
            
            GameManager.add_event_callback({
                "function": self.visualize_forces,
                "args": [GameManager.screen, self.external_forces.copy()],
                "kwargs": {},
            })
            
            print(self.external_forces)
            
            self.resultant_force_value = self.get_resultant_force_value()
            self.apply_force_value(self.resultant_force_value)
            self.velocity += self.acceleration
            self.rect.center += self.velocity
        
    def add_force(self, force: Force) -> None:
        if self.body_type != Rigidbody.BODY_TYPES.STATIC:
            self.external_forces.append(force)
            
    def apply_force_value(self, force: Vector2) -> None:
        self.acceleration += force / self.mass
                
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect)
        
    def colliding_with(self, other: Rigidbody) -> bool:
        return self.rect.colliderect(other.rect)
    
    def is_grounded(self, floor: Rigidbody) -> bool:
        return self.velocity.y == 0 and self.rect.bottom == floor.rect.top
    
    def ground(self, floor: Rigidbody) -> None:
        self.rect.bottom = floor.rect.top
        self.velocity.y = 0
    
    def add_normal_force(self) -> None:
        self.add_force(Force(
            name="normal_force",
            value=self.mass * Vector2(0, -GRAVITY * self.gravity_scale),
            one_time=True,
        ))
        
    def get_resultant_force_value(self) -> Vector2:
        self.remove_duplicate_forces()
        
        sum_of_forces: Vector2 = Vector2()
        for force in self.external_forces:
            sum_of_forces += force.value
            
            if force.one_time:
                self.external_forces.remove(force)
                
        return sum_of_forces
    
    # Passando external_forces como argumento para que todas as forças possam ser visualizadas antes de serem removidas
    def visualize_forces(self, screen: pygame.Surface, external_forces: list[dict]) -> None:        
        for force in external_forces:
            force_value: Vector2 = force.value * 1000
            color: tuple = FORCE_COLORS.get(force.name, WHITE)
            pygame.draw.line(screen, color, self.rect.center, self.rect.center + force_value, 4)
            
    def remove_duplicate_forces(self) -> None:
        self.external_forces = list({f.name: f for f in self.external_forces}.values())
                        

            


