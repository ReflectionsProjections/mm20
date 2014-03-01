

import pygame
import sys
import os

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700

MAX_FPS = 60

GameClock = None

TITLE = "Visualizer"

def setup():
	pygame.display.set_caption(TITLE)
	global ScreenSurface
	ScreenSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	global GameClock
	GameClock = pygame.time.Clock()

def main():
	while(1):
		draw()
		pygame.display.flip()
		GameClock.tick(MAX_FPS)

def draw():
	image = pygame.image.load("siebel-basement-map.bmp").convert()
	ScreenSurface.blit(image, (0, 0))


pygame.init()
setup()
main()

