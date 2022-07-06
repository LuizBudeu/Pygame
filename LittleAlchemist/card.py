import pygame 
from settings import *
from ui_utils import *


class Card:
    def __init__(self, name, level, combo_type, attack, defense):
        self.name = name
        self.level = int(level)
        self.combo_type = combo_type
        self.attack = int(attack)
        self.defense = int(defense)
        self.selected = False

    def draw(self, screen, topleft_pos, dim=(220, 270), color=YELLOW):
        self.rect = pygame.Rect(topleft_pos, dim)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)

        write_text(screen, text=self.name.upper(), size=20, center_pos=(topleft_pos[0]+110, topleft_pos[1]+250))
        write_text(screen, text=f"ATK: {self.attack}", size=16, center_pos=(topleft_pos[0]+90, topleft_pos[1]+20))
        write_text(screen, text=f"DEF: {self.defense}", size=16, center_pos=(topleft_pos[0]+165, topleft_pos[1]+20))
        write_text(screen, text=str(self.level), size=30, center_pos=(topleft_pos[0]+20, topleft_pos[1]+20))
        write_text(screen, text=self.combo_type, size=20, center_pos=(topleft_pos[0]+20, topleft_pos[1]+60))

    def hovering(self, mx, my):
        if self.rect.collidepoint(mx, my):
            return True
        return False

    def get_center_pos(self, topleft, dim=(220, 270)):
        return (topleft[0]-dim[0]//2, topleft[1]-dim[1]//2)

    