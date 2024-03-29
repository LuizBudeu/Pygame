import pygame
import sys
import random
from pygame import mixer
from .common.settings import *
from .common.ui_utils import *
from .player import Player
from .enemy import Enemy
from .item import Item
from .world_map import world_map
from .common.camera import Camera


class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-
                              16, channels=2, buffer=512)
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Bullet Hell")
        pygame.display.set_icon(pygame.image.load(
            'assets/images/item_increase_fire_rate_icon.png'))

        self.init_game()
        self.game_loop()

    def game_loop(self):
        while True:
            self.screen.fill(NIGHTBLUE)

            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Movement events
                    if self.player.controls_enabled:
                        if event.key == pygame.K_a:
                            self.player.velx += -self.player.vel_mod
                        if event.key == pygame.K_d:
                            self.player.velx += self.player.vel_mod
                        if event.key == pygame.K_w:
                            self.player.vely += -self.player.vel_mod
                        if event.key == pygame.K_s:
                            self.player.vely += self.player.vel_mod

                    # Mute/unmute event
                    if event.key == pygame.K_m:
                        if not self.muted:
                            self.mute_all_sounds()
                            self.muted = True
                        else:
                            self.unmute_all_sounds()
                            self.muted = False

                    # Restart event
                    if event.key == pygame.K_r:
                        self.init_game()

                    # Quit event
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

                    # God mode event
                    if event.key == pygame.K_g:
                        self.player.set_intangible(not self.player.intangible)

                    # Dash event
                    if event.key == pygame.K_SPACE:
                        if self.player.can_dash and self.player.controls_enabled:
                            self.player.dashing = True
                            self.player.can_dash = False
                            pygame.time.set_timer(
                                self.player_dash_ready, self.player.dash_cooldown)

                if event.type == pygame.KEYUP:
                    # Movement events
                    if self.player.controls_enabled:
                        if event.key == pygame.K_a:
                            self.player.velx -= -self.player.vel_mod
                        if event.key == pygame.K_d:
                            self.player.velx -= self.player.vel_mod
                        if event.key == pygame.K_w:
                            self.player.vely -= -self.player.vel_mod
                        if event.key == pygame.K_s:
                            self.player.vely -= self.player.vel_mod

                # Player bullet ready event
                if event.type == self.player_bullet_ready:
                    self.player.shoot(
                        self.entities, self.sounds['bullet']['sound'])

                # Enemy bullet ready event
                if event.type == self.enemy_bullet_ready:
                    for enemy in self.get_entities_from_name("enemy"):
                        enemy.shoot(self.entities, self.player)

                # Player dash ready event
                if event.type == self.player_dash_ready:
                    self.player.can_dash = True
                    pygame.time.set_timer(self.player_dash_ready, 0)

            self.screen_update()

            pygame.display.update()
            self.clock.tick(120)

    def init_game(self):
        self.load_sounds()
        self.load_images()

        self.entities = {}
        self.create_player()
        self.create_enemies()
        self.create_items()
        self.create_camera()
        
        # self.create_world_map()  

        self.muted = False
        self.play_background_music()
        self.init_time_events()

    def init_time_events(self):
        self.player_bullet_ready = pygame.USEREVENT + 0
        pygame.time.set_timer(self.player_bullet_ready, self.player.fire_rate)

        self.enemy_bullet_ready = pygame.USEREVENT + 1

        pygame.time.set_timer(self.enemy_bullet_ready, 250)

        self.player_dash_ready = pygame.USEREVENT + 2
        pygame.time.set_timer(self.player_dash_ready, 0)

    def screen_update(self):
        self.handle_player()
        self.handle_enemies()
        self.handle_bullets()
        self.handle_items()

        for entity in self.entities.values():
            self.camera.update(entity)
            entity.update()
            entity.draw(self.screen)

        self.draw_ui()
        self.cleanup()

    def handle_player(self):
        # Out of bounds handling
        self.player.limit_out_of_bounds()

        # Dash handling
        if self.player.dashing:
            self.player.dash(self.sounds['dash']['sound'])
            self.player.current_dash_frames -= 1
            draw_fading_rect(self.screen, self.player.rect.x, self.player.rect.y, self.player.rect.width,
                             self.player.rect.height, BLUE, self.player.current_dash_frames - self.player.max_dash_frames)
        if self.player.current_dash_frames <= 0:
            self.player.set_intangible(False)
            self.player.dashing = False
            self.player.current_dash_frames = self.player.max_dash_frames

        # Hit detection
        for bullet in self.get_entities_from_name('enemy_bullet'):
            if self.player.hit(bullet) and not self.player.intangible:
                self.player.take_damage(
                    25, self.sounds['player_hit']['sound'], self.sounds['explosion']['sound'])

        # Hit frames handling
        if self.player.current_hit_frames > 0 and self.player.taken_damage:
            self.player.current_hit_frames -= 1
        if self.player.current_hit_frames <= 0:
            self.player.set_intangible(False)
            self.player.taken_damage = False
            self.player.current_hit_frames = self.player.max_hit_frames

        # Visual effects
        self.player.show_lifebars(self.screen)

    def handle_enemies(self):
        for enemy in self.get_entities_from_name('enemy'):

            # Hit detection
            for bullet in self.get_entities_from_name('player_bullet'):
                if enemy.hit(bullet) and not enemy.intangible:
                    enemy.take_damage(
                        25, self.sounds['enemy_hit']['sound'], self.sounds['explosion']['sound'])

            # Hit frames handling
            if enemy.current_hit_frames > 0 and enemy.taken_damage:
                enemy.current_hit_frames -= 1
            if enemy.current_hit_frames <= 0:
                enemy.set_intangible(False)
                enemy.taken_damage = False
                enemy.current_hit_frames = enemy.max_hit_frames

            # Visual effects
            enemy.show_lifebars(self.screen)
            enemy.show_range(self.screen)

    def handle_bullets(self):
        for bullet in self.get_entities_like_name('bullet'):
            """ if bullet.distance_traveled() >= bullet.max_distance: """
            if bullet.out_of_bounds():
                bullet.name = 'to_be_deleted'

    def handle_items(self):
        for item in self.get_entities_like_name('item'):
            if self.player.hit(item.rect):
                item.apply_effect(self.player)
                pygame.time.set_timer(
                    self.player_bullet_ready, self.player.fire_rate)  # TODO temp
                mixer.Sound.set_volume(
                    self.sounds['bullet']['sound'], self.sounds['bullet']['volume']-0.01)
                item.name = 'to_be_deleted'

    def draw_ui(self):
        self.draw_sound_icon()

    def draw_sound_icon(self):
        if not self.muted:
            self.screen.blit(
                self.images['unmuted_icon'], (WINDOW_SIZE[0] - 40, WINDOW_SIZE[1] - 40))
        else:
            self.screen.blit(
                self.images['muted_icon'], (WINDOW_SIZE[0] - 40, WINDOW_SIZE[1] - 40))

    def load_images(self):
        unmuted_icon_surf = pygame.image.load(
            "assets/images/unmuted_icon.png").convert_alpha()
        muted_icon_surf = pygame.image.load(
            "assets/images/muted_icon.png").convert_alpha()
        increase_fire_rate_icon_surf = pygame.image.load(
            "assets/images/item_increase_fire_rate_icon.png").convert_alpha()

        self.images = {
            'unmuted_icon': unmuted_icon_surf,
            'muted_icon': muted_icon_surf,
            'items': {
                'increase_fire_rate': increase_fire_rate_icon_surf
            }
        }

    def load_sounds(self):
        # Background music
        mixer.music.load(
            f"assets/sound/music/gameloop{random.randint(1, 3)}.ogg")
        mixer.music.set_volume(0.2)

        # Sound effects
        bullet_sound = mixer.Sound("assets/sound/effects/laser.wav")
        dash_sound = mixer.Sound("assets/sound/effects/dash.wav")
        player_hit_sound = mixer.Sound("assets/sound/effects/player_hit.wav")
        enemy_hit_sound = mixer.Sound("assets/sound/effects/enemy_hit.wav")
        explosion_sound = mixer.Sound("assets/sound/effects/explosion.wav")

        self.sounds = {
            "bullet": {'sound': bullet_sound, 'volume': 0.03},
            "dash": {'sound': dash_sound, 'volume': 0.07},
            "player_hit": {'sound': player_hit_sound, 'volume': 0.1},
            "enemy_hit": {'sound': enemy_hit_sound, 'volume': 0.07},
            "explosion": {'sound': explosion_sound, 'volume': 0.05}
        }

        for sound in self.sounds:
            mixer.Sound.set_volume(
                self.sounds[sound]['sound'], self.sounds[sound]['volume'])

    def play_background_music(self):
        mixer.music.play(-1)

    def mute_all_sounds(self):
        mixer.music.set_volume(0)
        for sound in self.sounds:
            mixer.Sound.set_volume(self.sounds[sound]['sound'], 0)

    def unmute_all_sounds(self):
        mixer.music.set_volume(0.2)
        for sound in self.sounds:
            mixer.Sound.set_volume(
                self.sounds[sound]['sound'], self.sounds[sound]['volume'])

    def add_entity(self, entity):
        self.entities[entity.id] = entity

    def cleanup(self):
        for entity in self.entities.values():
            if entity.name == 'to_be_deleted':
                del self.entities[entity.id]
                break

    def get_entities_from_name(self, name):
        return [entity for entity in self.entities.values() if entity.name == name]

    def get_entities_like_name(self, name):
        return [entity for entity in self.entities.values() if name in entity.name]

    def create_player(self):
        self.player = Player(0, 0, 32, 32, YELLOW, 'player', max_health=100)
        self.player.set_center_position((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))
        self.add_entity(self.player)

    def create_enemies(self):
        number_of_enemies = 3
        enemies = [Enemy(0, 0, 32, 32, RED, 'enemy', max_health=100)
                   for i in range(number_of_enemies)]

        for i, enemy in enumerate(enemies):
            enemy.set_center_position(
                (WINDOW_SIZE[0]/(number_of_enemies+1)*(i+1), WINDOW_SIZE[1]/2 - 300))
            self.add_entity(enemy)

    def create_items(self):
        item_increased_fire_rate = Item(
            0, 0, 1, 1, None, 'item_increase_fire_rate', self.images['items']['increase_fire_rate'])
        item_increased_fire_rate.set_center_position(
            (WINDOW_SIZE[0]/9, WINDOW_SIZE[1]*0.8))
        self.add_entity(item_increased_fire_rate)

    def create_camera(self):
        self.camera = Camera(self.screen)
        self.camera.set_center_target(self.player)

    def create_world_map(self):
        self.world_map = world_map
        
        for i, row in enumerate(world_map):
            for j, col in enumerate(row):
                pass # TODO
