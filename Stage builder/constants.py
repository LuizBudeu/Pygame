import pygame

pygame.init()



WINDOWS_SIZE = (1440, 900)
LINE_X_POS = 200



LIGHTBLUE = (116, 247, 241)
WHITE = (255, 255, 255)
BROWN = (112, 46, 2)
REDDISHBROWN = (212, 54, 4)
SELECTEDREDDISHBROWN = (166, 42, 3)
GREENISH = (80, 189, 21)
SELECTEDGREENISH = (65, 156, 16)
DARKGRAY = (28, 28, 28)
PURPLE = (158, 9, 232)
GREEN = (4, 249, 4)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 247, 0)
BLACK = (0, 0, 0)
ORANGE= (255, 166, 0)


colorOptions = (BROWN, RED, GREEN, BLUE, YELLOW, PURPLE, BLACK, WHITE, ORANGE)
colorOptionsRects = []
for i, color in enumerate(colorOptions):
        if i < 3:
            colorOptionsRects.append(pygame.Rect(25 + i*55, 700, 40, 40))
        elif i < 6:
            colorOptionsRects.append(pygame.Rect(25 + (i-3)*55, 760, 40, 40))
        else:
            colorOptionsRects.append(pygame.Rect(25 + (i-6)*55, 820, 40, 40))












