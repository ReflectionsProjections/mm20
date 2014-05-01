import pygame
import sys
import os


SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700

MAX_FPS = 60

GameClock = None

TITLE = "Visualizer"

running = True

def setup():
    pygame.display.set_caption(TITLE)
    global ScreenSurface
    ScreenSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    global GameClock
    GameClock = pygame.time.Clock()

def main():
    while(running):
        frame()

def frame():
    step()
    draw()
    GameClock.tick(MAX_FPS)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    frame()


def step():
    pass

def draw():
    image = pygame.image.load("siebel-basement-map.bmp").convert()
    image = pygame.transform.scale(image,(SCREEN_WIDTH, SCREEN_HEIGHT))
    ScreenSurface.blit(image, (0, 0))
    pygame.display.flip()


pygame.init()
setup()
if __name__ == "__main__":
    main()

