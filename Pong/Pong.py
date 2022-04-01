import pygame
from random import *
from math import *
from pygame import mixer
import time

#Para começar o pygame
pygame.init()

#Para criar a tela
screen = pygame.display.set_mode((1000, 600)) #Esses dois valores são a largura e a altura da janela

#Título e ícone (geralmente o ícone é por volta de 32 pixels), arquivos no mesmo diretório
pygame.display.set_caption("Pong")
icon = pygame.image.load("pong-icon.png")
pygame.display.set_icon(icon)

#Música
mixer.music.load("pong-music.wav")
mixer.music.set_volume(0.1) #Volume da música, agora em 10%
mixer.music.play(-1) #Para tocar a música, esse '-1' significa para tocar em loop, se não tivesse nada a música tocaria só uma vez

#Linha do meio
linha_do_meioImg = pygame.image.load("pong-linha-do-meio.png")

#Jogadores
jogadorImg = pygame.image.load("pong-jogador.png") #Os jogadores são retângulos brancos de 15x70 pixels

#Jogador da direita
jogador_direitaX = 950
jogador_direitaY = 265
jogador_direitaY_change = 0

#Jogador da esquerda
jogador_esquerdaX = 35
jogador_esquerdaY = 265
jogador_esquerdaY_change = 0

#Bola
bolaImg = pygame.image.load("pong-bola.png")
bolaX = randint(450, 550)
bolaY = randint(100, 500)
bolaX_change = uniform(0.15, 0.3) * pow(-1, randint(1, 2)) #Esse uniform(0.4, 0.6) pega um float aleatório entre esses números, incluindo eles
bolaY_change = uniform(0.15, 0.3) * pow(-1, randint(1, 2))
primeira_jogada = True

#Placares
placar_direita = 0
placar_esquerda = 0
placar_font = pygame.font.Font("freesansbold.ttf", 32)

#Para mostrar a linha do meio
def show_linha_do_meio():
    screen.blit(linha_do_meioImg, (490, 0))

#Para mostrar o jogador da direita
def jogador_direita(y):
    screen.blit(jogadorImg, (950, y))

#Para mostrar o jogador da esquerda
def jogador_esquerda(y):
    screen.blit(jogadorImg, (35, y))

#Para desenhar a bola
def bola(x, y):
    screen.blit(bolaImg, (x, y))

#Função que define colisão
def checa_colisao(bolaX, bolaY, jogador_direitaX, jogador_direitaY, jogador_esquerdaX, jogador_esquerdaY):
    #Essa condição checa a distância da bola com os jogadores e também com seus hitboxes (1º parte do 'and')
    if (abs(bolaX - jogador_direitaX) < 4 or abs(bolaX - jogador_esquerdaX) < 4) and (abs(bolaY-jogador_direitaY) < 70 or abs(bolaY-jogador_esquerdaY) < 70):
        #Para não contar os 70 pixels em cima do jogador
        if bolaY-jogador_direitaY >= 0 or bolaY-jogador_esquerdaY >= 0:
            global bolaX_change #Para mudar o valor de bolaX_change fora da função também
            bolaX_change *= -1.1

#Mostra o placar
def show_placar(placar_direita, placar_esquerda):
    show_placar_direita = placar_font.render(str(placar_direita), True, (255, 255, 255))
    show_placar_esquerda = placar_font.render(str(placar_esquerda), True, (255, 255, 255))
    screen.blit(show_placar_direita, (600, 20))
    screen.blit(show_placar_esquerda, (368, 20))

running = True #O jogo está ativo
while running:
    #Para definir a cor do plano de fundo da janela
    screen.fill((0, 0, 0))  #Esses 3 valores são os valores RGB, nesse caso preto

    for event in pygame.event.get(): #Para todos os "eventos"
        if event.type == pygame.QUIT: #Se a janela é fechada, o jogo acabou
            running = False

        #Se uma tecla é apertada
        if event.type == pygame.KEYDOWN:
            #Para o jogador da direita
            if event.key == pygame.K_UP: #K_UP == flecha para cima
                jogador_direitaY_change = -0.7
            if event.key == pygame.K_DOWN: #K_DOWN == flecha para baixo
                jogador_direitaY_change = 0.7

            #Para o jogador da esquerda
            if event.key == pygame.K_w: #K_w == tecla 'w'
                jogador_esquerdaY_change = -0.7
            if event.key == pygame.K_s: #K_s == tecla 's'
                jogador_esquerdaY_change = 0.7

        # Se uma tecla é solta
        if event.type == pygame.KEYUP:
            #Para o jogador da direita
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                jogador_direitaY_change = 0  # Para o jogador não continuar se movendo mesmo depois de ter soltado a tecla

            #Para o jogador da esquerda
            if event.key == pygame.K_w or event.key == pygame.K_s:
                jogador_esquerdaY_change = 0

    #Para mostrar a linha do meio
    show_linha_do_meio()

     #Atualiza as posições dos jogadores
    jogador_direitaY += jogador_direitaY_change
    jogador_esquerdaY += jogador_esquerdaY_change

    #Atualiza a posição da bola
    bolaX += bolaX_change
    bolaY += bolaY_change

    #Para não deixar os jogadores saírem da tela
    if jogador_direitaY <= 0:
        jogador_direitaY = 0
    elif jogador_direitaY >= 530:
        jogador_direitaY = 530

    if jogador_esquerdaY <= 0:
        jogador_esquerdaY = 0
    elif jogador_esquerdaY >= 530:
        jogador_esquerdaY = 530

    #Para não deixar a bola sair da tela por baixo ou por cima
    if bolaY >= 590:
        bolaY_change *= -1
    elif bolaY <= 0:
        bolaY_change *= -1

    #Caso a bola saia pela direita
    if bolaX >= 990:
        placar_esquerda += 1
        time.sleep(3)

        jogador_direitaX = 950
        jogador_direitaY = 265
        jogador_esquerdaX = 35
        jogador_esquerdaY = 265

        bolaX = randint(450, 550)
        bolaY = randint(100, 500)
        bolaX_change = uniform(0.15, 0.3) * pow(-1, randint(1, 2))
        bolaY_change = uniform(0.15, 0.3) * pow(-1, randint(1, 2))

    #Caso a bola saia pela esquerda
    if bolaX <= 0:
        placar_direita += 1
        time.sleep(3)

        jogador_direitaX = 950
        jogador_direitaY = 265
        jogador_esquerdaX = 35
        jogador_esquerdaY = 265

        bolaX = randint(450, 550)
        bolaY = randint(100, 500)
        bolaX_change = uniform(0.15, 0.3) * pow(-1, randint(1, 2))
        bolaY_change = uniform(0.15, 0.3) * pow(-1, randint(1, 2))

    checa_colisao(bolaX, bolaY, jogador_direitaX, jogador_direitaY, jogador_esquerdaX, jogador_esquerdaY)
    jogador_direita(jogador_direitaY) #Chama a função 'jogador_direita'
    jogador_esquerda(jogador_esquerdaY) #Chama a função 'jogador_esquerda'
    bola(bolaX, bolaY)
    show_placar(placar_direita, placar_esquerda)

    pygame.display.update()  # Sempre atualiza a tela