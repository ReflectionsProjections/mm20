import pygame
import sys
import os
import config.handle_constants

class Visualizer( object ):
    SCREEN_WIDTH = 1300
    SCREEN_HEIGHT = 700

    MAX_FPS = 60

    GameClock = None

    background = None

    TITLE = "Visualizer"

    running = True

    def __init__(self):
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

    def main(self):
        while(self.running):
            self.frame()

    def frame(self):
        self.step()
        self.draw()
        self.GameClock.tick(self.MAX_FPS)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False


    def step(self):
        pass

    def draw(self):
        self.ScreenSurface.blit(self.background, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    vis = Visualizer()
    vis.main()

