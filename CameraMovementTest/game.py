import random 
import pygame
import sys
import time
from player import Player
from entity import Entity
from camera import Camera
from utils.settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)    
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Camera Movement Test")

        self.init_game()
        self.game_loop()

    def game_loop(self):
        while True:
            self.screen.fill(NIGHTBLUE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player.velx += -self.player.vel_mod

                    if event.key == pygame.K_d:
                        self.player.velx += self.player.vel_mod

                    if event.key == pygame.K_w:
                        self.player.vely += -self.player.vel_mod

                    if event.key == pygame.K_s:
                        self.player.vely += self.player.vel_mod

                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT or event.key == ord('a')):
                        self.player.velx -= -self.player.vel_mod

                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.velx -= self.player.vel_mod

                    if (event.key == pygame.K_UP or event.key == ord('w')):
                        self.player.vely -= -self.player.vel_mod

                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.vely -= self.player.vel_mod

            self.screen_update()

            pygame.display.update()
            self.clock.tick(120)

    def init_game(self):
        self.camera = Camera(self.screen)

        self.player = Player(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2, 35, 35, YELLOW, 'player')
        self.player.set_center_position((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

        enemies = [Entity(0, 0, 35, 35, RED, 'enemy', max_health=100) for i in range(3)]
        self.enemy.set_center_position((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 - 300))

        self.entities = {}
        self.add_entity(self.player)
        for i, enemy in enumerate(enemies):
            enemy.set_center_position((WINDOW_SIZE[0]/4*(i+1), WINDOW_SIZE[1]/2 - 300))
            self.add_entity(enemy)

    def add_entity(self, entity):
        self.entities[entity.id] = entity

    def screen_update(self):
        for entity in self.entities.values():
            entity.update()

        self.camera.draw(self.entities)
