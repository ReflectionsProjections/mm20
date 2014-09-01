import pygame
import config.handle_constants
import json
import random
import time
import math
from map_functions import map_reader

NO_CHAIR = (-100, -100)


class Visualizer(object):

    def __init__(self, rooms=None, map_overlay=None, **kwargs):
        self.serverDefaults = config.handle_constants.retrieveConstants("serverDefaults")
        self.constants = config.handle_constants.retrieveConstants("visualizerDefaults")
        self.SCREEN_WIDTH = self.constants["SCREEN_WIDTH"]
        self.SCREEN_MAP_WIDTH = self.SCREEN_WIDTH - self.constants["STATSBARWIDTH"]
        self.MAP_WIDTH = self.serverDefaults["mapWidth"]
        self.SCREEN_HEIGHT = self.constants["SCREEN_HEIGHT"]
        self.MAP_HEIGHT = self.serverDefaults["mapHeight"]
        self.MAX_FPS = self.constants["MAX_FPS"]
        self.TITLE = self.constants["TITLE"]
        self.running = True
        self.colors = self.constants["TEAMCOLORS"]
        for i in range(len(self.colors)):
            self.colors[i] = tuple(self.colors[i])
        self.people = list()
        self.ai = list()
        self.team_names = list()
        self.messages = list()
        self.game_done = False
        self.game_result = None
        self.debug = kwargs["debug"]
        self.rooms = rooms
        self.map_overlay = map_overlay or self.constants["map_overlay"]
        self.quitWhenDone = self.constants['QUIT_WHEN_DONE']
        self.set_scaleFactor()
        
        # shuffle seat assignment
        if self.rooms:
            for r in self.rooms.values():
                random.shuffle(r.chairs)

        pygame.init()
        self.setup()

    def scale(self, pos):
        return (int(pos[0] * self.scaleFactor[0]), int(pos[1] * self.scaleFactor[1]))

    def setup(self):
        pygame.display.set_caption(self.TITLE)
        self.ScreenSurface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.GameClock = pygame.time.Clock()
        image = pygame.image.load(self.map_overlay)
        self.MAP_HEIGHT = image.get_height()
        self.MAP_WIDTH = image.get_width()
        self.set_scaleFactor()
        image = image.convert()
        self.background = pygame.transform.scale(image, (self.SCREEN_MAP_WIDTH, self.SCREEN_HEIGHT))
        
        image = pygame.image.load("person.png").convert_alpha()
        self.personImage = pygame.transform.scale(image, (32, 32))
        # self.teamPersonImages = []

    def set_scaleFactor(self):
            self.scaleFactor = (float(self.SCREEN_WIDTH - self.constants["STATSBARWIDTH"]) / self.MAP_WIDTH, float(self.SCREEN_HEIGHT) / self.MAP_HEIGHT)

    def run_from_file(self, file_name=""):

        # Load game log
        json_file = None
        try:
            json_file = open(file_name)
        except:
            self.running = False
            print "ERROR: Invalid game logfile."
            return

        # Run the game
        for turn_str in json_file:
            self.frame(turn_str)

        # If game is done and we're supposed to quit on exit, wait a while then exit
        if self.quitWhenDone:
            print "Game done; exiting"
            time.sleep(5)
            pygame.quit()

    def movementIsComplete(self):
        for p in self.people:
            if p.targetPos != p.pos:
                return False
        return True

    def frame(self, turn=None):
        while self.running and self.update_state(json.loads(turn)):

            # Smooth moving
            movementFinalized = False
            frameCount = 0
            while not movementFinalized or frameCount < self.constants["MIN_FRAMES"]:
                frameCount += 1
                movementFinalized = self.movementIsComplete()

                self.draw()
                self.GameClock.tick(self.MAX_FPS)

                for p in self.people:
                    if p.targetPos != p.pos:
                        length = math.sqrt(math.pow((p.targetPos[0] - p.pos[0]), 2) + math.pow((p.targetPos[1] - p.pos[1]), 2))
                        if length > self.constants["WALK_SPEED"]:
                            x_dir = float(p.targetPos[0] - p.pos[0]) / length
                            y_dir = float(p.targetPos[1] - p.pos[1]) / length

                            p.pos = (p.pos[0] + x_dir * self.constants["WALK_SPEED"], p.pos[1] + y_dir * self.constants["WALK_SPEED"])
                        else:
                            p.pos = p.targetPos # To avoid floating point errors

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
            if not self.game_done:
                break

    def draw(self):
        #Draw background
        self.ScreenSurface.fill((0, 0, 0))
        self.ScreenSurface.blit(self.background, (0, 0))

        #Draw people in rooms
        for p in self.people:
            color = self.colors[-1]
            if p.team < len(self.colors):
                color = self.colors[p.team]

            if self.debug:
                pygame.draw.circle(
                    self.ScreenSurface,
                    (0, 0, 0),
                    self.scale(p.pos),
                    self.constants["PERSON_SIZE"],
                    0,
                )
                pygame.draw.circle(
                    self.ScreenSurface,
                    color, self.scale(p.pos),
                    self.constants["PERSON_SIZE"] - 2,
                    0)

            else:
                scale_pos = self.scale((p.pos[0], p.pos[1]))
                self.ScreenSurface.blit(p.image, [p - 16 for p in scale_pos])


        #Draw AI info
        namefont = pygame.font.SysFont("monospace", 40)
        aifont = pygame.font.SysFont("monospace", 20)
        x_pos = 0
        for i in range(len(self.ai)):
            color = self.colors[-1]
            if i < len(self.colors):
                color = self.colors[i]
            label = namefont.render(self.team_names[i], 2, color)
            self.ScreenSurface.blit(label, (self.SCREEN_MAP_WIDTH, x_pos))
            x_pos += 40
            for key, val in self.ai[i].iteritems():
                label = aifont.render(key + ": " + str(val), 1, (255, 255, 255))
                self.ScreenSurface.blit(label, (self.SCREEN_MAP_WIDTH, x_pos))
                x_pos += 20

        #Draw actions (move animations? failure prompts?)

        #If game is over, show winner
        if self.game_done:
            for i in range(len(self.game_result)):
                if self.game_result[i]["winner"]:
                    gameoverfont = pygame.font.SysFont("monospace", 100)
                    label = gameoverfont.render(self.team_names[i] + " WINS!", 35, (12, 12, 12))
                    self.ScreenSurface.blit(label, (0, 0))

        #flip display
        pygame.display.flip()

    def update_state(self, turn):
        # check to see if the game has ended 
        if "winner" in turn[0]:
            self.game_done = True
            self.game_result = turn
            return not self.quitWhenDone
        if "team_name" in turn[0]:
            self.add_teams(turn)
            return False
        #reshape data
        for i, player in enumerate(turn):
            self.ai[i] = player["aiStats"]
            for person in player["people"].values():
                if person["team"] == i:

                    visPlayer = self.people[person["person_id"]]
                    acted = person.get("acted", "asleep" if person["asleep"] else None)

                    currentRoom = self.rooms[person["location"]]
                    newRoom = self.rooms[person["location"]]

                    # Determine player position
                    if acted == "eat":
                        visPlayer.targetPos = currentRoom.snacktables[0]
                        if visPlayer in currentRoom.sitting:
                            currentRoom.sitting.remove(visPlayer)
                    elif acted in ["code", "move", "theorize"]:
                        visPlayer.sit_in_room(newRoom, currentRoom)

                    visPlayer.set_data(
                        person["location"],
                        acted,
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

            teamImage = self.personImage.copy()

            for person in player["team"].values():

                visPlayer = self.people[person["person_id"]]
                room = self.rooms[person["location"]]

                visPlayer.set_image(teamImage)

                visPlayer.sit_in_room(room)
                visPlayer.pos = visPlayer.targetPos
                visPlayer.set_data(
                    person["location"],
                    None,
                    person["team"], person["name"], self)

            color = self.colors[-1]
            if visPlayer.team < len(self.colors):
                color = self.colors[visPlayer.team]
            pygame.PixelArray(teamImage).replace(pygame.Color(255, 0, 255, 255), color)
        

class VisPerson(object):
    """
    A object that will hold the data for a person to be drawn
    """
    def __init__(self, ):
        self.room = None
        self.targetPos = None
        self.pos = None
        self.action = None
        self.team = None
        self.name = None
        self.image = None

    def set_image(self, image):
        self.image = image

    def sit_in_room(self, newRoom, currentRoom=None):

        # No-op case
        if self in newRoom.sitting:
            return

        # Assign person a new spot
        numPeople = len(newRoom.sitting)
        numChairs = len(newRoom.chairs)
        numStand = len(newRoom.stand)
        if numPeople < numChairs:
            self.targetPos = newRoom.chairs[numPeople]
        elif numPeople < numChairs + numStand:
            self.targetPos = newRoom.stand[numPeople - numChairs]
        else:
            print "NOT ENOUGH ROOM!\n"

        # Add person to room if they aren't there already
        if currentRoom and self in currentRoom.sitting:
            currentRoom.sitting.remove(self)
        newRoom.sitting.add(self)
        self.room = newRoom.name

        return
        
    def set_data(self, room, act, team, name, visualizer):
        """
        Fields to be used
        """
        self.room = room
        self.action = act
        self.team = team
        self.name = name
        
        
if __name__ == "__main__":
    mapPath = config.handle_constants.retrieveConstants("serverDefaults")['map']
    vis = Visualizer(map_reader(mapPath))
    vis.run_from_file(("../serverlog.json"))

