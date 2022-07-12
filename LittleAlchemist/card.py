import pygame 
from settings import *
from ui_utils import *


class Card:
    def __init__(self, name, level, combo_type, attack, defense, tier, img):
        self.name = name
        self.level = int(level)
        self.combo_type = combo_type
        self.attack = int(attack)
        self.defense = int(defense)
        self.selected = False
        self.surf = img

        tiers_colors = [LIGHTBROWN, LIGHTGRAY, YELLOW]
        self.color = tiers_colors[int(tier)]

    def draw(self, screen, center_pos=(100, 100), topleft_pos=None, dim=(220, 270)):
        if topleft_pos:
            self.rect = pygame.Rect(topleft_pos, dim)
        else:
            topleft_pos = self.get_topleft_pos(center_pos, dim)
            self.rect = pygame.Rect(topleft_pos, dim)
        
        # Card
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)

        # Card drawing
        pygame.draw.rect(screen, WHITE, (topleft_pos[0]+5, topleft_pos[1]+35, 210, 205))
        pygame.draw.rect(screen, BLACK, (topleft_pos[0]+5, topleft_pos[1]+35, 210, 205), 1)
        screen.blit(self.surf, (topleft_pos[0]+5, topleft_pos[1]+35))

        # Card attack
        pygame.draw.rect(screen, ORANGE, (topleft_pos[0]+57, topleft_pos[1]+6, 70, 25))
        pygame.draw.rect(screen, BLACK, (topleft_pos[0]+57, topleft_pos[1]+6, 70, 25), 1)

        # Card defense
        pygame.draw.rect(screen, LIGHTBLUE, (topleft_pos[0]+130, topleft_pos[1]+6, 70, 25))
        pygame.draw.rect(screen, BLACK, (topleft_pos[0]+130, topleft_pos[1]+6, 70, 25), 1)

        # Card stats
        write_text(screen, text=self.name.upper(), font_size=19, center_pos=(topleft_pos[0]+110, topleft_pos[1]+255))
        write_text(screen, text=f"ATK: {self.attack}", font_size=16, center_pos=(topleft_pos[0]+90, topleft_pos[1]+20))
        write_text(screen, text=f"DEF: {self.defense}", font_size=16, center_pos=(topleft_pos[0]+165, topleft_pos[1]+20))
        write_text(screen, text=str(self.level), font_size=30, center_pos=(topleft_pos[0]+20, topleft_pos[1]+20))
        write_text(screen, text=self.combo_type, font_size=20, center_pos=(topleft_pos[0]+20, topleft_pos[1]+55))

    def hovering(self):
        mx, my = get_mouse_pos()
        if self.rect.collidepoint(mx, my):
            return True
        return False

    def get_center_pos(self, topleft, dim=(220, 270)):
        return (topleft[0]+dim[0]//2, topleft[1]+dim[1]//2)

    def get_topleft_pos(self, center_pos, dim=(220, 270)):
        return (center_pos[0]-dim[0]//2, center_pos[1]-dim[1]//2)

    