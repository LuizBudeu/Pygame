import sys
import pygame
from pygame import mixer
from pygame import Vector2 as Vec

from .settings import *
from .framework import *
from .framework.subject import Subject
from .player import Player


class Game(Subject):
    def __init__(self):
        super().__init__()
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
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
        self.player = Player()
        
        self.add_observer(self.player)
        self.notify_observer(self.player, Player.Actions.MOVE_UP)
    
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
        