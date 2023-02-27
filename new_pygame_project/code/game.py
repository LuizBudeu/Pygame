import sys

import pygame
from pygame import mixer
from pygame import Vector2 as Vec

from .settings import *
from .framework import *


i = 0
class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-
                              16, channels=2, buffer=512)
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Bullet Hell Pro")
        
    def start_game(self):
        self.init_game()
        self.game_loop()
        
    def init_game(self):
        self.origin = Vec()
    
    def game_loop(self):
        while True:
            self.screen.fill(NIGHTBLUE)

            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen_update()
            pygame.display.update()
            self.clock.tick(FPS)
            
    def screen_update(self):
        pass
        