import random 
import pygame
from pygame import mixer
import sys
import time
from utils.settings import *
from utils.ui_utils import *
from player import Player
from enemy import Enemy
from camera import Camera


class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)    
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Bullet Hell")

        self.init_game()
        self.game_loop(show_hitboxes=False)

    def game_loop(self, show_hitboxes=False):
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
                    
                    if event.key == pygame.K_m:
                        if not self.muted:
                            self.mute_all_sounds()
                            self.muted = True
                        else:
                            self.unmute_all_sounds()
                            self.muted = False

                    if event.key == pygame.K_SPACE:
                        if self.player.can_dash:
                            self.player.dashing = True
                            self.player.can_dash = False
                            pygame.time.set_timer(self.player_dash_ready, self.player.dash_cooldown)

                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_a):
                        self.player.velx -= -self.player.vel_mod

                    if event.key == pygame.K_d:
                        self.player.velx -= self.player.vel_mod

                    if (event.key == pygame.K_w):
                        self.player.vely -= -self.player.vel_mod

                    if event.key == pygame.K_s:
                        self.player.vely -= self.player.vel_mod
                        
                if event.type == self.player_bullet_ready:
                    self.player.shoot(self.entities, self.bullet_sound)
                
                if event.type == self.enemy_bullet_ready:
                    self.enemy.shoot(self.entities, self.player)

                if event.type == self.player_dash_ready:
                    self.player.can_dash = True
                    pygame.time.set_timer(self.player_dash_ready, 0)

            self.screen_update(show_hitboxes)

            pygame.display.update()
            self.clock.tick(120)

    def init_game(self):
        self.camera = Camera(self.screen)

        self.player = Player(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2, 35, 35, YELLOW, 'player')
        self.player.set_center_position((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

        self.enemy = Enemy(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2, 35, 35, RED, 'enemy')
        self.enemy.set_center_position((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 - 300))

        self.entities = {}
        self.add_entity(self.player)
        self.add_entity(self.enemy)

        self.muted = False

        self.init_time_events()
        self.load_sounds()
        self.load_images()
        self.play_background_music() 

    def screen_update(self, show_hitboxes):
        self.handle_player()
        
        for entity in self.entities.values():
            self.camera.center_target_position(self.player)
            self.camera.update(entity)
            entity.update()
            entity.draw(self.screen)
            
        #self.camera.update(self.entities)
        #print(self.camera.offset)

        self.draw_ui()

    def init_time_events(self):
        self.player_bullet_ready = pygame.USEREVENT + 0
        pygame.time.set_timer(self.player_bullet_ready, self.player.fire_rate)

        self.enemy_bullet_ready = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_bullet_ready, self.enemy.fire_rate)

        self.player_dash_ready = pygame.USEREVENT + 2
        pygame.time.set_timer(self.player_dash_ready, 0)

    def load_images(self):
        unmuted_icon_surf = pygame.image.load("assets/images/unmuted_icon.png").convert_alpha()
        muted_icon_surf = pygame.image.load("assets/images/muted_icon.png").convert_alpha()

        self.images = {
            'unmuted_icon': unmuted_icon_surf,
            'muted_icon': muted_icon_surf
        }

    def load_sounds(self):
        mixer.music.load(f"assets/sound/music/gameloop{random.randint(1, 3)}.ogg")
        mixer.music.set_volume(0.2) 

        self.bullet_sound = mixer.Sound("assets/sound/effects/laser.wav")  
        self.dash_sound = mixer.Sound("assets/sound/effects/dash2.wav")

        self.sounds = {
            self.bullet_sound: {'volume': 0.03},
            self.dash_sound: {'volume': 0.07}
        }

        for sound in self.sounds:
            mixer.Sound.set_volume(sound, self.sounds[sound]['volume'])

    def play_background_music(self):
        mixer.music.play(-1)

    def mute_all_sounds(self):
        mixer.music.set_volume(0)
        for sound in self.sounds:
            mixer.Sound.set_volume(sound, 0)

    def unmute_all_sounds(self):
        mixer.music.set_volume(0.2)
        for sound in self.sounds:
            mixer.Sound.set_volume(sound, self.sounds[sound]['volume'])

    def handle_player(self):
        if self.player.dashing:
            self.player.dash(self.dash_sound)
            self.player.current_dash_frames -= 1
            
        if self.player.current_dash_frames <= 0:
            self.player.set_intangible(False)
            self.player.dashing = False
            self.player.current_dash_frames = self.player.max_dash_frames
     
    def draw_ui(self):
        self.draw_sound_icon()

    def draw_sound_icon(self):
        if not self.muted:
            self.screen.blit(self.images['unmuted_icon'], (WINDOW_SIZE[0] - 40, WINDOW_SIZE[1] - 40))
        else:
            self.screen.blit(self.images['muted_icon'], (WINDOW_SIZE[0] - 40, WINDOW_SIZE[1] - 40))
    
    def add_entity(self, entity):
        self.entities[entity.id] = entity
