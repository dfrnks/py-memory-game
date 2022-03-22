# import pygame
#
#
# background_colour = (000, 255, 255)
# (width, height) = (300, 200)
#
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption('Memory game')
# screen.fill(background_colour)
#
# pygame.display.flip()
#
# running = True
# while running:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       running = False
#
#
#
#


import pygame, sys
from pygame.locals import *
pygame.init()
#-------------------------------------------------------------------------------
# Settings
WIDTH = 300
HEIGHT = 300
FPS = 60
#-------------------------------------------------------------------------------
# Screen Setup
WINDOW = pygame.display.set_mode([WIDTH, HEIGHT])
CAPTION = pygame.display.set_caption('Test')
SCREEN = pygame.display.get_surface()
TRANSPARENT = pygame.Surface([WIDTH, HEIGHT])
TRANSPARENT.set_alpha(255)
TRANSPARENT.fill((255, 255, 255))
#-------------------------------------------------------------------------------
# Misc stuff
rect1 = pygame.draw.rect(SCREEN, (255, 255, 255), (0, 0, 50, 50))
rect2 = pygame.draw.rect(SCREEN, (255, 255, 255), (0, 55, 50, 50))
rect3 = pygame.draw.rect(SCREEN, (255, 255, 255), (55, 0, 50, 50))
rect4 = pygame.draw.rect(SCREEN, (255, 255, 255), (55, 55, 50, 50))

rectangles = [rect1, rect2, rect3, rect4]

#-------------------------------------------------------------------------------
# Refresh Display
pygame.display.flip()
#-------------------------------------------------------------------------------
# Main Loop
while True:
    pos = pygame.mouse.get_pos()
    mouse = pygame.draw.circle(TRANSPARENT, (0, 0, 0), pos , 0)
    # Event Detection---------------
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            for rect in rectangles:
                if rect.contains(mouse):
                    rect.Color
                    rect = pygame.draw.rect(SCREEN, (155, 155, 155), (rect.left, rect.top, rect.width, rect.height))
                    pygame.display.flip()
