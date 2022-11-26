import pygame
import sys
from .common.settings import *
from .common.ui_utils import *
from .particle_manager import ParticleManager
from .particle_types import ParticleTypes


FPS = 300

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PixelSimulation")
    
    def game_loop(self):
        while True:
            self.draw_background()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.dragging = True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.particles.clear()
                        
                    if event.key == pygame.K_1:
                        self.particle_selected = ParticleTypes.SAND
                        
                    if event.key == pygame.K_2:
                        self.particle_selected = ParticleTypes.WATER
                    
                    if event.key == pygame.K_3:
                        self.particle_selected = ParticleTypes.WOOD

            self.update()                    
                    
            pygame.display.update()
            self.clock.tick(FPS)
            
    def screen_update(self):
        if self.debug:
            self.draw_grid()
        
        self.check_dragging()
        self.particle_manager.handle_particles(self.screen)
    
    def check_dragging(self):
        if self.dragging:
            mx, my = get_mouse_pos()
            self.particle_manager.create_particle(mx, my, self.particle_selected)
            
    def init_game(self):
        self.debug = True
        self.grid = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        self.particles = []
        self.dragging = False
        self.particle_manager = ParticleManager(self.particles, self.grid)
        self.particle_selected = ParticleTypes.SAND
        
    def update(self):
        self.screen_update()
        
    def start_game(self):
        self.init_game()
        self.game_loop()

    def draw_grid(self):
        for i in range(GRID_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (0, i*WINDOW_SIZE[0]//GRID_SIZE), (WINDOW_SIZE[0], i*WINDOW_SIZE[0]//GRID_SIZE), 1)
            pygame.draw.line(self.screen, (255, 255, 255), (i*WINDOW_SIZE[1]//GRID_SIZE, 0), (i*WINDOW_SIZE[1]//GRID_SIZE, WINDOW_SIZE[1]), 1)
    
    def draw_background(self):
        self.screen.fill((16, 20, 82))
        