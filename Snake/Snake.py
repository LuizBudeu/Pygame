# BIBILIOTECAS
import pygame 
from pygame.math import Vector2
import sys
import random


# INICIALIZAÇÕES
pygame.init()
cell_size = 40
num_cells = 20
screen = pygame.display.set_mode((cell_size * num_cells, cell_size * num_cells))    # Assim criamos uma "grade" 800x800
clock  = pygame.time.Clock()



# CLASSES
class Fruit:
    def __init__(self):
        self.x = random.randint(0, num_cells - 1)
        self.y = random.randint(0, num_cells - 1)
        self.pos = Vector2(self.x, self.y)    # Para salvar a posição usaremos um vetor (não lista, mesmo sendo possível usar uma lista) porque é mais fácil de implementar operações sobre os valores. Essa é uma função do 'pygame.math' 

    def drawFruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)    # Utilizamos essa função para criar um retângulo diretamente, os parâmetros são: (x, y, width, height)
        pygame.draw.rect(screen, (255, 0, 0), fruit_rect)    # Para desenhar o retângulo usamos essa função, os parâmetros são: (surface, color, rect)


class Snake:
    def __init__(self):
        self.body = [Vector2(14, 10), Vector2(15, 10)]    # Vamos organizar a snake como uma lista de vetores de posições, em que o primeiro elemento vai ser a cabeça da snake
        self.direction = Vector2(-1, 0)    # Essa vai ser a direção inicial (para esquerda)
        self.new_block = False    # Vai nos ajudar quando tivermos que adicionar um block à snake

    def drawSnake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 191, 0), block_rect)

    def moveSnake(self):
        if self.new_block:
            body_copy = self.body[:]    # Essa linha copia o conteúdo de 'self.body'
            body_copy.insert(0, body_copy[0] + self.direction)    # Insere na primeira posição da lista a nova abeça
            self.body = body_copy[:]    # Copia a nova posição para 'self.body'
            self.new_block = False

        else:
            body_copy = self.body[:-1]    # Essa linha copia o conteúdo de 'self.body' menos o último elemento
            body_copy.insert(0, body_copy[0] + self.direction)    # Insere na primeira posição da lista a nova abeça
            self.body = body_copy[:]    # Copia a nova posição para 'self.body'

    def addBlock(self):
        self.new_block = True


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.moveSnake()
        self.checkCollision()
        self.checkDeath()

    def drawElements(self):
        self.fruit.drawFruit()
        self.snake.drawSnake()

    def checkCollision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit = Fruit()    # Cria nova fruta
            self.snake.addBlock()    # Adiciona um novo bloco à snake

    def checkDeath(self):
        if not 0 <= self.snake.body[0].x < num_cells or not 0 <= self.snake.body[0].y < num_cells:
            self.gameOver()

        for block in self.snake.body[1:]:    # Não incuindo a cabeça
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        pygame.quit()
        sys.exit()   # Sai da tela (e não dá erro)




# GAME VARIABLES
main_game = Main()

SCREEN_UPDATE = pygame.USEREVENT   # Vamos criar um timer para o movimento da snake
pygame.time.set_timer(SCREEN_UPDATE, 150)



# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()   # Sai da tela (e não dá erro)

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)


    # Desenha o background
    screen.fill((175, 215, 70))
    
    # Desenha os elementos
    main_game.drawElements()


    # Atualizações do loop
    pygame.display.update()
    clock.tick(60)

