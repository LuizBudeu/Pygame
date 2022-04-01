# DECLARAÇÃO DE BIBLIOTECAS ---------------------------------------------- #
import pygame, sys 



# CONSTANTES ------------------------------------------------------------- #
WIDTH = 1000
HEIGHT = 800 
ROWS = 6
COLS = 7
HOLDER_SIZE = (1000, 620)
HOLES_POS = {(-20 + (j+1)*130): j for j in range(COLS)}
HOLES_POS_REV = {j: (-20 + (j+1)*130) for j in range(COLS)}



# INICIALIZAÇÕES --------------------------------------------------------- #
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))    
clock = pygame.time.Clock()



# CLASSES ---------------------------------------------------------------- #
class Holder:
    def draw(self):
        holder = pygame.Rect(0, 140, HOLDER_SIZE[0], HOLDER_SIZE[1])
        pygame.draw.rect(screen, (22, 112, 252), holder)


class Holes:
    def __init__(self):
        self.holesMatrix = [['0' for i in range(COLS)] for i in range(ROWS)]   # List comprehension pra fazer a matriz cheia de 0s

    def draw(self, red, yellow):
        for i in range(ROWS):
            for j in range(COLS):
                if self.holesMatrix[i][j] == '0':
                    pygame.draw.circle(screen, (250, 176, 114), (HOLES_POS_REV[j], 100 + (i+1)*100), 48)
                elif self.holesMatrix[i][j] == 'r':
                    pygame.draw.circle(screen, red, (HOLES_POS_REV[j], 100 + (i+1)*100), 48)
                else:
                    pygame.draw.circle(screen, yellow, (HOLES_POS_REV[j], 100 + (i+1)*100), 48)


class Main:
    def __init__(self):
        self.holder = Holder()
        self.holes = Holes()

        self.RED = (252, 43, 22)
        self.YELLOW = (234, 221, 13)

        self.reds_turn = True
        self.dropping = False

    def updateElements(self, pos):
        self.holder.draw()
        self.holes.draw(self.RED, self.YELLOW)
        self.movePieces(pos)
    
    def getPos(self, mouse_pos):
        mx, my = mouse_pos 
        for j in range(COLS):
            if HOLES_POS_REV[j] - 64 <= mx <= HOLES_POS_REV[j] + 64:
                mx = -20 + (j+1)*130

        return mx, 70

    def movePieces(self, pos):
        if self.reds_turn and not self.dropping:
            pygame.draw.circle(screen, self.RED, self.getPos(pos), 48)
        else:
            pygame.draw.circle(screen, self.YELLOW, self.getPos(pos), 48)

    def dropPiece(self, pos, color):
        j, _ = self.getPos(pos)
        j = HOLES_POS[j]

        for i in range(0, ROWS):
            if self.holes.holesMatrix[-(i+1)][j] == '0':
                if color == self.RED:
                    self.holes.holesMatrix[-(i+1)][j] = 'r'
                else:
                    self.holes.holesMatrix[-(i+1)][j] = 'y'
                break

        pygame.draw.circle(screen, color, pos, 48)
        self.dropping = False



# MAIN LOOP -------------------------------------------------------------- #
main = Main()
mx, my = 0, 0
while True:
    screen.fill((250, 176, 114))
    main.updateElements((mx, my))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if 0 <= my <= 140:
                    main.dropping = True
                    if main.reds_turn:
                        main.dropPiece((mx, my), main.RED)
                    else: 
                        main.dropPiece((mx, my), main.YELLOW)

                    main.reds_turn = not main.reds_turn
            

    pygame.display.update()
    clock.tick(60) 