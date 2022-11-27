import pygame
import sys
from .common.settings import *
from .common.ui_utils import *
from .common.funcs import *
from .particle_manager import ParticleManager
from .particle_types import ParticleTypes


FPS = 20

class Game:
    def __init__(self):
        """Creates the Game object.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PixelSimulation")
    
    def game_loop(self):
        """Main game loop.
        """
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
                        self.grid = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
                        
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
        """Updates everything related to visuals of the screen.
        """
        if self.debug:
            self.draw_grid()
        
        self.check_dragging()
        self.particle_manager.handle_particles(self.screen)
        self.update_grid()
        print(len(self.particles))
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                write_text(self.screen, str(self.grid[i][j]), 20, (255, 255, 255), topleft_pos=(i*WINDOW_SIZE[0]//GRID_SIZE, j*WINDOW_SIZE[1]//GRID_SIZE))
        
    def update_grid(self):
        """Updates the grid matrix.
        """
        for particle in self.particles:
            # print(particle.i, particle.j)
            self.grid[particle.i][particle.j] = particle.type.value
            if not particle.stationary:
                self.grid[particle.previ][particle.prevj] = 0
            
    def update(self):
        """Updates the game every frame.
        """
        self.screen_update()
        self.frame_count += 1
        if self.frame_count >= FPS:
            self.frame_count = 0
        
    def init_game(self):
        """Initializes the game variables and objects.
        """
        self.debug = True
        self.grid = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        self.particles = []
        self.dragging = False
        self.particle_manager = ParticleManager(self.particles, self.grid)
        self.particle_selected = ParticleTypes.SAND
        self.frame_count = 0
        
    def check_dragging(self):
        """Checks if the user is dragging the mouse.
        """
        if self.dragging:
            mx, my = get_mouse_pos()
            i, j = pos_to_ij(mx, my)
            if self.grid[i][j] == 0:
                self.particle_manager.create_particle(self.particle_selected, i=i, j=j)
                self.grid[i][j] = self.particle_selected.value
        
    def start_game(self):
        """Starts the game (initialization and game loop).
        """
        self.init_game()
        self.game_loop()

    def draw_grid(self):
        """Draws the grid as lines and columns (n,m=GRID_SIZE).
        """
        for i in range(GRID_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (0, i*WINDOW_SIZE[0]//GRID_SIZE), (WINDOW_SIZE[0], i*WINDOW_SIZE[0]//GRID_SIZE), 1)
            pygame.draw.line(self.screen, (255, 255, 255), (i*WINDOW_SIZE[1]//GRID_SIZE, 0), (i*WINDOW_SIZE[1]//GRID_SIZE, WINDOW_SIZE[1]), 1)
    
    def draw_background(self):
        """Draws the background of the screen.
        """
        self.screen.fill((16, 20, 82))
        