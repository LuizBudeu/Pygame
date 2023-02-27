import sys

import pygame
from pygame import mixer
from pygame import Vector2 as Vec

from .settings import *
from .framework import *
from .framework.camera import Camera


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
        self.camera = Camera()
        self.player = GameObject(dim=Vec(100, 100)*WINDOW_SIZE[0]/WINDOW_SIZE[1], center_pos=Vec(*WINDOW_SIZE)/2, rect_color=RED, name="Player")
        self.wall = GameObject(dim=Vec(100, 100)*WINDOW_SIZE[0]/WINDOW_SIZE[1], center_pos=Vec(WINDOW_SIZE[0], 0), rect_color=YELLOW, name="Wall")
    
    def game_loop(self):
        while True:
            self.draw_background()

            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        # self.player.velx -= self.player.velmax
                        self.camera.vel += Vec(self.camera.velmax, 0)
                    if event.key == pygame.K_d:
                        # self.player.velx += self.player.velmax
                        self.camera.vel += Vec(-self.camera.velmax, 0)
                    if event.key == pygame.K_w:
                        # self.player.vely -= self.player.velmax
                        self.camera.vel += Vec(0, self.camera.velmax)
                    if event.key == pygame.K_s:
                        # self.player.vely += self.player.velmax
                        self.camera.vel += Vec(0, -self.camera.velmax)
                        
                    # Restart event
                    if event.key == pygame.K_r:
                        self.start_game()
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        # self.player.velx += self.player.velmax
                        self.camera.vel += Vec(-self.camera.velmax, 0)
                    if event.key == pygame.K_d:
                        # self.player.velx -= self.player.velmax
                        self.camera.vel += Vec(self.camera.velmax, 0)
                    if event.key == pygame.K_w:
                        # self.player.vely += self.player.velmax
                        self.camera.vel += Vec(0, -self.camera.velmax)
                    if event.key == pygame.K_s:
                        # self.player.vely -= self.player.velmax
                        self.camera.vel += Vec(0, self.camera.velmax)
            
            self.screen_update()
            pygame.display.update()
            self.clock.tick(FPS)
            
    def screen_update(self):
        self.player.update()
        self.player.draw()
        self.player.write_name()
        
        self.wall.update()
        self.wall.pos = self.wall.rect.center + self.camera.pos
        print(self.wall.pos)
        self.wall.draw()
        self.wall.write_name()
        
        self.camera.update()
        self.player.pos = self.player.rect.center + self.camera.pos
        # print(self.player.pos)
        
    def draw_everything(self):
        pass
        
    def draw_background(self):
        self.screen.fill(NIGHTBLUE)
        self.camera.draw_origin()
        