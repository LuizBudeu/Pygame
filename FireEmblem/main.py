# MODULES
import pygame, sys, os, random
from constants import *
from GameEngine import GameEngine
from Piece import Piece



# OBJETOS GLOBAIS
IJ_TO_POS = {(j, i): (i*SQUARE_SIZE, j*SQUARE_SIZE) for j in range(NUM_OF_SQUARES) for i in range(NUM_OF_SQUARES)}
POS_TO_IJ = {v: k for k, v in IJ_TO_POS.items()}



# INICIALIZAÇÕES
pygame.init()
screen = pygame.display.set_mode((SQUARE_SIZE * NUM_OF_SQUARES, SQUARE_SIZE * NUM_OF_SQUARES))    
clock = pygame.time.Clock()
pygame.display.set_caption("Fire Emblem")
icon = pygame.transform.scale(pygame.image.load('assets/black_sword.PNG'), (32, 32))
pygame.display.set_icon(icon)


# FUNÇÕES
def screenUpdate(ge, pieces):
    ge.drawBoard()
    for piece in pieces:
        piece.draw()

# CLASSES

board= []
k = 0
for i in range(NUM_OF_SQUARES):
    b2 = []
    for j in range(NUM_OF_SQUARES):
        b2.append(k)
        k += 1
    board.append(b2)

def removeDuplicates(paths):
    for path in paths:
        setPath = set(path)
        if len(setPath) != len(path):
            paths.remove(path)


def findPaths(path, i, j, movingRange):
    if 0 <= i <= SQUARE_SIZE-1 and 0 <= j <= SQUARE_SIZE-1:
        if len(path) > movingRange:
            paths.append(path+[board[i][j]])
            return

        path.append(board[i][j])
        print(i, j)

        if 0 <= i+1 <= SQUARE_SIZE-1 and 0 <= j <= SQUARE_SIZE-1:
            findPaths(path, i+1, j, movingRange)

        if 0 <= i <= SQUARE_SIZE-1 and 0 <= j+1 <= SQUARE_SIZE-1:
            findPaths(path, i, j+1, movingRange)

        if 0 <= i-1 <= SQUARE_SIZE-1 and 0 <= j <= SQUARE_SIZE-1:
            findPaths(path, i-1, j, movingRange)

        if 0 <= i <= SQUARE_SIZE-1 and 0 <= j-1 <= SQUARE_SIZE-1:
            findPaths(path, i, j-1, movingRange)

        path.pop()


path = []
paths = []
#findPaths(path, 0, 0)
#removeDuplicates(paths)
#print(paths)
movingRange = 3


# MAIN LOOP
ge = GameEngine(screen)
sword = Piece(screen, 'sword', IJ_TO_POS[(5, 5)], 'red')
spear = Piece(screen, 'spear', IJ_TO_POS[(0, 1)], 'blue')
axe = Piece(screen, 'axe', IJ_TO_POS[(3, 2)])

pieces = []
pieces.append(sword)
pieces.append(spear)
pieces.append(axe)
while True:
    screenUpdate(ge, pieces)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                mx, my = pygame.mouse.get_pos()
                i = mx//SQUARE_SIZE
                j = my//SQUARE_SIZE
                #ge.squares[i][j].select()
                findPaths(path, i, j, movingRange)
                removeDuplicates(paths)
                #print(paths)
                ge.highlightRange(movingRange, paths)


    pygame.display.update()
    clock.tick(60) 