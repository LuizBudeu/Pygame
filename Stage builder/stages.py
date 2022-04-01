import pygame
from constants import *

pygame.init()

Stage1 = {
    "STAGE_SIZE": (WINDOWS_SIZE[0] - LINE_X_POS, WINDOWS_SIZE[1]),
    "NUM_OF_RECTS": 4,
    "Rects": [pygame.Rect(400, 500, 500, 100), pygame.Rect(700, 700, 500, 100),
              pygame.Rect(300, 100, 200, 100), pygame.Rect(900, 300, 100, 200)],
    "Colors": [BROWN, BROWN, PURPLE, PURPLE]
}





