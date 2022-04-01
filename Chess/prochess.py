# DECLARAÇÃO DE BIBLIOTECAS
import pygame
import sys
from ChessEngine import *



# CONSTANTES GLOBAIS E INICIALIZAÇÕES
SQUARE_SIZE = 100
NUM_OF_SQUARES = 8
FILES_PATH = 'D:/User/VS Code testes/pythonzera/Pygame/Chess/Game files/'
IMAGES = {}

pygame.init()
screen = pygame.display.set_mode((SQUARE_SIZE * NUM_OF_SQUARES, SQUARE_SIZE * NUM_OF_SQUARES))    
clock = pygame.time.Clock()
pygame.display.set_caption("Chess")
icon = pygame.transform.scale(pygame.image.load(FILES_PATH + "wn.png"), (32, 32))
pygame.display.set_icon(icon)



# FUNÇÕES
def loadImages():
    pieces = ['br', 'bn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wq', 'wk', 'wp']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(FILES_PATH + piece + '.png'), (90, 90))


def drawGameSate(board):
    drawBoard()
    drawPieces(board)

def drawBoard():
    for i in range(NUM_OF_SQUARES):
        for j in range(NUM_OF_SQUARES):
            square_rect = pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            if (i + j + 1) % 2 == 0:
                pygame.draw.rect(screen, (0, 0, 0), square_rect)
            else:
                pygame.draw.rect(screen, (255, 255, 255), square_rect)


def drawPieces(board):
    for i in range(NUM_OF_SQUARES):
        for j in range(NUM_OF_SQUARES):
            piece_rect = pygame.Rect(i * SQUARE_SIZE + 5, j * SQUARE_SIZE + 5, SQUARE_SIZE, SQUARE_SIZE)
            piece = board[j][i]

            if piece != '--':
                screen.blit(IMAGES[piece], piece_rect)


def main():
    gs = GameState()
    loadImages()

    square_selected = ()
    player_clicks = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//SQUARE_SIZE   # Essas duas barras representam divisão inteira, 'int(location[0]/SQUARE_SIZE)'
                row = location[1]//SQUARE_SIZE

                if square_selected == (row, col):     # Se o player clicar no mesmo quadrado 2 vezes
                    square_selected = ()
                    player_clicks = []

                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)

                if len(player_clicks) == 2:    # Depois do segundo clique
                    move = Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    square_selected = ()
                    player_clicks = []



        drawGameSate(gs.board)

        pygame.display.update()
        clock.tick(60) 


# PADRÃO DO PYTHON (CHECA SE A MAIN É RODADA DESSE ARQUIVO)
if __name__ == '__main__':
    main()
