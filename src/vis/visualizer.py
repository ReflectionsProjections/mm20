import pygame
import sys
import os
import config.handle_constants

class Visualizer( object ):

    def __init__(self, rooms=None):
        self.constants = config.handle_constants.retrieveConstants("visualizerDefaults")
        self.SCREEN_WIDTH = self.constants["SCREEN_WIDTH"]
        self.SCREEN_HEIGHT = self.constants["SCREEN_HEIGHT"]
        self.MAX_FPS = self.constants["MAX_FPS"]
        self.TITLE = self.constants["TITLE"]
        self.running = True
        pygame.init()
        self.setup()

    def setup(self):
        pygame.display.set_caption(self.TITLE)
        self.ScreenSurface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.GameClock = pygame.time.Clock()
        image = pygame.image.load(config.handle_constants.retrieveConstants("serverDefaults")["map"]).convert()
        self.background = pygame.transform.scale(image,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def run_from_file(self, file_name=""):
        while(self.running):
            self.frame()

    def frame(self, turn=None):
        self.draw()
        self.GameClock.tick(self.MAX_FPS)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False


    def draw(self):
        self.ScreenSurface.blit(self.background, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    vis = Visualizer()
    vis.run_from_file()

