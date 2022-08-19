import random 
import pygame
from pygame import mixer
import sys
import time
from common.settings import *
from common.ui_utils import *
from player import Player
from enemy import Enemy


class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)    
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Bullet Hell")

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
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.velx += -self.player.vel_mod

                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.velx += self.player.vel_mod

                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.vely += -self.player.vel_mod

                    if event.key == pygame.K_DOWN or event.key == ord('s'):
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
                    if (event.key == pygame.K_LEFT or event.key == ord('a')):
                        self.player.velx -= -self.player.vel_mod

                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.velx -= self.player.vel_mod

                    if (event.key == pygame.K_UP or event.key == ord('w')):
                        self.player.vely -= -self.player.vel_mod

                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.vely -= self.player.vel_mod
                        
                if event.type == self.player_bullet_ready:
                    self.player.shoot(self.entities, self.bullet_sound)
                
                if event.type == self.enemy_bullet_ready:
                    self.enemy.shoot(self.entities, self.player)

                if event.type == self.player_dash_ready:
                    self.player.can_dash = True
                    pygame.time.set_timer(self.player_dash_ready, 0)

            self.screen_update()

            pygame.display.update()
            self.clock.tick(120)

    def init_game(self):
        self.player = Player(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2, 35, 35, YELLOW, 'player', max_health=100)
        self.player.set_center_position((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

        self.enemy = Enemy(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2, 35, 35, RED, 'enemy', max_health=100)
        self.enemy.set_center_position((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 - 300))

        self.entities = {}
        self.add_entity(self.player)
        self.add_entity(self.enemy)

        self.muted = False

        self.init_time_events()
        self.load_sounds()
        self.load_images()
        self.play_background_music() 

    def init_time_events(self):
        self.player_bullet_ready = pygame.USEREVENT + 0
        pygame.time.set_timer(self.player_bullet_ready, self.player.fire_rate)

        self.enemy_bullet_ready = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_bullet_ready, self.enemy.fire_rate)

        self.player_dash_ready = pygame.USEREVENT + 2
        pygame.time.set_timer(self.player_dash_ready, 0)

    def screen_update(self):
        for entity in self.entities.values():
            entity.update()
            entity.draw(self.screen)

            if not entity.alive():
                entity.name = 'to_be_deleted'

        self.handle_player()
        self.handle_enemies()
        self.handle_bullets()

        self.draw_ui()
        self.cleanup()

    def handle_player(self):
        # Dash handling
        if self.player.dashing:
            self.player.dash(self.dash_sound)
            self.player.current_dash_frames -= 1
        if self.player.current_dash_frames <= 0:
            self.player.set_intangible(False)
            self.player.dashing = False
            self.player.current_dash_frames = self.player.max_dash_frames

        # Hit detection
        for bullet in self.get_entities_from_name('enemy_bullet'):
            if self.player.hit(bullet) and not self.player.intangible:
                self.player.take_damage(25)
        
        # Hit frames handling
        if self.player.current_hit_frames > 0 and self.player.taken_damage:
            self.player.current_hit_frames -= 1
        if self.player.current_hit_frames <= 0:
            self.player.set_intangible(False)
            self.player.taken_damage = False
            self.player.current_hit_frames = self.player.max_hit_frames

        # Visual effects
        self.player.show_lifebars(self.screen)
        #self.player.show_hitbox(self.screen)

    def handle_enemies(self):
        for enemy in self.get_entities_from_name('enemy'):
                # Hit detection
                for bullet in self.get_entities_from_name('player_bullet'):
                    if enemy.hit(bullet) and not enemy.intangible:
                        enemy.take_damage(25)
                
                # Hit frames handling
                if enemy.current_hit_frames > 0 and enemy.taken_damage:
                    enemy.current_hit_frames -= 1
                if enemy.current_hit_frames <= 0:
                    enemy.set_intangible(False)
                    enemy.taken_damage = False
                    enemy.current_hit_frames = enemy.max_hit_frames

                # Visual effects
                enemy.show_lifebars(self.screen)
                #enemy.show_hitbox(self.screen)

    def handle_bullets(self):
        for entity in self.entities.values():
            if 'bullet' in entity.name:
                #entity.show_hitbox(self.screen)

                if entity.out_of_bounds():
                    entity.name = 'to_be_deleted'
     
    def draw_ui(self):
        self.draw_sound_icon()

    def draw_sound_icon(self):
        if not self.muted:
            self.screen.blit(self.images['unmuted_icon'], (WINDOW_SIZE[0] - 40, WINDOW_SIZE[1] - 40))
        else:
            self.screen.blit(self.images['muted_icon'], (WINDOW_SIZE[0] - 40, WINDOW_SIZE[1] - 40))

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

    def add_entity(self, entity):
        self.entities[entity.id] = entity

    def cleanup(self):
        for entity in self.entities.values():
            if entity.name == 'to_be_deleted':
                del self.entities[entity.id]
                break

    def get_entities_from_name(self, name):
        return [entity for entity in self.entities.values() if entity.name == name]