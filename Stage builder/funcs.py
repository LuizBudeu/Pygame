import pygame
from constants import *


pygame.init()
font = pygame.font.Font("freesansbold.ttf", 20)


def drawRects(screen, stage):
    for i in range(stage["NUM_OF_RECTS"]):
        pygame.draw.rect(screen, stage["Colors"][i], stage["Rects"][i])


def screenUpdate(screen, stage, buttonsDic, selectedColor):
    screen.fill(LIGHTBLUE)
    pygame.draw.line(screen, WHITE, (LINE_X_POS, 0), (LINE_X_POS, WINDOWS_SIZE[1]), 5)
    drawRects(screen, stage)
    checkRectsBorders(stage)
    showColorOptions(screen, selectedColor)

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


def printRemoval(screen):
    text_surface = font.render("Select rect", True, DARKGRAY)
    text_rect = text_surface.get_rect(center = (100, 300))
    screen.blit(text_surface, text_rect)

    text_surface = font.render("to remove", True, DARKGRAY)
    text_rect = text_surface.get_rect(center = (100, 330))
    screen.blit(text_surface, text_rect)

    outline_rect = pygame.Rect(text_rect.left - 20, text_rect.top - 45, text_surface.get_width() + 40, text_surface.get_height() * 3 + 20)
    pygame.draw.rect(screen, WHITE, outline_rect, 3)



def insertNewRect(stage, color):
    stage["NUM_OF_RECTS"] += 1
    stage["Rects"].append(pygame.Rect(100, 100, 100, 100))
    stage["Colors"].append(color)



def deleteRect(stage, rect):
    stage["NUM_OF_RECTS"] -= 1
    stage["Colors"].pop(stage["Rects"].index(rect))
    stage["Rects"].remove(rect)


def showColorOptions(screen, selectedColor):
    for i, color in enumerate(colorOptions):
        if color == highlighted(selectedColor):
            pygame.draw.rect(screen, color, colorOptionsRects[i], 3)
        else: 
            pygame.draw.rect(screen, color, colorOptionsRects[i])


def hoveringColorOption(mx, my):
    for crect in colorOptionsRects:
        if crect.collidepoint(mx, my):
            return True, colorOptions[colorOptionsRects.index(crect)]

    return False, None
    

def highlighted(selectedColor):
    for color in colorOptions:
        if color == selectedColor:
            return color


