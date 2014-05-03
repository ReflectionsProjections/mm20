import pygame
import config.handle_constants
import json
import random

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
        self.game_done = False
        self.game_result = None
        pygame.init()
        self.setup()

    def setup(self):
        pygame.display.set_caption(self.TITLE)
        self.ScreenSurface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.GameClock = pygame.time.Clock()
        image = pygame.image.load(config.handle_constants.retrieveConstants("serverDefaults")["map"]).convert()
        self.background = pygame.transform.scale(image,(self.SCREEN_WIDTH - self.constants["STATSBARWIDTH"], self.SCREEN_HEIGHT))

    def run_from_file(self, file_name=""):
        while(self.running):
            self.frame()

    def frame(self, turn=None):
        if self.running:
            self.update_state(json.loads(turn))
            self.draw()
            self.GameClock.tick(self.MAX_FPS)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.running = False


    def draw(self):
        #Draw background
        self.ScreenSurface.fill((0,0,0))
        self.ScreenSurface.blit(self.background, (0, 0))

        #Draw people in rooms
        for p in self.people:
            color = self.colors[-1]
            if p.team < len(self.colors):
                color = self.colors[p.team]
            pygame.draw.circle(self.ScreenSurface, color, p.pos, 4, 0)

        #Draw AI info
        myfont = pygame.font.SysFont("monospace", 40)
        label = myfont.render("AI!", 1, (255,255,255))
        self.ScreenSurface.blit(label, (self.SCREEN_WIDTH - self.constants["STATSBARWIDTH"], 0))

        #Draw actions (move animations? failure prompts?)

        #flip display
        pygame.display.flip()

    def update_state(self, turn):
        # check to see if the game as ended 
        if "winner" in turn[0]:
            self.game_done = True
            self.game_result = turn
            return
        #make the need structures
        self.ai = [None] * len(turn)
        self.people = [VisPerson() for _ in xrange (len(turn) * 3)]
        #reshape data
        for i, player in enumerate(turn):
            self.ai[i] = player["aiStats"]
            for room in player["map"]:
                for person in room["peopleInRoom"]:
                    if person["team"] == i:
                        pos = random.choice(
                            self.rooms[person["location"]].chairs)
                        self.people[person["person_id"]].set_data(
                            person["location"], pos,
                            person["acted"] or
                            ("asleep" if person["asleep"] else None),
                            person["team"])

            
                
class VisPerson(object):
    """
    A object that will hold the data for a person to be drawn
    """
    
    def set_data(self, room, pos, act, team):
        """
        Fields to be used
        """
        self.room = room
        self.pos = pos                  # (x, y) coordinats
        self.action = act
        self.team = team
        
        

if __name__ == "__main__":
    vis = Visualizer()
    vis.run_from_file()

