import pygame
import config.handle_constants
import json
import random

NO_CHAIR = (-100, -100)

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
        # suffule seat assinment
        for r in self.rooms.values():
            random.shuffle(r.chairs)
        self.people = list()
        self.ai = list()
        self.team_names = list()
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
            d = self.update_state(json.loads(turn))
            while True and d:
                self.draw()
                self.GameClock.tick(self.MAX_FPS)
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            self.running = False
                if not self.game_done or not self.running:
                    break


    def draw(self):
        #Draw background
        self.ScreenSurface.fill((0,0,0))
        self.ScreenSurface.blit(self.background, (0, 0))

        #Draw people in rooms
        for p in self.people:
            color = self.colors[-1]
            if p.team < len(self.colors):
                color = self.colors[p.team]
            pygame.draw.circle(self.ScreenSurface, (0,0,0), p.pos, 5, 0)
            pygame.draw.circle(self.ScreenSurface, color, p.pos, 4, 0)

        #Draw AI info
        namefont = pygame.font.SysFont("monospace", 40)
        aifont = pygame.font.SysFont("monospace", 20)
        x_pos = 0
        for i in range(len(self.ai)):
            color = self.colors[-1]
            if i < len(self.colors):
                color = self.colors[i]
            label = namefont.render(self.team_names[i], 2, color)
            self.ScreenSurface.blit(label, (self.SCREEN_WIDTH - self.constants["STATSBARWIDTH"], x_pos))
            x_pos +=40
            for key, val in self.ai[i].iteritems():
                label = aifont.render(key+": "+str(val), 1, (255,255,255))
                self.ScreenSurface.blit(label, (self.SCREEN_WIDTH - self.constants["STATSBARWIDTH"], x_pos))
                x_pos +=20

        #Draw actions (move animations? failure prompts?)

        #If game is over, do stuff
        if self.game_done:
            for i in range(len(self.game_result)):
                if self.game_result[i]["winner"]:
                    gameoverfont = pygame.font.SysFont("monospace", 100)
                    label = gameoverfont.render(self.team_names[i]+ " WINS!", 40, (12, 12, 12))
                    self.ScreenSurface.blit(label, (0, 0))

        #flip display
        pygame.display.flip()

    def update_state(self, turn):
        # check to see if the game as ended 
        if "winner" in turn[0]:
            self.game_done = True
            self.game_result = turn
            return True
        if "team_name" in turn[0]:
            self.add_teams(turn)
            return False
        #reshape data
        for i, player in enumerate(turn):
            self.ai[i] = player["aiStats"]
            for person in player["people"]:
                if person["team"] == i:

                    self.people[person["person_id"]].set_data(
                        person["location"],
                        person["position"],
                        person["acted"] or
                        ("asleep" if person["asleep"] else None),
                        person["team"], person["name"], self)
        return True
                        
    def add_teams(self, teams):
        """
        set up the visualizer to view the teams
        """
        self.ai = [None] * len(teams)
        self.team_names = list(self.ai)
        number_of_people = 0
        
        for i, player in enumerate(teams):
            self.team_names[i] = player["team_name"]
            number_of_people += len(player["team"])
        self.people = [VisPerson() for _ in xrange(number_of_people)]
        for player in teams:
            for person in player["team"]:
                self.people[person["person_id"]].set_data(
                    person["location"],
                    person["position"],
                    person["acted"] or
                    ("asleep" if person["asleep"] else None),
                    person["team"], person["name"], self)
        


class VisPerson(object):
    """
    A object that will hold the data for a person to be drawn
    """
    def __init__(self, ):
        self.room = None
        self.pos = None
        self.action = None
        self.team = None
        self.name = None
        
    def set_data(self, room, pos, act, team, name, visualizer):
        """
        Fields to be used
        """
        self.pos = pos
        self.room = room
        self.action = act
        self.team = team
        self.name = name
        
        

if __name__ == "__main__":
    vis = Visualizer()
    vis.run_from_file()

