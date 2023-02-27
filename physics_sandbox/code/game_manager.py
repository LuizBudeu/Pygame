import sys

import pygame
from pygame import mixer
from pygame import Vector2

from .settings import *
from .framework import *
from .physics.rigidbody import Rigidbody
from .physics.force import Force


class GameManager:
    def __init__(self) -> None:
        pygame.mixer.pre_init(frequency=44100, size=-
                              16, channels=2, buffer=512)
        pygame.mixer.init()
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        pygame.display.set_caption("Physics Sandbox")
        
    def start_game(self) -> None:
        self.init_game()
        self.game_loop()
        
    def init_game(self) -> None:
        self.origin: Vector2 = Vector2()
        self.all_objects: list = []
        self.event_callbacks: list[dict] = []
        
        self.create_ribidbody()
        self.create_floor()
    
    def game_loop(self) -> None:
        while True:
            self.screen.fill(NIGHTBLUE)

            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.rb.add_force(Force(
                            name="jump_force",
                            value=Vector2(0, -5),
                            one_time=True,
                        ))
                        
                    if event.key == pygame.K_ESCAPE:
                        self.start_game()
                        self.rb.velocity = Vector2()
                        self.rb.acceleration = Vector2()
                        self.rb.external_forces = []
                        
                    if event.key == pygame.K_a:
                        self.rb.add_force(Force(
                            name="left_force",
                            value=Vector2(-0.5, 0),
                            one_time=True,
                        ))
                        
                    if event.key == pygame.K_d:
                        self.rb.add_force(Force(
                            name="right_force",
                            value=Vector2(0.5, 0),
                            one_time=True,
                        ))
                    
            self.all_updates_and_draws()
            self.call_event_callbacks()
            pygame.display.update()
            self.clock.tick(FPS)
            
    def all_updates_and_draws(self) -> None:
        rb, floor = self.all_objects
        
        for obj in self.all_objects:
            obj.update(self)
            
            obj.draw(self.screen)
            
        if rb.colliding_with(floor):
            rb.ground(floor)
        
        if rb.is_grounded(floor):
            rb.add_normal_force()

            
        # # self.check_collisions()
            
    # def check_collisions(self) -> None:
    #     for obj in self.all_objects:
    #         for other in self.all_objects:
    #             if obj != other:
    #                 if obj.colliding_with(other):
    #                     print("Collision")
            
    def create_ribidbody(self) -> None:
        # self.rb: Rigidbody = Rigidbody(initial_velocity=Vector2(0, -5), gravity_scale=0)
        self.rb: Rigidbody = Rigidbody()
        self.rb.rect.center = (WINDOW_SIZE[0]//2, 400)
        
        self.rb.add_force(Force(
            name="jump_force",
            value=Vector2(0, -1),
            one_time=True,
        ))
        
        self.all_objects.append(self.rb)
        
    def create_floor(self) -> None:
        floor: Rigidbody = Rigidbody(
            body_type=Rigidbody.BODY_TYPES.STATIC,
            pos=(0, WINDOW_SIZE[1] - 100),
            dim=(WINDOW_SIZE[0], 100),
            color=YELLOW
        )
        
        self.all_objects.append(floor)
        
    def add_event_callback(self, callback: dict) -> None:
        self.event_callbacks.append(callback)
        
    def remove_event_callback(self, callback: dict) -> None:
        self.event_callbacks.remove(callback)
    
    def call_event_callbacks(self) -> None:
        for callback in self.event_callbacks:
            callback["function"](*callback["args"], **callback["kwargs"])
            self.remove_event_callback(callback)
    