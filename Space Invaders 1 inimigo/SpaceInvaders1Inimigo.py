import pygame
import random
from math import *
from pygame import mixer #Para colocar a música e os sons

#Para começar o pygame
pygame.init()

#Para criar a tela
screen = pygame.display.set_mode((800, 600)) #Esses dois valores são a largura e a altura da janela

#Título e ícone (geralmente o ícone é por volta de 32 pixels), arquivos no mesmo diretório
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space-invaders-logo.png")
pygame.display.set_icon(icon)

#Fundo de tela
background = pygame.image.load("space-invaders-background.png")

#Linha de chegada
lineImg = pygame.image.load("linha-de-chegada.png")

#Música
mixer.music.load("background-music.wav")
mixer.music.set_volume(0.2) #Volume da música, agora em 20%
mixer.music.play(-1) #Para tocar a música, esse '-1' significa para tocar em loop, se não tivesse nada a música tocaria só uma vez

#Imagem do jogador (nesse caso o tamanho é 64 pixels), arquivos no memso diretório
playerImg = pygame.image.load("space-invaders-ship.png")
playerX = 370 #Coordenada X da imagem do jogador no começo
playerY = 480 #Coordenada Y da imagem do jogador no começo
playerX_change = 0 #O valor da coordenada X que vai mudar quando uma tecla for apertada
#Não existe playerY_change porque nosso jogador não vai se mover na coordenada Y

#Imagem do inimigo (nesse caso o tamanho é 64 pixels), arquivos no memso diretório
enemyImg = pygame.image.load("space-invaders-alien.png")
enemyX = random.randint(0, 736) #Coordenada X da imagem do inimigo no começo
enemyY = random.randint(25, 75) #Coordenada Y da imagem do inimigo no começo
enemyY_change = 0.5 #O valor da coordenada Y do inimigo muda constantemente
enemyX_change = 1 #O valor da coordenada X do inimigo muda constantemente

#Imagem da bala (nesse caso o tamanho é 32 pixels), arquivos no mesmo diretório
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_ready = True #Se a bala estiver pronta para ser atirada (não tenha uma bala já voando)

#Placar do jogo, cada nave abatida é 1 ponto
score_value = 0
score_font = pygame.font.Font("freesansbold.ttf", 32) #Definindo qual fonte vai ser utilizada, também dá pra baixar outra fonte da internet, basta só colocar o arquivo no memso diretório
textX = 10 #Coordenada X do texto                                                                                                                      e ter certeza que a extensão é .ttf
textY = 10 #Coordenada Y do texto

#Para mostrar o placar
def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255)) #Esses últimos 3 valores são os RGB
    screen.blit(score, (x, y))

#Game over
game_over_font = pygame.font.Font("freesansbold.ttf", 80)

def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (150, 250))

def show_line():
    screen.blit(lineImg, (0, 480))

def player(x, y):
    screen.blit(playerImg, (x, y)) #Para desenhar o jogador

def enemy(x, y):
    screen.blit(enemyImg, (x, y)) #Para desenhar o inimigo

def bullet(x, y):
    global bullet_ready #Define "bullet_ready" como uma variável global que pode agora ser usada nessa função sem precisar dela como parâmetro
    bullet_ready = False
    screen.blit(bulletImg, (x+16, y+10)) #Para nascer a bala um pouco em cima da imagem do jogador

def isCollision(enemyX, enemyY, bulletX, bulletY): #Função que define colisão
    distance = sqrt((pow(enemyX-bulletX, 2)) + (pow(enemyY-bulletY, 2))) #Basicamente a fórmula da distância entre dois pontos
    if distance < 27:
        return True
    else:
        return False

#Game loop, só sai quando a janela é fechada
running = True #O jogo está ativo
while running:
    #Para definir a cor do plano de fundo da janela
    screen.fill((0, 0, 0))  #Esses 3 valores são os valores RGB, nesse caso preto

    #Para por o background
    screen.blit(background, (0, 0))

    # Para por a linha de chegada
    show_line()

    for event in pygame.event.get(): #Para todos os "eventos"
        if event.type == pygame.QUIT: #Se a janela é fechada, o jogo acabou
            running = False

        #Se uma tecla é apertada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #K_LEFT == flecha para esquerda
                playerX_change = -3 #Move o jogador 0.1 para a esquerda
            if event.key == pygame.K_RIGHT:  # K_RIGHT == flecha para direita
                playerX_change = 3 #Move o jogador 0.1 para a direita
            if event.key == pygame.K_SPACE: #K_SPACE == barra de espaço
                if bullet_ready: #Se não tiver nenhuma outra bala voando
                    bullet_sound = mixer.Sound("laser.wav")  # Definir o som de quando atirar uma bala
                    mixer.Sound.set_volume(bullet_sound, 0.2)  # Definir o volume do 'bullet_sound' para 20%
                    bullet_sound.play()  # Tocar o som
                    bulletX = playerX
                    bullet(bulletX, bulletY)  # Atira a bala da posição do jogador

        #Se uma tecla é solta
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0 #Para o jogador não continuar se movendo mesmo depois de ter soltado a tecla

    playerX += playerX_change #Atualiza a posição X do jogador (caso tenham sido apertadas as teclas correspondentes)

    #Para criar uma borda e não deixar que o jogador saisa da tela
    if playerX <= 0: #Pela esquerda
        playerX = 0
    elif playerX >= 736: #Pela esquerda
        playerX = 736

    # Para criar uma borda e fazer o inimigo quicar na parede
    enemyY += enemyY_change #Atualiza a posição Y do inimigo
    enemyX += enemyX_change #Atualiza a posição X do inimigo
    if enemyX <= 0: #Pela esquerda
        enemyX_change = 1
    if enemyX >= 736: #Pela esquerda
        enemyX_change = -1

    #Movimento da bala
    if bulletY <= -64: #Quando ela some no topo da tela outra bala pode ser atirada
        bulletY = 480
        bullet_ready = True
    if not bullet_ready: #Quando uma bala está voando
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Colisão
    if isCollision(enemyX, enemyY, bulletX, bulletY):
        explosion_sound = mixer.Sound("explosion.wav")  # Definir qual som vai tocar quando uma nave ser atingida
        mixer.Sound.set_volume(explosion_sound, 0.1)  # Definir o volume do 'explosion_sound' para 10%
        explosion_sound.play()  # Para tocar o som
        bulletY = 480  # Volta a bala pra posição 480
        bullet_ready = True  # Prepara a próxima bala
        score_value += 1  # Aumenta o placar
        enemyX = random.randint(0, 736)  # Respawna um novo inimigo
        enemyY = random.randint(25, 75)

    #Game over
    if enemyY > 430:
        enemyY = 2000
        show_game_over()
        break

    player(playerX, playerY) #Chama a função 'player'
    enemy(enemyX, enemyY)  # Chama a função 'enemy'
    show_score(textX, textY)
    pygame.display.update() #Sempre atualiza a tela