import random 
import pygame
import sys
import time
from utils.settings import *
from utils.ui_utils import *
from player import Player
from enemy import Enemy


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)    
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Bullet Hell")

        self.init_game()
        self.game_loop()

    def game_loop(self):
        player_bullet_ready = pygame.USEREVENT + 0
        pygame.time.set_timer(player_bullet_ready, self.player.fire_rate)

        enemy_bullet_ready = pygame.USEREVENT + 1
        pygame.time.set_timer(enemy_bullet_ready, self.enemy.fire_rate)

        while True:
            self.screen.fill(NIGHTBLUE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.velx += -self.player.vel_mod

                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.velx += self.player.vel_mod

                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.vely += -self.player.vel_mod

                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.vely += self.player.vel_mod

                    if event.key == pygame.K_SPACE:
                        self.player.dashing = True

                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT or event.key == ord('a')):
                        self.player.velx -= -self.player.vel_mod

                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.velx -= self.player.vel_mod

                    if (event.key == pygame.K_UP or event.key == ord('w')):
                        self.player.vely -= -self.player.vel_mod

                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.vely -= self.player.vel_mod
                        
                if event.type == player_bullet_ready:
                    self.player.shoot(self.entities)
                
                if event.type == enemy_bullet_ready:
                    self.enemy.shoot(self.entities, self.player)

            self.screen_update()

            pygame.display.update()
            self.clock.tick(120)

    def init_game(self):
        self.player = Player(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2, 35, 35, YELLOW)
        self.player.set_center_position((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

        self.enemy = Enemy(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2, 35, 35, RED)
        self.enemy.set_center_position((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 - 300))

        self.entities = []
        self.entities.append(self.player)
        self.entities.append(self.enemy)

    def handle_player(self):
        if self.player.dashing:
            self.player.dash()
            self.player.current_dash_frames -= 1
            
        if self.player.current_dash_frames <= 0:
            self.player.set_intangible(False)
            self.player.dashing = False
            self.player.current_dash_frames = self.player.max_dash_frames

    def screen_update(self):
        self.handle_player()
        
        for entity in self.entities:
            entity.update()
            entity.draw(self.screen)
            entity.show_hitbox(self.screen)

