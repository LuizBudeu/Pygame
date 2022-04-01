# MODULES
import pygame, sys, os, math, random





# CONSTANTS
WINDOW_SIZE = (1440, 900)

LIGHTBLUE = (116, 247, 241)
WHITE = (255, 255, 255)
BROWN = (112, 46, 2)
REDDISHBROWN = (212, 54, 4)
SELECTEDREDDISHBROWN = (166, 42, 3)
GREENISH = (80, 189, 21)
SELECTEDGREENISH = (65, 156, 16)
DARKGRAY = (28, 28, 28)
GRAY = (214, 214, 212)
PURPLE = (158, 9, 232)
GREEN = (4, 249, 4)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 247, 0)
BLACK = (0, 0, 0)
ORANGE= (255, 166, 0)

GRAVITY = 0.5
LINE_LENGTH = 80
LAUNCH_POINT = (100, 700)






# INITIALIZATIONS
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)    
clock = pygame.time.Clock()
pygame.display.set_caption("Raft Wars")
time0 = 0






# STAGES
Stages = {
    1: {
        "NUM_OF_ENEMIES": 2,
        "ENEMIES_POS": [(1100, LAUNCH_POINT[1] - 20), (1200, LAUNCH_POINT[1] - 20)] 
    },
    2: {
        "NUM_OF_ENEMIES": 2,
        "ENEMIES_POS": [(1100, LAUNCH_POINT[1] - 20), (1300, LAUNCH_POINT[1] - 100)]
    },
    3: {
        "NUM_OF_ENEMIES": 3,
        "ENEMIES_POS": [(1000, LAUNCH_POINT[1] - 20), (1150, LAUNCH_POINT[1] - 20), (1300, LAUNCH_POINT[1] - 20)]
    }
}






# UTILITY FUNCTIONS
def screenUpdate(stage_num, enemies, ally, ball, powerMeter, turn):
    global time0

    screen.fill(LIGHTBLUE)
    handleEnemies(enemies, turn)
    ally.draw()
    handlePowerMeter(powerMeter)
    drawArrow()
    drawTurnTriangle(turn, ally, enemies)
    drawTurnBox(turn, enemies)

    if ball != None:
        handleBall(ball)

        hitEnemy, enemy = checkEnemyHit(ball, enemies)
        if hitEnemy:
            if enemy.alive:
                time1 = pygame.time.get_ticks()
                if time1 - time0 >= 600:
                    enemy.calculateDamage(ball)
                time0 = pygame.time.get_ticks()

        elif checkAllyHit(ball, ally):
            if turn != 0:
                time1 = pygame.time.get_ticks()
                if time1 - time0 >= 600:
                    ally.calculateDamage(ball)
                time0 = pygame.time.get_ticks()

    showLevelAndCoins(stage_num)
        

def getMousePos():
    return pygame.mouse.get_pos()


def handleEnemies(enemies, turn):
    drawEnemies(enemies)


def drawEnemies(enemies):
    for enemy in enemies:
        enemy.draw()
            

def handleBall(ball):
    ball.posx += ball.velx
    ball.vely += GRAVITY
    ball.posy += ball.vely 
    ball.draw((round(ball.posx), round(ball.posy)))


def handlePowerMeter(powerMeter):
    powerMeter.draw()
    
    if powerMeter.changing:
        powerMeter.changeStrength()


def resetPowerMeter(powerMeter):
    powerMeter.changing = False
    powerMeter.inner_width = 1


def calculatePoint():
    mx, my = getMousePos()

    try:
        a = math.atan((LAUNCH_POINT[1] - my)/(mx - LAUNCH_POINT[0]))

        if mx - LAUNCH_POINT[0] > 0 and LAUNCH_POINT[1] - my > 0:
            if 0 < a < math.pi:
                return int(LAUNCH_POINT[0] + LINE_LENGTH*math.cos(a)), int(LAUNCH_POINT[1] - LINE_LENGTH*math.sin(a))
        
        else:
            if mx - LAUNCH_POINT[0] < 0:
                return LAUNCH_POINT[0], LAUNCH_POINT[1] - LINE_LENGTH
            elif LAUNCH_POINT[1] - my < 0:
                return LAUNCH_POINT[0] + LINE_LENGTH, LAUNCH_POINT[1]

    except:
        pass
    

def drawArrow():
    endPoint = calculatePoint()

    if endPoint != None:
        pygame.draw.line(screen, (227, 227, 227), LAUNCH_POINT, endPoint, 3)
    else:
        pygame.draw.line(screen, (227, 227, 227), LAUNCH_POINT, (LAUNCH_POINT[0] + LINE_LENGTH, LAUNCH_POINT[1]), 3)


def calculatePower(length):
    mx, my = getMousePos()

    if mx - LAUNCH_POINT[0] != 0:
        a = math.atan((LAUNCH_POINT[1] - my)/(mx - LAUNCH_POINT[0]))

        if mx - LAUNCH_POINT[0] > 0 and LAUNCH_POINT[1] - my > 0:
            if 0 < a < math.pi:
                return int(length*math.cos(a)), int(length*math.sin(a))
        
        else:
            if mx - LAUNCH_POINT[0] < 0:
                return 0, length
            elif LAUNCH_POINT[1] - my < 0:
                return length, 0
    
    else: return 0, length


def checkEnemyHit(ball, enemies): 
    for enemy in enemies:
        if ball.rect.colliderect(enemy):
            return True, enemy

    return False, None
        

def checkAllyHit(ball, ally):
    if ball.rect.colliderect(ally):
        return True 

    return False


def drawTurnTriangle(turn, ally, enemies):
    surf = pygame.image.load("imgs/turn-triangle.png").convert_alpha()
    rect = surf.get_rect()

    if turn % (len(enemies) + 1) == 0:
        rect.centerx, rect.centery = ally.rect.centerx, ally.rect.centery - 90
    
    else:
        rect.centerx, rect.centery = enemies[turn-1].rect.centerx, enemies[turn-1].rect.centery - 90

    screen.blit(surf, rect)


def drawTurnBox(turn, enemies):
    if turn % (len(enemies) + 1) == 0:
        b = Button(text="Ally's turn", center_pos=(WINDOW_SIZE[0]//2, 50), bg_color=YELLOW, bg_tocolor=YELLOW)
    
    else:
        b = Button("Enemy's turn", center_pos=(WINDOW_SIZE[0]//2, 50), bg_color=RED, bg_tocolor=RED)

    b.draw()


def showVictoryScreen(stage_num):
    font = pygame.font.Font("freesansbold.ttf", 150)
    text_surf = font.render("YOU WON!", True, GREEN)
    text_rect = text_surf.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 100))
    screen.blit(text_surf, text_rect)

    b1 = Button(text="Return to menu", center_pos=(WINDOW_SIZE[0]//2 - 150, 750))

    b2 = Button(text="Next stage", center_pos=(WINDOW_SIZE[0]//2 + 150, 750))

    while True:
        mx, my = getMousePos()

        b1.draw()
        b2.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if b2.hovering(mx, my):
                        try:
                            playStage(stage_num+1)
                        except:
                            showMainMenu()

                    elif b1.hovering(mx, my):
                        showMainMenu()

        pygame.display.update()
        clock.tick(60)


def showDefeatScreen(stage_num):
    font = pygame.font.Font("freesansbold.ttf", 150)
    text_surf = font.render("YOU LOST!", True, RED)
    text_rect = text_surf.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 100))
    screen.blit(text_surf, text_rect)

    b1 = Button(text="Return to menu", center_pos=(WINDOW_SIZE[0]//2 - 150, 750))

    b2 = Button(text="Try again", center_pos=(WINDOW_SIZE[0]//2 + 150, 750))
    
    
    while True:
        mx, my = getMousePos()

        b1.draw()
        b2.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if b2.hovering(mx, my):
                        print(stage_num)
                        playStage(stage_num)

                    elif b1.hovering(mx, my):
                        showMainMenu()

        pygame.display.update()
        clock.tick(60)


def showLevelAndCoins(stage_num):
    font = pygame.font.Font("freesansbold.ttf", 30)
    text_surf = font.render(f"Level: {stage_num}", True, BLACK)
    text_rect = text_surf.get_rect(topright=(WINDOW_SIZE[0] - 5, 5))
    screen.blit(text_surf, text_rect)

    text_surf = font.render(f"Coins: {coins}", True, (237, 230, 2))
    text_rect = text_surf.get_rect(topleft=(5, 5))
    screen.blit(text_surf, text_rect)


def drawAimAssist(velx, vely):
    try:
        v0 = math.sqrt(velx**2 + vely**2)
        a = math.atan(vely/velx)
        x = -v0**2 * math.sin(a*2)/GRAVITY
        
        vy = math.sqrt(vely**2 + 2*GRAVITY*80)
        t = (vy + vely)/GRAVITY
        dx = velx*t/1.25

        pygame.draw.circle(screen, WHITE, (LAUNCH_POINT[0] + round(x) + round(dx), LAUNCH_POINT[1] + 80), 5)

    except: 
        pass







# CLASSES 
class Button:
    def __init__(self, text = "aaa", font_size = 20, dim = (200, 100), center_pos = (100, 50), bg_color = (154, 171, 170), bg_tocolor = (110, 122, 122)):
        self.font = pygame.font.Font("freesansbold.ttf", font_size)

        self.text = text
        self.bg_color = bg_color
        self.bg_tocolor = bg_tocolor

        self.rect = pygame.Rect(center_pos[0] - dim[0]//2, center_pos[1] - dim[1]//2, dim[0], dim[1])

    def draw(self):
        mx, my = getMousePos()
        if self.hovering(mx, my):
            pygame.draw.rect(screen, self.bg_tocolor, self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)

        text_surface = self.font.render(self.text, True, DARKGRAY)
        text_rect = text_surface.get_rect(center = self.rect.center)
        screen.blit(text_surface, text_rect)

    
    def hovering(self, mx, my):
        if self.rect.collidepoint(mx, my):
            return True
        
        return False


class Fighter:
    def __init__(self, pos, role):
        self.posx = pos[0]
        self.posy = pos[1]
        self.role = role
        self.alive = True

        if role == "ally":
            self.surf = pygame.image.load("imgs/ally.png").convert_alpha()
        elif role == "enemy":
            self.surf = pygame.image.load("imgs/enemy.png").convert_alpha()

        self.dead_surf = pygame.image.load("imgs/dead.png").convert_alpha()
        
        self.rect = self.surf.get_rect(topleft = pos)
        self.lifebar = Lifebar((self.rect.centerx, self.rect.top - 20))


    def draw(self):
        if self.alive:
            screen.blit(self.surf, self.rect)

        else:
            screen.blit(self.dead_surf, self.rect)
        
        self.lifebar.draw()

    def calculateDamage(self, ball):
        vel = math.sqrt(ball.velx**2 + ball.vely**2)
        self.takeDamage(round(vel/2))

    def takeDamage(self, damage):
        if self.lifebar.gwidth - damage >= 0:
            self.lifebar.gwidth -= damage
        else:
            self.lifebar.gwidth = 0
            self.alive = False


class Ball:
    def __init__(self, velx, vely):
        self.posx = LAUNCH_POINT[0]
        self.posy = LAUNCH_POINT[1]
        self.velx = velx
        self.vely = vely

        self.surf = pygame.image.load("imgs/ball.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (20, 20))
        self.rect = self.surf.get_rect()

    def draw(self, pos):
        self.rect.center = pos
        screen.blit(self.surf, self.rect)


class PowerMeter:
    def __init__(self):
        self.inner_width = 1
        self.changing = False

        self.x, self.y = 15, 830
        self.outerRect = pygame.Rect(self.x, self.y, 120, 50)

    def draw(self):
        self.innerRect = pygame.Rect(self.x+5, self.y+5, self.inner_width, 40)

        pygame.draw.rect(screen, BLACK, self.outerRect, 5)
        pygame.draw.rect(screen, GREEN, self.innerRect)

    def changeStrength(self):
        if self.inner_width >= 110:
            self.inner_width = 1
        
        else:
            self.inner_width += 1


class Lifebar:
    def __init__(self, pos):
        self.pos = pos
        self.gwidth = 50

        self.rrect = pygame.Rect(pos[0], pos[1], self.gwidth, 10)
        self.rrect.centerx = pos[0]

    def draw(self):
        self.grect = pygame.Rect(self.pos[0] - 25, self.pos[1], self.gwidth, 10)

        pygame.draw.rect(screen, RED, self.rrect)
        pygame.draw.rect(screen, GREEN, self.grect)







# MAIN FUNCTIONS
def runGame():
    showMainMenu()


coins = 0
def showMainMenu():
    while True:
        screen.fill(LIGHTBLUE)

        font = pygame.font.Font("freesansbold.ttf", 150)
        text_surf = font.render("RAFT WARS", True, (196, 190, 0))
        text_rect = text_surf.get_rect(center=(WINDOW_SIZE[0]//2, 250))
        screen.blit(text_surf, text_rect)


        font = pygame.font.Font("freesansbold.ttf", 30)
        text_surf = font.render("Level: 1", True, BLACK)
        text_rect = text_surf.get_rect(topright=(WINDOW_SIZE[0]-5, 5))
        screen.blit(text_surf, text_rect)


        font = pygame.font.Font("freesansbold.ttf", 30)
        text_surf = font.render(f"Coins: {coins}", True, (237, 230, 2))
        text_rect = text_surf.get_rect(topleft=(5, 5))
        screen.blit(text_surf, text_rect)



        playButton = Button(text="PLAY", font_size=40, dim=(500, 100), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 100), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        playButton.draw()

        mx, my = getMousePos()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if playButton.hovering(mx, my):
                        playStage(1)



        pygame.display.update()
        clock.tick(60) 


def playStage(stage_num):
    stage = Stages[stage_num]
    enemies = [Fighter(stage["ENEMIES_POS"][i], "enemy") for i in range(stage["NUM_OF_ENEMIES"])]
    ally = Fighter((LAUNCH_POINT[0] - 40, LAUNCH_POINT[1] - 20), "ally")
    ball = None
    powerMeter = PowerMeter()
    powerX, powerY = 0.1, 0.1
    turn = 0
    won = False
    ready = False
    READY_TO_PLAY = pygame.USEREVENT
    pygame.time.set_timer(READY_TO_PLAY, 1000) 
    


    # MAIN LOOP
    while True:
        screenUpdate(stage_num, enemies, ally, ball, powerMeter, turn)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == READY_TO_PLAY:
                ready = True

            if ready:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if turn % (len(enemies) + 1) == 0 and ally.alive:
                            powerMeter.changing = True
                            
                            

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if turn % (len(enemies) + 1) == 0 and ally.alive and ball == None:
                            powerX, powerY = calculatePower(powerMeter.inner_width)
                            velx, vely = powerX/1.8, -powerY/1.8
                            ball = Ball(velx, vely)
                            
                        resetPowerMeter(powerMeter)


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        ally.alive = False
                    
        
        # Draw Aim assist
        if powerMeter.changing:
            powerX, powerY = calculatePower(powerMeter.inner_width)
        drawAimAssist(powerX/1.8, -powerY/1.8)



        # Check ball boundaries
        if ball != None:
            if ball.posx >= WINDOW_SIZE[0] + 10 or ball.posy >= WINDOW_SIZE[1] + 10 or ball.posx <= -20:
                ball = None
                turn += 1

        # Reset turn
        if turn >= (len(enemies) + 1):
            turn = 0

        # Enemies' turn
        if turn != 0 and ball == None:
            if enemies[turn-1].alive:
                ball = Ball(-random.randint(15, 20), -random.randint(15, 20))
                ball.posx = enemies[turn-1].posx - 10
                ball.posy = enemies[turn-1].posy + 20 
            else:
                turn += 1


        # Check when loading first time
        if not ready:
            b = Button(text="loading...", center_pos=(WINDOW_SIZE[0]//2, 50), bg_color=GRAY, bg_tocolor=GRAY)
            b.draw()


        # Check if player won or lost
        if not ally.alive:
            showDefeatScreen(stage_num)

        else:
            won = True
            for enemy in enemies:
                if enemy.alive:
                    won = False
                    

            if won:
                showVictoryScreen(stage_num)
        


        pygame.display.update()
        clock.tick(60) 







# RUN
if __name__ == '__main__':
    runGame()
    
