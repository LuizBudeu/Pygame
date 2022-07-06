from recipes.combos import get_all_combos
import pygame

WINDOW_SIZE = (1440, 900)

LIGHTBLUE = (116, 247, 241)
WHITE = (255, 255, 255)
BROWN = (112, 46, 2)
REDDISHBROWN = (212, 54, 4)
SELECTEDREDDISHBROWN = (166, 42, 3)
GREENISH = (80, 189, 21)
SELECTEDGREENISH = (65, 156, 16)
DARKGRAY = (28, 28, 28)
GRAY = (214, 214, 212)
PURPLE = (158, 9, 232)
GREEN = (4, 249, 4)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 247, 0)
BLACK = (0, 0, 0)
ORANGE= (255, 166, 0)

def get_all_cards_stats():
    with open('cards/cards_stats.csv') as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        lines = lines[1:]
        l = []
        for s in lines:
            l.append(s.split(','))
        return {line[0]: {"level": line[1], "attack": line[2], "defense": line[3]} for line in l}

def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key
    return "key doesn't exist"

def get_mouse_pos():
    return pygame.mouse.get_pos()
    


all_cards_stats = get_all_cards_stats()
all_combos = get_all_combos()

player_1_default_cards_pos = {i: (80 + 260*(i), 620) for i in range(5)}
player_2_default_cards_pos = {i: (425 + 110*(i), -50) for i in range(5)}

