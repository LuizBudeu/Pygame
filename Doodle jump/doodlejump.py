# DECLARAÇÃO DE BIBLIOTECAS
import pygame
import sys
import random



# INICIALIZAÇÕES
pygame.init()
screen = pygame.display.set_mode((532, 850))    
clock = pygame.time.Clock()    # Cria um clock para ditar o framerate
files_path = 'D:/User/VS Code testes/pythonzera/Pygame/Doodle jump/Game files/'
# Pra setar o ícone
pygame.display.set_caption("Doodle jump")
icon = pygame.image.load(files_path + "icon.png")
pygame.display.set_icon(icon)
score_font = pygame.font.Font("freesansbold.ttf", 50)



# CLASSES
class Platform:
    def __init__(self, tipo):
        self.tipo = tipo



# FUNÇÕES DO JOGO
def drawBackground():
    screen.blit(background_surface, (0, 0))

def drawDoodler():
    screen.blit(doodler_surface, doodler_rect)

def drawPlatfroms(colors):
    for index, platform in enumerate(platform_list):
        platform.centery += platform_velocity
        screen.blit(colors[index], platform)

        if platform.centery >= 950:
            platform_list.remove(platform)
            platform_list.append(colors[index].get_rect(center = (random.randint(70, 480), random.randint(-100, 0))))


def isCollision():
    for platform in platform_list:
        if abs(doodler_rect.centery - platform.centery) <= 45 and (doodler_rect.right - 10 >= platform.left and doodler_rect.left + 10 <= platform.right):
            return True
    return False

def checkGameOver():
    if doodler_rect.centery >= 890:
        return True
    return False

def showScore():
    score_surface = score_font.render('Score: ' + str(score), True, (128, 128, 0))
    score_rect = score_surface.get_rect(center = (266, 50))
    screen.blit(score_surface, score_rect)

def showGameOver():
    game_over_surface = score_font.render('Press R to play again', True, (128, 128, 0))
    game_over_surface_rect = game_over_surface.get_rect(center = (266, 200))
    screen.blit(game_over_surface, game_over_surface_rect)

    # Arquivo com os highscores
    highscores = open(files_path + "highscores.txt", "r")  # Primeiro lê o arquivo
    highscores_lista = highscores.readlines()  # Salva os valores de highscores em uma lista
    highscores.close()
    highscores = open(files_path + "highscores.txt", "a")
    if score > int(highscores_lista[-1]):  # Caso o score seja maior que o último ele adiciona o novo highscore
        highscores.write("\n" + str(score))
    highscores.close()

    highscore_surface = score_font.render("Highscore: " + str(highscores_lista[-1]), True, (128, 128, 0))
    highscore_surface_rect = highscore_surface.get_rect(center = (266, 300))
    screen.blit(highscore_surface, highscore_surface_rect)



# LOAD FILES
background_surface = pygame.image.load(files_path + 'background.png').convert()    # No VSCode tem que por o path absoluto, e esse 'convert()' faz com que o pygame haja mais rápido ao ler a imagem

big_doodler_surface = pygame.image.load(files_path + 'doodler.png').convert_alpha()
doodler_surface = pygame.transform.scale(big_doodler_surface, (95, 95))    # Só para diminuir um pouco a imagem original
doodler_rect = doodler_surface.get_rect(center = (266, 400))

raw_green_platform_surface = pygame.image.load(files_path + 'green-platform.png').convert_alpha()
green_platform_surface = pygame.transform.scale(raw_green_platform_surface, (130, 20))
gp = Platform(green_platform_surface)     # Classe 'Platform' do arquivo 'classes.py'
brown_platform_surface = pygame.image.load(files_path + 'brown-platform.png').convert_alpha()
bp = Platform(brown_platform_surface)
platform_list = []
platforms_colors_list = []
number_of_platforms = 11
for i in range(11):
    platform_list.append(gp.tipo.get_rect(center = (random.randint(70, 480), 850/number_of_platforms*i)))
    platforms_colors_list.append(gp.tipo)
""" platform_list.append(brown_platform_surface.get_rect(center = (random.randint(70, 480), 850/number_of_platforms*5)))
platforms_colors_list.append(bp.tipo)
for i in range(5):
    platform_list.append(gp.tipo.get_rect(center = (random.randint(70, 480), 850/number_of_platforms*(i+5))))
    platforms_colors_list.append(gp.tipo)
platform_list.append(brown_platform_surface.get_rect(center = (random.randint(70, 480), 850/number_of_platforms*11)))
platforms_colors_list.append(bp.tipo) """



# GAME VARIABLES
gravity = 0.1

doodler_y_velocity = 0
doodler_x_change = 0
facing_right = True
facing_left = False

platform_velocity = 0
platform_antigravity = 0.08

ready_to_jump = True
game_over = False
score = 0


# MAIN
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()   # Sai da tela (e não dá erro)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                doodler_x_change = -4
                if facing_right:
                    doodler_surface = pygame.transform.flip(doodler_surface, True, False)
                    facing_left = True
                    facing_right = False

            if event.key == pygame.K_RIGHT:
                doodler_x_change = 4
                if facing_left:
                    doodler_surface = pygame.transform.flip(doodler_surface, True, False)
                    facing_left = False
                    facing_right = True

            if event.key == pygame.K_r:
                game_over = False
                doodler_rect.center = (266, 400) 
                doodler_y_velocity = 0
                score = 0

        if event.type == pygame.KEYUP:
            doodler_x_change = 0


    # Desenha o background
    drawBackground()

    if not game_over:
        # Desenha o doodler
        doodler_y_velocity += gravity
        doodler_rect.centery += doodler_y_velocity
        doodler_rect.centerx += doodler_x_change

        # Para teleportar ao chegar no limite
        if doodler_rect.centerx <= 0:
            doodler_rect.centerx = 530
        if doodler_rect.centerx >= 531:
            doodler_rect.centerx = 0
        
        drawDoodler()
        if doodler_y_velocity >= 3:
            ready_to_jump = True


        # Desenha as plataformas 
        platform_velocity -= platform_antigravity
        if platform_velocity <= 0:
            platform_velocity = 0
        drawPlatfroms(platforms_colors_list)


        # Checa colisões
        if isCollision():
            if ready_to_jump:
                doodler_y_velocity = 0
                doodler_y_velocity -= 4

                platform_velocity = 6
                ready_to_jump = False
                score += 1

    else: 
        showGameOver()


    # Atualizações do loop
    game_over = checkGameOver()
    showScore()
    pygame.display.update()
    clock.tick(120)   # Determina o framerate como 120 fps no máximo (quer dizer que o framerate pode ser menor, mas como o que faremos é até que leve, o jogo rodará a 120 fps)