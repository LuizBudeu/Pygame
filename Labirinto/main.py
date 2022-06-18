import pygame, sys, os, random, queue
from GameEngine import GameEngine
from constants import *

q = queue.Queue()

# INICIALIZAÇÕES
pygame.init()
screen = pygame.display.set_mode((SQUARE_SIZE * NUM_OF_SQUARES, SQUARE_SIZE * NUM_OF_SQUARES))    
clock = pygame.time.Clock()
pygame.display.set_caption("Labirinto")


""" board = [[j*(1+i) for j in range(NUM_OF_SQUARES)] for i in range(NUM_OF_SQUARES)]
squaresVisited = []
print(board) """

board= []
k = 0
for i in range(NUM_OF_SQUARES):
    b2 = []
    for j in range(NUM_OF_SQUARES):
        b2.append(k)
        k += 1
    board.append(b2)


""" def visited(pos):
    if pos in squaresVisited:
        return True
    return False

def solve(inix, iniy, endx, endy):
    steps = 5
    i = inix
    j = iniy
    q.put((inix, iniy))
    while steps != 0 and not q.empty():
        current = q.get()

        if (i, j) == (endx, endy):
            break

        if board[i+1][j] == 0 and not visited((i+1, j)):
            q.put((i+1, j))

        if board[i][j+1] == 0 and not visited((i, j+1)):
            q.put((i, j+1))

        if board[i-1][j] == 0 and not visited((i-1, j)):
            q.put((i-1, j))

        if board[i][j-1] == 0 and not visited((i+1, j-1)):
            q.put((i, j-1))

        squaresVisited.append((i, j)) """


def removeDuplicates(paths):
    for path in paths:
        setPath = set(path)
        if len(setPath) != len(path):
            paths.remove(path)


def findPaths(path, i, j):
    if len(path) > 3:
        #print(path+[board[i][j]])
        paths.append(path+[board[i][j]])
        return

    path.append(board[i][j])

    if 0 <= i+1 <= SQUARE_SIZE-1 and 0 <= j <= SQUARE_SIZE-1:
        findPaths(path, i+1, j)

    if 0 <= i <= SQUARE_SIZE-1 and 0 <= j+1 <= SQUARE_SIZE-1:
        findPaths(path, i, j+1)

    if 0 <= i-1 <= SQUARE_SIZE-1 and 0 <= j <= SQUARE_SIZE-1:
        findPaths(path, i-1, j)

    if 0 <= i <= SQUARE_SIZE-1 and 0 <= j-1 <= SQUARE_SIZE-1:
        findPaths(path, i, j-1)


    path.pop()


path = []
paths = []
findPaths(path, 0, 0)
removeDuplicates(paths)
print(paths)


ge = GameEngine(screen)
while True:

    ge.updateBoard()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            ge.selecting = True

        if event.type == pygame.MOUSEBUTTONUP:
            ge.selecting = False



    pygame.display.update()
    clock.tick(60) 