import pygame
import config.handle_constants

class Visualizer( object ):

    def __init__(self, rooms=None):
        self.constants = config.handle_constants.retrieveConstants("visualizerDefaults")
        self.SCREEN_WIDTH = self.constants["SCREEN_WIDTH"]
        self.SCREEN_HEIGHT = self.constants["SCREEN_HEIGHT"]
        self.MAX_FPS = self.constants["MAX_FPS"]
        self.TITLE = self.constants["TITLE"]
        self.running = True
        self.colors = self.constants["TEAMCOLORS"]
        for i in range(len(self.colors)):
            self.colors[i] = tuple(self.colors[i])
        self.rooms = rooms
        self.people = list()
        self.ai = list()
        self.messages = list()
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
        if self.running:
            self.update_state(turn)
            self.draw()
            self.GameClock.tick(self.MAX_FPS)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.running = False


    def draw(self, ai = None):
        #Draw background
        self.ScreenSurface.blit(self.background, (0, 0))

        #Draw people in rooms
        for p in self.people:
            color = self.colors[-1]
            if p["team"] < len(colors):
                color = self.colors[p["team"]]
            pygame.draw.circle(self.ScreenSurface, color, p["pos"], 4, 0)

        #Draw AI info

        #Draw actions (move animations? failure prompts?)

        #flip display
        pygame.display.flip()

    def update_state(self, turn):
        pass

if __name__ == "__main__":
    vis = Visualizer()
    vis.run_from_file()

