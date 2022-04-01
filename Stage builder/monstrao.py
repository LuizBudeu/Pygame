# DECLARAÇÃO DE IMPORTS
import pygame, sys, os




# INICIALIZAÇÕES E CONSTANTES GLOBAIS
LIGHTBLUE = (116, 247, 241)
WHITE = (255, 255, 255)
BROWN = (112, 46, 2)
REDDISHBROWN = (212, 54, 4)
SELECTEDREDDISHBROWN = (166, 42, 3)
GREEN = (80, 189, 21)
SELECTEDGREEN = (65, 156, 16)
DARKGRAY = (28, 28, 28)

WINDOWS_SIZE = (1440, 900)
LINE_X_POS = 200

pygame.init()
screen = pygame.display.set_mode(WINDOWS_SIZE)    
clock = pygame.time.Clock()
pygame.display.set_caption("Stage builder")
font = pygame.font.Font("freesansbold.ttf", 20)





# FUNÇÕES
def drawRects(screen, stage, color):
    for i in range(stage["NUM_OF_RECTS"]):
        pygame.draw.rect(screen, color, stage["Rects"][i])


def screenUpdate(screen, stage, color, buttonsDic):
    screen.fill(LIGHTBLUE)
    pygame.draw.line(screen, WHITE, (LINE_X_POS, 0), (LINE_X_POS, WINDOWS_SIZE[1]), 5)
    drawRects(screen, stage, color)
    checkRectsBorders(stage)

    for button in buttonsDic.values():
        button.draw()


def getMousePos():
    return pygame.mouse.get_pos()


def hoveringRect(mx, my, stage):
    for rect in stage["Rects"]:
        if rect.collidepoint(mx, my):
           return True, rect

    return False, None


def dragRect(rect, mx, my):
    rect.center = mx, my


def hoveringButton(mx, my, buttonsDic):
    for button in buttonsDic.values():
        if button.rect.collidepoint(mx, my):
            return True, button

    return False, None


def checkRectsBorders(stage):
    for rect in stage["Rects"]:
        if rect.left <= 203:
            rect.left = 203

        if rect.right >= WINDOWS_SIZE[0]:
            rect.right = WINDOWS_SIZE[0]

        if rect.top <= 0:
            rect.top = 0

        if rect.bottom >= WINDOWS_SIZE[1]:
            rect.bottom = WINDOWS_SIZE[1]





# CLASSES
class Button:
    def __init__(self, screen, text, pos, color, tocolor):
        self.screen = screen
        self.text = text
        self.pos = pos
        self.color = color
        self.tocolor = tocolor

        self.rect = pygame.Rect(pos[0], pos[1], 160, 100)

    def draw(self):
        mx, my = getMousePos()
        if self.hoveringButton(mx, my):
            pygame.draw.rect(self.screen, self.tocolor, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)

        text_surface = font.render(self.text, True, DARKGRAY)
        text_rect = text_surface.get_rect(center = self.rect.center)
        self.screen.blit(text_surface, text_rect)


    def clickButton(self, stage):
        if self.text == "Insert new rect":
            stage["NUM_OF_RECTS"] += 1
            stage["Rects"].append(pygame.Rect(100, 100, 100, 100))

    
    def hoveringButton(self, mx, my):
        if self.rect.collidepoint(mx, my):
            return True
        
        return False






# VARIÁVEIS GLOBAIS
dragging = False
buttonsDic = {"gb": Button(screen, "Insert new rect", (20, 20), GREEN, SELECTEDGREEN),
              "rb": Button(screen, "Delete rect", (20, 150), REDDISHBROWN, SELECTEDREDDISHBROWN)
}

Stage1 = {
    "STAGE_SIZE": (WINDOWS_SIZE[0] - LINE_X_POS, WINDOWS_SIZE[1]),
    "NUM_OF_RECTS": 4,
    "Rects": [pygame.Rect(400, 500, 500, 100), pygame.Rect(700, 700, 500, 100),
              pygame.Rect(300, 100, 200, 100), pygame.Rect(900, 300, 100, 200)
              ]
}





# MAIN LOOP
while True:
    screenUpdate(screen, Stage1, BROWN, buttonsDic)
    mx, my = getMousePos()

    hoveringR, rect = hoveringRect(mx, my, Stage1)
    if hoveringR and dragging:
        dragRect(rect, mx, my)

    hoveringB, but = hoveringButton(mx, my, buttonsDic)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if hoveringR:
                    dragging = True
                if hoveringB:
                    but.clickButton(Stage1)

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False



    pygame.display.update()
    clock.tick(60) 



