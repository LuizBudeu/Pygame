import pygame
from constants import *



class GameEngine:
    def __init__(self, screen):
        self.squares = [[Square(i, j, (0, 0, 0)) for j in range(10)] for i in range(10)]
        self.boardMatrix = [['' for j in range(10)] for i in range(10)]
        self.screen = screen
        self.iniColors()

    def iniColors(self):
        for i in range(NUM_OF_SQUARES):
            for j in range(NUM_OF_SQUARES):
                if (i + j + 1) % 2 == 0:
                    self.squares[i][j].setColor((219, 219, 219))
                else:
                    self.squares[i][j].setColor((105, 105, 105))

    def drawBoard(self):
        for i in range(NUM_OF_SQUARES):
            for j in range(NUM_OF_SQUARES):
                if (i + j + 1) % 2 == 0:
                    pygame.draw.rect(self.screen, self.squares[i][j].color, self.squares[i][j].rect)
                else:
                    pygame.draw.rect(self.screen, self.squares[i][j].color, self.squares[i][j].rect)
                
    def highlightRange(self, range, paths):
        for path in paths:
            for p in path:
                if (p % NUM_OF_SQUARES != 0):
                    j = int(p % NUM_OF_SQUARES - 1)
                    i = int(p / NUM_OF_SQUARES)
                else:
                    j = int(NUM_OF_SQUARES - 1)
                    i = int(p / NUM_OF_SQUARES - 1)
                
                self.squares[i][j].select()

    

class Square:
    def __init__(self, i, j, color):
        self.rect = pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.color = color
        self.selected = False

    def setColor(self, newcolor):
        self.color = newcolor
        self.origColor = newcolor

    def select(self):
        if not self.selected:
            self.selected = True
            if self.origColor == (105, 105, 105):
                self.color = (205, 105, 105)
            else:
                self.color = (217, 156, 156)
        else:
            self.selected = False 
            self.color = self.origColor