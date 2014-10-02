import pygame
from config.handle_constants import retrieveConstants
import json
import random
import time
import Queue
import math
from animation import Animation
from map_functions import map_reader
from vector import vecLen, angleBetween

NO_CHAIR = (-100, -100)

lastCachedPos = dict({"atest1": (-1, -1), "atest2": (-1, -1), "atest3": (-1, -1)})


class Visualizer(object):

    def __init__(self, rooms=None, map_overlay=None, **kwargs):
        self.serverDefaults = retrieveConstants("serverDefaults")
        self.constants = retrieveConstants("visualizerDefaults")
        self.mapConstants = retrieveConstants("map_reader_constants")
        self.map_overlay = map_overlay or self.constants["map_overlay"]
        self.MAX_FPS = self.constants["MAX_FPS"]
        self.TITLE = self.constants["TITLE"]
        self.running = True
        self.colors = self.constants["TEAMCOLORS"]
        for i in range(len(self.colors)):
            self.colors[i] = tuple(self.colors[i])
        self.people = list()
        self.professor = VisPerson()
        self.professor.pos = (-300, -300)
        self.professor.set_data(
            None,
            None, "PROFESSOR", self)
        self.ai = list()
        self.team_names = list()
        self.messages = list()
        self.game_done = False
        self.game_result = None
        self.debug = kwargs.get("debug", False)
        self.rooms = rooms
        self.quitWhenDone = self.constants['QUIT_WHEN_DONE']
        self.scaleMod = (1,1)
        self.Animations = {}
        self.frameNumber = 0

        # shuffle seat assignment
        if self.rooms:
            for r in self.rooms.values():
                random.shuffle(r.chairs)

        # Pathfinding variables
        self.allPaths = dict()
        self.availableConnections = dict()
        self.waypointRooms = dict()

        pygame.init()
        self.setup()

    def scale(self, pos):
        return (int(pos[0] * self.scaleMod[0]), int(pos[1] * self.scaleMod[1]))

    def setup(self):
        pygame.display.set_caption(self.TITLE)
        image = pygame.image.load(self.map_overlay)
        self.MAP_HEIGHT = image.get_height()
        self.MAP_WIDTH = image.get_width()
        self.ScreenSurface = pygame.display.set_mode((self.MAP_WIDTH, self.MAP_HEIGHT))
        self.GameClock = pygame.time.Clock()
        image = image.convert()
        self.background = pygame.transform.scale(image, (self.MAP_WIDTH, self.MAP_HEIGHT))
        profimage = self.constants["animations"]["PROFESSOR"]
        image = pygame.image.load(profimage[0]).convert_alpha()
        self.professor_image = pygame.transform.scale(image, (32,32))

        # self.personImage = pygame.transform.scale(image, (32, 32))
        # self.teamPersonImages = []

        # [Pathfinding] Get waypoints --> rooms mapping
        for r in self.rooms.values():
            for o in r.snacktable + r.stand + r.chairs + r.doors:
                if o not in self.waypointRooms:
                    self.waypointRooms[o] = set()
                self.waypointRooms[o].update((r.name,))

        # [Pathfinding] Get all paths
        for r in self.rooms.values():
            for p1 in r.paths:
                if p1 not in self.allPaths:
                    self.allPaths[p1] = dict()
                for p2 in r.paths[p1]:
                    self.allPaths[p1][p2] = r.paths[p1][p2]

        # [Pathfinding] Get connected paths
        for startPt in self.allPaths.keys():
            self.availableConnections[startPt] = []

        for startPt in self.allPaths.keys():
            for endPt in self.allPaths[startPt].keys():

                if startPt != endPt:
                    self.availableConnections[startPt].append(endPt)
                    self.availableConnections[endPt].append(startPt)

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
            self.test(turn_str)

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

    def update(self):
        self.frameNumber += 1
        if self.frameNumber > self.constants["MAX_FRAMES_PER_TURN"]:
            self.frameNumber = 0

    # Determine which points a player moves through to reach a certain position
    # (using A*, since performance here matters unlike in the map reader)
    def construct_path(self, start, end):

        # Rooms the path can go through
        allowedRooms = list(self.waypointRooms[start] | self.waypointRooms[end])

        # Queue of paths so far
        frontierPaths = Queue.PriorityQueue()
        frontierPaths.put([0, [start], 0])

        # Dict of points reached so far (to keep contains() at O(1))
        visited = dict()
        visited[start] = True

        while not frontierPaths.empty():

            currentNode = frontierPaths.get()
            currentPath = currentNode[1]  # A list of waypoints

            # Check if we've reached the goal - if so, terminate pathfinding
            currentWaypoint = currentPath[-1]
            if currentWaypoint == end:

                # Concatenate all the steps between the waypoints together
                currentSteps = []
                for i in range(0, len(currentPath) - 1):

                    a = currentPath[i+1]
                    b = currentPath[i]

                    fullPath = self.allPaths[a][b]
                    currentSteps.extend(fullPath)

                return (currentSteps, currentPath)

            # Expand it
            for nextWaypoint in self.availableConnections[currentWaypoint]:

                # Don't include already-visited points
                if nextWaypoint in visited:
                    continue

                # Don't include waypoints in non-allowed rooms
                inAllowedRooms = False
                for r in self.waypointRooms[nextWaypoint]:
                    if r in allowedRooms:
                        inAllowedRooms = True
                        break
                if not inAllowedRooms:
                    continue

                # Mark next waypoint as visited
                visited[nextWaypoint] = True

                # Add path to frontier
                nextPath = self.allPaths[nextWaypoint][currentWaypoint]
                travelled = currentNode[2] + len(nextPath) * self.mapConstants["path_step_size"]
                dist = vecLen(end, nextWaypoint)
                frontierPaths.put([travelled + dist, currentPath + [nextWaypoint], travelled])

        # No paths found
        print '\033[91mERROR: no path found between ' + str(start) + ' --> ' + str(end) + '\033[0m'
        return ([], [])

    def turn(self, turn=None):
        while self.running and self.update_state(json.loads(turn)):

            # Get paths
            for p in self.people:
                p.path = []
                if p.pos != p.targetPos:
                    (p.path, p.waypoints) = self.construct_path(p.pos, p.targetPos)
                    p.pathLength = len(p.path)

            # Smooth moving
            framesLeft = float(self.constants["FRAMES_PER_TURN"])
            movementFinalized = False
            while framesLeft >= 0 or not movementFinalized:
                movementFinalized = self.movementIsComplete()

                self.draw()
                self.update()
                self.GameClock.tick(self.MAX_FPS)

                framesLeft -= 1.0

                for p in self.people:

                    # --- Calculate path length ---
                    # Initial float
                    iterSteps = float(p.pathLength) / float(self.constants["FRAMES_PER_TURN"])

                    # Smooth float part out over frames
                    iterSteps = math.ceil(framesLeft * iterSteps) - math.floor((framesLeft - 1) * iterSteps)

                    # Keep people moving at a minimum pace
                    iterSteps = min(iterSteps, self.constants["MIN_STEPS_PER_FRAME"])
                    # ------ End path length ------

                    if p.path and len(p.path) > iterSteps:

                        for i in range(0, int(iterSteps)):
                            p.pos = p.path[0]
                            p.path.pop(0)

                        # Adjust rotation
                        rotationLookahead = self.constants["ROTATION_LOOKAHEAD"]
                        if len(p.path) > rotationLookahead:
                            p.set_rotation(angleBetween(p.pos, p.path[rotationLookahead]) - 90)
                        else:
                            p.set_rotation(angleBetween(p.pos, p.targetPos) - 90)

                    else:
                        p.pos = p.targetPos
                        p.path = []

                        # Check for direction marker, otherwise just keep current rotation
                        for d in self.rooms[p.room].dirmarkers:
                            if vecLen(d, p.pos) < self.constants["DIR_MARKER_RADIUS"]:
                                p.set_rotation(angleBetween(p.pos, d) - 90)
                                break

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.running = False
                        movementFinalized = True
            if self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.running = False
            if not self.game_done:
                break

    def draw(self):

        # Draw background
        self.ScreenSurface.fill((0, 0, 0))
        self.ScreenSurface.blit(self.background, (0, 0))

        #TODO: Draw professor
        self.ScreenSurface.blit(self.professor_image, [p - 16 for p in self.professor.pos])

        # Draw people in rooms
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
                # scale_pos = self.scale((p.pos[0], p.pos[1]))
                # self.ScreenSurface.blit(p.image, [p - 16 for p in scale_pos])
                self.Animations[p.team].draw(p, self.frameNumber)

            # Debug
            if self.debug and p.targetPos != p.pos and p.path:

                # Draw line to target
                pygame.draw.line(
                    self.ScreenSurface,
                    (0, 255, 0),
                    self.scale(p.targetPos),
                    self.scale(p.pos),
                    3
                )

                # Draw remaining path
                for q in range(0, len(p.path) - 1):
                    pygame.draw.line(
                        self.ScreenSurface,
                        (255, 0, 0),
                        self.scale(p.path[q]),
                        self.scale(p.path[q+1]),
                        1
                    )

                # Draw waypoints
                for q in p.waypoints:
                    pygame.draw.circle(
                        self.ScreenSurface,
                        (0, 0, 255),
                        self.scale(q),
                        5
                    )

                # Draw paths from current waypoint
                for c in self.availableConnections:
                    for c2 in self.availableConnections[c]:

                        drawLine = False
                        for p in self.people:
                            if p.name in lastCachedPos and c == lastCachedPos[p.name]:
                                drawLine = True
                                break
                            if p.name in lastCachedPos and c == p.pos:
                                lastCachedPos[p.name] = c

                        if drawLine:
                            qpath = self.allPaths[c][c2]
                            for q in range(0, len(qpath) - 1):
                                pygame.draw.line(
                                    self.ScreenSurface,
                                    (0, 0, 255),
                                    self.scale(qpath[q]),
                                    self.scale(qpath[q+1]),
                                    1
                                )

        # Draw AI info
        # namefont = pygame.font.SysFont("monospace", 40)
        # aifont = pygame.font.SysFont("monospace", 20)
        # x_pos = 0
        # for i in range(len(self.ai)):
        #     color = self.colors[-1]
        #     if i < len(self.colors):
        #         color = self.colors[i]
        #     label = namefont.render(self.team_names[i], 2, color)
        #     self.ScreenSurface.blit(label, (self.SCREEN_MAP_WIDTH, x_pos))
        #     x_pos += 40
        #     for key, val in self.ai[i].iteritems():
        #         label = aifont.render(key + ": " + str(val), 1, (255, 255, 255))
        #         self.ScreenSurface.blit(label, (self.SCREEN_MAP_WIDTH, x_pos))
        #         x_pos += 20

        # Draw actions (move animations? failure prompts?)

        # If game is over, show winner
        if self.game_done:
            for i in range(len(self.game_result)):
                if self.game_result[i] and self.game_result[i]["winner"]:
                    gameoverfont = pygame.font.SysFont("monospace", 100)
                    label = gameoverfont.render(self.team_names[i] + " WINS!", 35, (12, 12, 12))
                    self.ScreenSurface.blit(label, (0, 0))

        # Flip display
        pygame.display.flip()

    def update_state(self, turn):

        # Check to see if the game has ended
        firstTurn = next(t for t in turn if t)
        if "winner" in firstTurn:
            self.game_done = True
            self.game_result = turn
            return not self.quitWhenDone
        if "team_name" in firstTurn:
            self.add_teams(turn)
            return False

        movePeople = list()

        for e in firstTurn["events"]:
            if e["name"] == "PROFESSOR":
                self.professor.stand_in_room(self.rooms[e["message"]])
                self.professor.room = e["message"]
                self.professor.pos = self.professor.targetPos
            elif e["name"] == "NOPROFESSOR":
                if self.professor in self.rooms[self.professor.room].people:
                    self.rooms[self.professor.room].people.remove(self.professor)
                self.professor.pos = (-300, -300)
                self.professor.targetPos = (-300, -300)

        # Reshape data
        for i, player in enumerate(turn):

            # Skip bad teams
            if not player or player.get("status") == "Failure":
                continue

            self.ai[i] = player["aiStats"]

            for person in player["people"].values():
                if person["team"] == i:
                    visPerson = self.people[person["person_id"]]
                    visPerson.isBlocked = False
                    visPerson.action = None
                    visPerson.sentNoAction = True
                    if visPerson.toSleep:
                        visPerson.asleep = True
                    if visPerson.toWake:
                        visPerson.asleep = False

            for message in player["messages"]:
                if message["success"]:
                    self.people[message["person_id"]].action = message["action"]
                    self.people[message["person_id"]].sentNoAction = False
                else:
                    # make sure these are right reasons
                    if message["reason"] == "ASLEEP":
                        self.people[message["person_id"]].asleep = True
                        self.people[message["person_id"]].sentNoAction = False
                        self.people[message["person_id"]].isDistracted = False
                    # elif message["reason"] == "INVALID":
                        # self.people[message["person_id"]].isBlocked = True
                        # self.people[message["person_id"]].isDistracted = False
                        # self.people[message["person_id"]].sentNoAction = False
                    elif message["reason"] == "DISTRACTED":
                        self.people[message["person_id"]].isDistracted = True
                        self.people[message["person_id"]].sentNoAction = False
                    else:
                        self.people[message["person_id"]].isDistracted = False

            for person in player["people"].values():
                if person["team"] == i:

                    # Get existing data
                    # Disregard the name, visPlayer is actually a person
                    visPlayer = self.people[person["person_id"]]
                    acted = person.get("acted")
                    visPlayer.toSleep = False
                    visPlayer.toWake = False
                    if person["asleep"]:
                        visPlayer.toSleep = True
                    else:
                        visPlayer.toWake = True

                    currentRoom = self.rooms[visPlayer.room]
                    newRoom = self.rooms[person["location"]]

                    if currentRoom != newRoom or person["sitting"] != (visPlayer in currentRoom.sitting) or (acted != "eat" and len(currentRoom.snacktable) > 0 and visPlayer.pos == currentRoom.snacktable[0]):
                        movePeople.append(person)
                        if visPlayer in currentRoom.sitting:
                            currentRoom.sitting.remove(visPlayer)
                        if visPlayer in currentRoom.people:
                            currentRoom.people.remove(visPlayer)
                    else:
                        visPlayer.targetPos = visPlayer.pos

                    # Determine player position
                    if acted == "eat":
                        visPlayer.targetPos = currentRoom.snacktable[0]

                    visPlayer.set_data(
                        person["location"],
                        person["team"], person["name"], self)

            # Update sitting/standing
            for person in movePeople:
                visPlayer = self.people[person["person_id"]]
                newRoom = self.rooms[person["location"]]
                if person["sitting"]:
                    visPlayer.sit_in_room(newRoom)
                else:
                    visPlayer.stand_in_room(newRoom)

        return True

    # Initialization of the teams
    def add_teams(self, teams):
        """
        set up the visualizer to view the teams
        """

        # Remove null teams (due to bad clients)
        self.ai = [None] * len(teams)
        self.team_names = list(self.ai)
        number_of_people = 0

        for i, player in enumerate(teams):
            if player and player.get("status", "Failure") != "Failure":
                self.team_names[i] = player["team_name"]
                number_of_people += len(player["team"])
            else:
                self.team_names[i] = ""

        self.people = [VisPerson() for _ in xrange(number_of_people)]

        for i, player in enumerate(teams):
            self.Animations[i] = None

            # Skip bad teams
            if not (player and player.get("status", "Failure") != "Failure"):
                continue

            # teamImage = self.personImage.copy()
            # for animation_type in ANIMATION_TYPES: dont exist yet; modify constants to make these
            for person in player["team"].values():
                visPlayer = self.people[person["person_id"]]
                room = self.rooms[person["location"]]

                visPlayer.stand_in_room(room)
                visPlayer.pos = visPlayer.targetPos
                visPlayer.set_data(
                    person["location"],
                    person["team"], person["name"], self)

            team_color = self.colors[-1]
            if visPlayer.team < len(self.colors):
                team_color = self.colors[visPlayer.team]

            self.Animations[i] = Animation(team_color, self)


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
        self.rotation = 0
        self.path = []
        self.pathLength = 0
        self.waypoints = []
        self.isDistracted = False
        self.sentNoAction = True
        self.isBlocked = False
        self.asleep = False
        self.toSleep = False
        self.toWake = False

    def set_rotation(self, rotation):

        self.rotation = rotation

    def stand_in_room(self, newRoom):
        # No-op case

        # Loop through all standing positions, find an unoccupied one and take it.
        # To find unoccupied, we first compile a list of positions NOT to take.
        # If no standing, we can take a sitting spot too.
        badpos = set()
        found = False
        for person in newRoom.people:
            if person.pos:
                if person.targetPos:
                    badpos.add(person.targetPos)
        for position in newRoom.stand:
            if position not in badpos:
                self.targetPos = position
                found = True
                break
        if not found:
            for position in newRoom.chairs:
                if position not in badpos:
                    self.targetPos = position
                    found = True
                    break
        if found:
            newRoom.people.add(self)
        return

    def sit_in_room(self, newRoom):

        # Loop through all sitting positions, find an unoccupied one and take it.
        # To find unoccupied, we first compile a list of positions NOT to take.
        badpos = dict()
        found = False
        for person in newRoom.people:
            if person.pos:
                if person.targetPos:
                    badpos[person.targetPos] = person
        for position in newRoom.chairs:
            if position not in badpos:
                self.targetPos = position
                found = True
                break
        if not found:
            for position in newRoom.chairs:
                if badpos[position] not in newRoom.sitting:
                    self.targetPos = position
                    found = True
                    newRoom.people.remove(badpos[position])
                    badpos[position].stand_in_room(newRoom)

        # Add person to room if they aren't there already
        if found:
            newRoom.people.add(self)
            newRoom.sitting.add(self)
        return

    def set_data(self, room, team, name, visualizer):
        """
        Fields to be used
        """
        self.room = room
        self.team = team
        self.name = name

if __name__ == "__main__":
    mapConstants = retrieveConstants("serverDefaults")
    mapPath = mapConstants['map']
    vis = Visualizer(map_reader(mapPath, tuple(mapConstants["mapParseStartPos"])))
    vis.run_from_file(("../serverlog.json"))
