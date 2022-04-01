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
class Doodler:
    def __init__(self):
        self.gravity = 0.15
        self.y_vel = 0
        self.x_change = 0
        self.facing_right = True
        self.facing_left = False
        self.ready_to_jump = True

        big_doodler_surface = pygame.image.load(files_path + 'doodler.png').convert_alpha()
        self.doodler_surface = pygame.transform.scale(big_doodler_surface, (95, 95))    # Só para diminuir um pouco a imagem original
        self.rect = self.doodler_surface.get_rect(center = (266, 400))

    def drawDoodler(self):
        screen.blit(self.doodler_surface, self.rect)

    def doodlerMovement(self):
        self.y_vel += self.gravity
        self.rect.centery += self.y_vel
        self.rect.centerx += self.x_change
        self.drawDoodler()

        if self.rect.centerx <= 0:
            self.rect.centerx = 530
        if self.rect.centerx >= 531:
            self.rect.centerx = 0

        if self.y_vel >= 1:
            self.ready_to_jump = True

    def moveDoodlerLeft(self):
        self.x_change = -4

        if self.facing_right:
            self.doodler_surface = pygame.transform.flip(self.doodler_surface, True, False)
            self.facing_left = True
            self.facing_right = False 

    def moveDoodlerRight(self):
        self.x_change = 4

        if self.facing_left:
            self.doodler_surface = pygame.transform.flip(self.doodler_surface, True, False)
            self.facing_left = False
            self.facing_right = True
    
    def jump(self):
        self.y_vel = 0
        self.y_vel -= 4
        self.ready_to_jump = False
    
    def bigJump(self):
        self.y_vel = 0
        self.y_vel -= 8
        self.ready_to_jump = False


class Platform:
    def __init__(self, number_of_platforms):
        self.platform_list = []
        self.platforms_colors_list = []

        self.vel = 0
        self.platform_antigravity = 0.1

        green_platform_surface = pygame.image.load(files_path + 'green-platform.png').convert_alpha()
        self.gps = pygame.transform.scale(green_platform_surface, (130, 20))
        self.g_chance = 80

        self.bps = pygame.image.load(files_path + 'brown-platform.png').convert_alpha()
        self.broken_bps = pygame.image.load(files_path + 'broken-brown-platform.png').convert_alpha()
        self.b_chance = 20

        self.startPlatforms(number_of_platforms)

    def startPlatforms(self, number_of_platforms):
        for i in range(number_of_platforms):
            rchoice = random.randint(0, 100)
            if rchoice > 10:
                self.platform_list.append(self.gps.get_rect(center = (random.randint(70, 480), 850/number_of_platforms*i)))
                self.platforms_colors_list.append('green')
            else:
                self.platform_list.append(self.bps.get_rect(center = (random.randint(70, 480), 850/number_of_platforms*(i))))
                self.platforms_colors_list.append('brown')

    def drawPlatforms(self, colors):
        for index, plat in enumerate(self.platform_list):
            if colors[index] == 'green':
                screen.blit(self.gps, plat)
            elif colors[index] == 'brown':
                screen.blit(self.bps, plat)
            elif colors[index] == 'broken brown':
                screen.blit(self.broken_bps, plat)

            if plat.centery >= 900:
                self.newPlatform(plat, index)

    def newPlatform(self, plat, index):
        plat.center = (random.randint(70, 480), -50)
        rchoice = random.randint(0, 100)
        if rchoice > 20:
            self.platforms_colors_list[index] = 'green'
        else:
            self.platforms_colors_list[index] = 'brown'

    def platformsMovement(self):
        self.vel -= self.platform_antigravity
        if self.vel <= 0:
            self.vel = 0

        for platform in self.platform_list:
            platform.centery += self.vel

        self.drawPlatforms(self.platforms_colors_list)

    def movePlatformsDown(self):
        self.vel = 6

    def platformBreak(self, plat, index):
        self.platform_list[index] = self.broken_bps.get_rect(center = (plat.centerx, plat.centery + 15))
        self.platforms_colors_list[index] = 'broken brown'

    def topPlatform(self):
        for plat in self.platform_list:
            if plat.centery < 200:
                return plat


class Spring:
    def __init__(self):
        self.spawned = False

        self.spring_surface = pygame.image.load(files_path + 'spring.png').convert_alpha()
        self.rect = self.spring_surface.get_rect(center = (0, 0))

    def drawSpring(self):
        screen.blit(self.spring_surface, self.rect)

    def spawnSpring(self, posx, posy):
        self.rect = self.spring_surface.get_rect(center = (posx, posy))
        self.spawned = True

    def moveSpring(self, posx, posy, plat):
        if abs(self.rect.bottom - plat.top) <= 10:
            self.rect = self.spring_surface.get_rect(center = (posx, posy))
        else:
            self.rect = self.spring_surface.get_rect(center = (posx, posy + 10))

        self.drawSpring()


class Main:
    def __init__(self):
        self.background_surface = pygame.image.load(files_path + 'background.png').convert()
        self.doodler = Doodler()
        self.platform = Platform(10)
        self.spring = Spring()
        self.score = 0
        self.game_over = False

    def update(self):
        self.drawBackground()
        self.showScore()
        self.game_over = self.checkGameOver()
        if not self.game_over:
            self.doodler.doodlerMovement()
            self.platform.platformsMovement()
            if not self.spring.spawned:
                self.top_platform_at_time = self.platform.topPlatform()
            if self.platform.platforms_colors_list[self.platform.platform_list.index(self.top_platform_at_time)] != 'brown':
                if not self.spring.spawned:
                    self.spring.spawnSpring(self.top_platform_at_time.centerx, self.top_platform_at_time.centery - 30)
                else: 
                    self.spring.moveSpring(self.top_platform_at_time.centerx, self.top_platform_at_time.centery - 30, self.top_platform_at_time)
                    if self.top_platform_at_time.centery - 30 >= 850:
                        self.spring.spawned = False

            if self.hitSpring():
                if self.doodler.ready_to_jump:
                    self.doodler.bigJump()
                    self.platform.movePlatformsDown()
                    self.score += 1

            elif self.hitPlatform():
                if self.doodler.ready_to_jump:
                    self.doodler.jump()
                    self.platform.movePlatformsDown()
                    self.score += 1

        else:
            self.showGameOver()
            self.platform.platform_list.clear()
            self.platform.platforms_colors_list.clear()

    def drawBackground(self):
        screen.blit(self.background_surface, (0, 0))

    def hitPlatform(self):
        for index, plat in enumerate(self.platform.platform_list):
            if abs(self.doodler.rect.bottom - plat.top) <= 3 and (self.doodler.rect.right - 10 >= plat.left and self.doodler.rect.left + 10 <= plat.right) and self.platform.platforms_colors_list[index] != 'broken brown':
                if self.doodler.ready_to_jump and self.platform.platforms_colors_list[self.platform.platform_list.index(plat)] == 'brown':
                    self.platform.platformBreak(plat, self.platform.platform_list.index(plat))

                return True
        return False

    def hitSpring(self):
        if abs(self.doodler.rect.bottom - self.spring.rect.top) <= 3 and (self.doodler.rect.right - 10 >= self.spring.rect.left and self.doodler.rect.left + 10 <= self.spring.rect.right):
            return True
        return False

    def showScore(self):
        score_surface = score_font.render('Score: ' + str(self.score), True, (128, 128, 0))
        score_rect = score_surface.get_rect(center = (266, 50))
        screen.blit(score_surface, score_rect)
    
    def checkGameOver(self):
        if self.doodler.rect.centery >= 890:
            return True
        return False

    def showGameOver(self):
        game_over_surface = score_font.render('Press R to play again', True, (128, 128, 0))
        game_over_surface_rect = game_over_surface.get_rect(center = (266, 200))
        screen.blit(game_over_surface, game_over_surface_rect)

        # Arquivo com os highscores
        highscores = open(files_path + "highscores.txt", "r")  # Primeiro lê o arquivo
        highscores_lista = highscores.readlines()  # Salva os valores de highscores em uma lista
        highscores.close()
        highscores = open(files_path + "highscores.txt", "a")
        if self.score > int(highscores_lista[-1]):  # Caso o score seja maior que o último ele adiciona o novo highscore
            highscores.write("\n" + str(self.score))
        highscores.close()

        highscore_surface = score_font.render("Highscore: " + str(highscores_lista[-1]), True, (128, 128, 0))
        highscore_surface_rect = highscore_surface.get_rect(center = (266, 300))
        screen.blit(highscore_surface, highscore_surface_rect)



SPRING_SPAWN = pygame.USEREVENT
pygame.time.set_timer(SPRING_SPAWN, 15000)



# MAIN LOOP
main = Main()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SPRING_SPAWN:
            main.spring.spawnSpring(0, 0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                main.doodler.moveDoodlerLeft()
            
            if event.key == pygame.K_RIGHT: 
                main.doodler.moveDoodlerRight()

            if event.key == pygame.K_r:
                main.game_over = False
                main.doodler.rect.center = (266, 400) 
                main.doodler.y_vel = 0
                main.score = 0
                main.platform.startPlatforms(10)

        if event.type == pygame.KEYUP:
            main.doodler.x_change = 0 


    main.update()
    pygame.display.update()
    clock.tick(60) 


