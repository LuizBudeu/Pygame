# DECLARAÇÃO DE BIBLIOTECAS
import pygame
import sys
import os



# INICIALIZAÇÕES
pygame.init()
square_size = 100
num_of_squares = 8
screen = pygame.display.set_mode((square_size * num_of_squares, square_size * num_of_squares))    
clock = pygame.time.Clock()    # Cria um clock para ditar o framerate

files_path = 'D:/User/VS Code testes/pythonzera/Pygame/Chess/Game files/'
# Pra setar o ícone
pygame.display.set_caption("Chess")
icon_ = pygame.image.load(files_path + "wn.png")
icon = pygame.transform.scale(icon_, (32, 32))
pygame.display.set_icon(icon)



# CLASSES
class Board:
    def __init__(self):
        self.mboard = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'], 
            ['--', '--', '--', '--', '--', '--', '--', '--'], 
            ['--', '--', '--', '--', '--', '--', '--', '--'], 
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'], 
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]

    def draw(self):
        for i in range(num_of_squares):
            for j in range(num_of_squares):
                square_rect = pygame.Rect(i * square_size, j * square_size, square_size, square_size)
                if (i + j + 1) % 2 == 0:
                    pygame.draw.rect(screen, (0, 0, 0), square_rect)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), square_rect)


class Bishop:
    def __init__(self):
        pass


class BlackBishop(Bishop):
    def __init__(self):
        self.bb_surface = pygame.image.load(files_path + 'bb.png').convert_alpha()
        self.bb_c8_rect = self.bb_surface.get_rect(center = (2*square_size + square_size/2, square_size/2))
        self.bb_f8_rect = self.bb_surface.get_rect(center = (5*square_size + square_size/2, square_size/2))
        self.bb_list = [self.bb_c8_rect, self.bb_f8_rect]

    def draw(self):
        screen.blit(self.bb_surface, self.bb_c8_rect)
        screen.blit(self.bb_surface, self.bb_f8_rect)


class BlackKing:
    def __init__(self):
        self.bk_surface = pygame.image.load(files_path + 'bk.png').convert_alpha()
        self.bk_rect = self.bk_surface.get_rect(center = (4*square_size + square_size/2, square_size/2))

    def draw(self):
        screen.blit(self.bk_surface, self.bk_rect)


class BlackQueen:
    def __init__(self):
        self.bq_surface = pygame.image.load(files_path + 'bq.png').convert_alpha()
        self.bq_rect = self.bq_surface.get_rect(center = (3*square_size + square_size/2, square_size/2))

    def draw(self):
        screen.blit(self.bq_surface, self.bq_rect)


class BlackKnight:
    def __init__(self):
        self.bn_surface = pygame.image.load(files_path + 'bn.png').convert_alpha()
        self.bn_b8_rect = self.bn_surface.get_rect(center = (1*square_size + square_size/2, square_size/2))
        self.bn_g8_rect = self.bn_surface.get_rect(center = (6*square_size + square_size/2, square_size/2))
        self.bn_list = [self.bn_b8_rect, self.bn_g8_rect]

    def draw(self):
        screen.blit(self.bn_surface, self.bn_b8_rect)
        screen.blit(self.bn_surface, self.bn_g8_rect)


class BlackRook:
    def __init__(self):
        self.br_surface = pygame.image.load(files_path + 'br.png').convert_alpha()
        self.br_a8_rect = self.br_surface.get_rect(center = (square_size/2, square_size/2))
        self.br_h8_rect = self.br_surface.get_rect(center = (7*square_size + square_size/2, square_size/2))
        self.br_list = [self.br_a8_rect, self.br_h8_rect]

    def draw(self):
        screen.blit(self.br_surface, self.br_a8_rect)
        screen.blit(self.br_surface, self.br_h8_rect)


class BlackPawn:
    def __init__(self):
        self.bp_surface = pygame.image.load(files_path + 'bp.png').convert_alpha()
        self.bp_list = []
        for i in range(num_of_squares):
            self.bp_list.append(self.bp_surface.get_rect(center = (i*square_size + square_size/2, 3/2*square_size)))

    def draw(self):
        for bp in self.bp_list:
            screen.blit(self.bp_surface, bp)


class WhiteBishop(Bishop):
    def __init__(self):
        self.wb_surface = pygame.image.load(files_path + 'wb.png').convert_alpha()
        self.wb_c1_rect = self.wb_surface.get_rect(center = (2*square_size + square_size/2, 7*square_size + square_size/2))
        self.wb_f1_rect = self.wb_surface.get_rect(center = (5*square_size + square_size/2, 7*square_size + square_size/2))
        self.wb_list = [self.wb_c1_rect, self.wb_f1_rect]

    def draw(self):
        screen.blit(self.wb_surface, self.wb_c1_rect)
        screen.blit(self.wb_surface, self.wb_f1_rect)


class WhiteKing:
    def __init__(self):
        self.wk_surface = pygame.image.load(files_path + 'wk.png').convert_alpha()
        self.wk_rect = self.wk_surface.get_rect(center = (4*square_size + square_size/2, 7*square_size + square_size/2))

    def draw(self):
        screen.blit(self.wk_surface, self.wk_rect)


class WhiteQueen:
    def __init__(self):
        self.wq_surface = pygame.image.load(files_path + 'wq.png').convert_alpha()
        self.wq_rect = self.wq_surface.get_rect(center = (3*square_size + square_size/2, 7*square_size + square_size/2))

    def draw(self):
        screen.blit(self.wq_surface, self.wq_rect)


class WhiteKnight:
    def __init__(self):
        self.wn_surface = pygame.image.load(files_path + 'wn.png').convert_alpha()
        self.wn_b1_rect = self.wn_surface.get_rect(center = (1*square_size + square_size/2, 7*square_size + square_size/2))
        self.wn_g1_rect = self.wn_surface.get_rect(center = (6*square_size + square_size/2, 7*square_size + square_size/2))
        self.wn_list = [self.wn_b1_rect, self.wn_g1_rect]

    def draw(self):
        screen.blit(self.wn_surface, self.wn_b1_rect)
        screen.blit(self.wn_surface, self.wn_g1_rect)


class WhiteRook:
    def __init__(self):
        self.wr_surface = pygame.image.load(files_path + 'wr.png').convert_alpha()
        self.wr_a1_rect = self.wr_surface.get_rect(center = (square_size/2, 7*square_size + square_size/2))
        self.wr_h1_rect = self.wr_surface.get_rect(center = (7*square_size + square_size/2, 7*square_size + square_size/2))
        self.wr_list = [self.wr_a1_rect, self.wr_h1_rect]

    def draw(self):
        screen.blit(self.wr_surface, self.wr_a1_rect)
        screen.blit(self.wr_surface, self.wr_h1_rect)


class WhitePawn:
    def __init__(self):
        self.wp_surface = pygame.image.load(files_path + 'wp.png').convert_alpha()
        self.wp_list = []
        for i in range(num_of_squares):
            self.wp_list.append(self.wp_surface.get_rect(center = (i*square_size + square_size/2, 6*square_size + square_size/2)))

    def draw(self):
        for wp in self.wp_list:
            screen.blit(self.wp_surface, wp)





class Main:
    def __init__(self):
        self.dragging = False

        self.board = Board()
        self.bb = BlackBishop()
        self.bk = BlackKing()
        self.bq = BlackQueen()
        self.bn = BlackKnight()
        self.br = BlackRook()
        self.bp = BlackPawn()
        self.black_pieces_list = [
            self.bb.bb_c8_rect, self.bb.bb_f8_rect, self.bk.bk_rect, self.bq.bq_rect,
            self.bn.bn_b8_rect, self.bn.bn_g8_rect, self.br.br_a8_rect, self.br.br_h8_rect
        ]
        self.black_pieces_list.extend(self.bp.bp_list)
        self.wb = WhiteBishop()
        self.wk = WhiteKing()
        self.wq = WhiteQueen()
        self.wn = WhiteKnight()
        self.wr = WhiteRook()
        self.wp = WhitePawn()
        self.white_pieces_list = [
            self.wb.wb_c1_rect, self.wb.wb_f1_rect, self.wk.wk_rect, self.wq.wq_rect,
            self.wn.wn_b1_rect, self.wn.wn_g1_rect, self.wr.wr_a1_rect, self.wr.wr_h1_rect
        ]
        self.white_pieces_list.extend(self.wp.wp_list)

        self.pieces_list = self.black_pieces_list + self.white_pieces_list

    def drawPieces(self):
        self.board.draw()
        self.bb.draw()
        self.bk.draw()
        self.bq.draw()
        self.bn.draw()
        self.br.draw()
        self.bp.draw()
        self.wb.draw()
        self.wk.draw()
        self.wq.draw()
        self.wn.draw()
        self.wr.draw()
        self.wp.draw()

    def dragPiece(self, piece, pos):
        self.dragging = True
        piece.center = pos

    def dropPiece(self, piece, color, last_pos):
        self.dragging = False
        piece.centerx = int(piece.centerx/square_size) * square_size + square_size/2
        piece.centery = int(piece.centery/square_size) * square_size + square_size/2

        if color == 'black':
            self.black_pieces_list.remove(piece)
            for p in self.black_pieces_list:
                if int(piece.centerx/square_size) == int(p.centerx/square_size) and int(piece.centery/square_size) == int(p.centery/square_size):
                    piece.center = last_pos
            self.black_pieces_list.append(piece)

        elif color == 'white':
            self.white_pieces_list.remove(piece)
            for p in self.white_pieces_list:
                if int(piece.centerx/square_size) == int(p.centerx/square_size) and int(piece.centery/square_size) == int(p.centery/square_size):
                    piece.center = last_pos
            self.white_pieces_list.append(piece)

        """ ii = int(last_pos[0]/square_size)
        jj = int(last_pos[1]/square_size)

        self.board.mboard[ii][jj] = 0

        i = int(piece.centerx/square_size)
        j = int(piece.centery/square_size)

        if color == 'black':
            self.board.mboard[i][j] = -1
        elif color == 'white':
            self.board.mboard[i][j] = 1

        for r in range(8):
            for c in range(8):
                print(str(self.board.mboard[r][c]), end = ' ')
            print("\n") """ 




# MAIN LOOP
main = Main()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for piece in main.pieces_list:
                    if piece.collidepoint(event.pos) and not main.dragging:
                        last_pos = event.pos
                        if piece in main.black_pieces_list:
                            color = 'black'
                        else:
                            color = 'white'
                        main.dragPiece(piece, event.pos)
                        mov_piece = piece
                        

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                main.dropPiece(mov_piece, color, last_pos)           

        elif event.type == pygame.MOUSEMOTION:
            if main.dragging:
                main.dragPiece(mov_piece, event.pos)

    
    main.drawPieces()

    pygame.display.update()
    clock.tick(60) 
