import pygame
import math
from constants import *
from funcs import *

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 20)




class Button:
    def __init__(self, screen, text, pos, color, tocolor):
        self.screen = screen
        self.text = text
        self.pos = pos
        self.color = color
        self.tocolor = tocolor

        self.rect = pygame.Rect(pos[0], pos[1], 160, 100)

    def draw(self):
        mx, my = getMousePos()
        if self.hoveringButton(mx, my):
            pygame.draw.rect(self.screen, self.tocolor, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)

        text_surface = font.render(self.text, True, DARKGRAY)
        text_rect = text_surface.get_rect(center = self.rect.center)
        self.screen.blit(text_surface, text_rect)

    
    def hoveringButton(self, mx, my):
        if self.rect.collidepoint(mx, my):
            return True
        
        return False



class Fighter:
    def __init__(self, screen, pos, role):
        self.screen = screen
        self.posx = pos[0]
        self.posy = pos[1]
        self.role = role
        self.alive = True

        if role == "ally":
            self.surf = pygame.image.load("imgs/ally.png").convert_alpha()
        elif role == "enemy":
            self.surf = pygame.image.load("imgs/enemy.png").convert_alpha()

        self.dead_surf = pygame.image.load("imgs/dead.png").convert_alpha()
        
        self.rect = self.surf.get_rect(topleft = pos)
        self.lifebar = Lifebar(screen, (self.rect.centerx, self.rect.top - 20))


    def draw(self):
        if self.alive:
            self.screen.blit(self.surf, self.rect)

        else:
            self.screen.blit(self.dead_surf, self.rect)
        
        self.lifebar.draw()

    def calculateDamage(self, ball):
        vel = math.sqrt(ball.velx**2 + ball.vely**2)
        self.takeDamage(round(vel/2))

    def takeDamage(self, damage):
        if self.lifebar.gwidth - damage >= 0:
            self.lifebar.gwidth -= damage
        else:
            self.lifebar.gwidth = 0
            self.alive = False
            



class Ball:
    def __init__(self, screen, velx, vely):
        self.screen = screen
        self.posx = LAUNCH_POINT[0]
        self.posy = LAUNCH_POINT[1]
        self.velx = velx
        self.vely = vely

        self.surf = pygame.image.load("imgs/ball.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (20, 20))
        self.rect = self.surf.get_rect()

    def draw(self, pos):
        self.rect.center = pos
        self.screen.blit(self.surf, self.rect)



class PowerMeter:
    def __init__(self, screen):
        self.screen = screen
        self.inner_width = 1
        self.changing = False

        self.x, self.y = 15, 830
        self.outerRect = pygame.Rect(self.x, self.y, 120, 50)

    def draw(self):
        self.innerRect = pygame.Rect(self.x+5, self.y+5, self.inner_width, 40)

        pygame.draw.rect(self.screen, BLACK, self.outerRect, 5)
        pygame.draw.rect(self.screen, GREEN, self.innerRect)

    def changeStrength(self):
        if self.inner_width >= 110:
            self.inner_width = 1
        
        else:
            self.inner_width += 1




class Lifebar:
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.gwidth = 50

        self.rrect = pygame.Rect(pos[0], pos[1], self.gwidth, 10)
        self.rrect.centerx = pos[0]

    def draw(self):
        self.grect = pygame.Rect(self.pos[0] - 25, self.pos[1], self.gwidth, 10)

        pygame.draw.rect(self.screen, RED, self.rrect)
        pygame.draw.rect(self.screen, GREEN, self.grect)

    
        

