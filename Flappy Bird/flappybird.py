# DECLARAÇÃO DE BIBLIOTECAS
import pygame
import sys
import random



# INICILIAZAÇÕES
pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512)    # Para que o som não fique atrasado no momento da ação, usar essa pré incicialização do pygame.mixer
pygame.init()
screen = pygame.display.set_mode((288, 512))    # Cria a tela com 288 pixels de largura e 512 pixels de altura (as dimensões de um celular)
clock = pygame.time.Clock()    # Cria um clock para ditar o framerate
files_path = 'D:/User/VS Code testes/pythonzera/Pygame/Flappy Bird/Game files/'
# Pra setar o ícone
pygame.display.set_caption("Flappy bird")
icon = pygame.image.load(files_path + "icon.png")
pygame.display.set_icon(icon)
# Pra usar a fonte do Flappy bird
game_font = pygame.font.Font(files_path + '04B_19.ttf', 20)   # 20 é o tamanho da letra
game_over_font = pygame.font.Font(files_path + '04B_19.ttf', 40)



# FUNÇÕES DO JOGO
def drawBackground():
    screen.blit(background_surface, (0, 0))

def drawFloor():
    screen.blit(floor_surface, (floorX, 450))
    screen.blit(floor_surface, (floorX + 288, 450))

def drawBird():
    screen.blit(rotated_bird, bird_rect)

def createPipe():
    random_pipeY = random.choice(pipe_height)
    new_bottom_pipe = pipe_surface.get_rect(midtop = (350, random_pipeY))
    new_top_pipe = pipe_surface.get_rect(midbottom = (350, random_pipeY - 150))
    return new_bottom_pipe, new_top_pipe

def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:    # Assim sabemos que é um bottom_pipe
            screen.blit(pipe_surface, pipe)

        else:
            flipped_pipe = pygame.transform.flip(pipe_surface, False, True)    # Esses dois booleans são para flipar em direção do eixo X e do eixo Y, respectivamente
            screen.blit(flipped_pipe, pipe)

def checkCollision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):    # Função para checar se os retângulos de 'bird_rect' e 'pipe' estão colidindo, retorna True ou False
            death_sound.play()
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 470:
        death_sound.play()
        return False
    
    return True

def rotateBird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_velocity * -4, 1)    # Para rotacionar o bird, passamos o bird_surface, o ângulo de rotação (nesse caso podemos usar o sentido de bird_velocity) e a escala final da nova surface
    return new_bird

def birdAnimation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))   # Assim pegamos a posição Y do último bird_rect
    return new_bird, new_bird_rect

def scoreDisplay():
    score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (144, 50))
    screen.blit(score_surface, score_rect)

def showGameOver():
    game_over_surface = game_over_font.render("Game Over", True, (255, 255, 255))
    game_over_surface_rect = game_over_surface.get_rect(center = (144 , 150))
    screen.blit(game_over_surface, game_over_surface_rect)

    try_again_surface = game_font.render("Press UP to play again", True, (255, 255, 255))
    try_again_surface_rect = try_again_surface.get_rect(center = (144, 180))
    screen.blit(try_again_surface, try_again_surface_rect)


    # Arquivo com os highscores
    highscores = open(files_path + "highscores.txt", "r")  # Primeiro lê o arquivo
    highscores_lista = highscores.readlines()  # Salva os valores de highscores em uma lista
    highscores.close()
    highscores = open(files_path + "highscores.txt", "a")
    if score > int(highscores_lista[-1]):  # Caso o score seja maior que o último ele adiciona o novo highscore
        highscores.write("\n" + str(score))
    highscores.close()

    highscore_surface = game_font.render("Highscore: " + str(highscores_lista[-1]), True, (255, 255, 255))
    highscore_surface_rect = highscore_surface.get_rect(center = (144, 250))
    screen.blit(highscore_surface, highscore_surface_rect)

def showFirstTime():
    try_again_surface = game_font.render("Press UP to jump", True, (255, 255, 255))
    try_again_surface_rect = try_again_surface.get_rect(center = (144, 180))
    screen.blit(try_again_surface, try_again_surface_rect)



# LOAD FILES
background_surface = pygame.image.load(files_path + 'background.png').convert()    # No VSCode tem que por o path absoluto, e esse 'convert()' faz com que o pygame haja mais rápido ao ler a imagem

floor_surface = pygame.image.load(files_path + 'base.png').convert()

# Para fazer a animação do bird batendo as asas, salvamos cada frame em uma lista
bird_downflap = pygame.image.load(files_path + 'bird-downflap.png').convert_alpha()    # Esse 'convert_alpha()' faz com que quando rotacionamos a bird_surface, não apareça um retângulo preto em volta
bird_midflap = pygame.image.load(files_path + 'bird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load(files_path + 'bird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))   # Essa linha cria um retângulo (hitbox) do tamanho de 'bird' e com posição do centro do retângulo em (50, 256)

pipe_surface = pygame.image.load(files_path + 'pipe.png').convert()

flap_sound = pygame.mixer.Sound(files_path + 'sfx_wing.wav')
pygame.mixer.Sound.set_volume(flap_sound, 0.15)
death_sound = pygame.mixer.Sound(files_path + 'sfx_hit.wav')
pygame.mixer.Sound.set_volume(death_sound, 0.10)
score_sound = pygame.mixer.Sound(files_path + 'sfx_point.wav')
pygame.mixer.Sound.set_volume(score_sound, 0.10)


# Para redimensionar uma imagem se necessário, basta:
# background = pygame.transform.scale2x(background)    por exemplo, dobra a resolução de 'background'



# GAME VARIABLES
floorX = 0

gravity = 0.25
bird_velocity = 0
BIRDFLAP = pygame.USEREVENT + 1    # Esse +1 para criar um evento diferente do SPAWNPIPE
pygame.time.set_timer(BIRDFLAP, 200)

pipe_list = []
pipe_height = [200, 300, 400]   # Possíveis alturas dos pipes
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 800)   # Essas últimas duas linhas definem um novo tipo de evento, que basicamente vai spawnar novos pipes de acordo com um timer (o 800 é o tempo entre ativações do evento em milisegundos)

game_active = False
score2 = 0
score = int(score2/2)
first_time = True



# MAIN
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()   # Sai da tela (e não dá erro)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:   # Pulo
                bird_velocity = 0
                bird_velocity -= 6
                flap_sound.play()

            if event.key == pygame.K_UP and not game_active:
                game_active = True
                first_time = False
                score2 = 0
                score = 0
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_velocity = 0
                bird_velocity -= 6
                flap_sound.play()

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(createPipe())    # Tá 'extend' em vez de 'append' porque 'createPipe()' devolve um tuple

        if event.type == BIRDFLAP and game_active:
            if bird_index < 2:
                bird_index += 1

            else: 
                bird_index = 0

            bird_surface, bird_rect = birdAnimation()

    # Desenha o background
    drawBackground()

    # Desenha o chão
    floorX -= 1
    drawFloor()
    if floorX <= -288:
        floorX = 0

    # Player e pipes
    if game_active:

        # Desenha o player
        bird_velocity += gravity
        rotated_bird = rotateBird(bird_surface)    # Pra fazer a animação do bird rotacionando
        bird_rect.centery += bird_velocity   # 'centery' corresponde ao eixo Y que passa pelo centro do retângulo de 'bird_rect'
        drawBird()
        game_active = checkCollision(pipe_list)

        # Desenha os pipes
        pipe_list = movePipes(pipe_list)
        drawPipes(pipe_list)

    else:
        if first_time:
            showFirstTime()
        else:
            showGameOver()

    # Atualiza o score
    for pipe in pipe_list:
        if bird_rect.centerx == pipe.centerx:
            score2 += 1    # O score aumenta em 2 se fizer 'score += 1'
            score = int(score2/2)
            score_sound.play()

    # Atualizações do loop
    scoreDisplay()
    pygame.display.update()
    clock.tick(120)   # Determina o framerate como 120 fps no máximo (quer dizer que o framerate pode ser menor, mas como o que faremos é até que leve, o jogo rodará a 120 fps)

