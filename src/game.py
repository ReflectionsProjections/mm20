from objects.team import Team
import map_functions
import action_handler
import config.handle_constants
import random
import unittest
import sys

## Holds the gamestate and represents the game to the server
class Game(object):
    # Objects:
    # rooms: A list of all of the rooms
    # turn: Which turn it is
    # turn_limit: The maximum length the game will run
    # action_buffer: A list of actions to be performed at the next 'tick'
    # result_buffer: A dictionary, indexed by client, of
    #   lists of responses to actions
    # teams: A list of all of the teams
    # people: A list of all of the people

    ## Called by the server to have the game set itself up
    # @param map_file
    #   the file in which the map is located
    def __init__(self, map_file, ticks=0, rooms=None):
        if rooms:
            self.rooms = rooms
        else:
            self.rooms = map_functions.map_reader(map_file, tuple(config.handle_constants.retrieveConstants("serverDefaults")["mapParseStartPos"]))
        self.turn = 0
        defaults = config.handle_constants.retrieveConstants('generalInfo')
        if ticks == 0:
            self.turn_limit = defaults["TICKSINHOUR"] * 24
        else:
            self.turn_limit = ticks * 24
        self.unoptimized_weight = defaults["UNOPTWEIGHT"]
        self.optimized_weight = defaults["OPTWEIGHT"]
        self.team_limit = defaults["TEAMSIZE"]
        self.spawnchance = defaults["SPAWNCHANCE"]
        self.action_buffer = []
        self.result_buffer = {}
        self.teams = {}
        self.people = []
        self.practice_games = False
        self.events = list()
        self.professorroom = ""
        self.professortime = 0
        self.professorhours = defaults["PROFESSORHOURS"]

    ##  Adds a new team and returns success / failure message
    # @param data
    #   The data sent by the player to set up state
    # @param client_id
    #   The ID assigned to that player by the server
    # @return
    #   A (bool, dict) tuple stating success or failure and listing
    #   errors or sending starting info to the player
    def add_new_team(self, data, client_id):
        response = {"status": "Success", "errors": []}
        try:
            if len(data["members"]) > self.team_limit:
                return (False, {"status": "Failure", "errors": [
                    "Number of team members exceeds team size"]})
            start_room = random.choice(self.rooms.values())
            try_limit = 1000
            while(try_limit > 0 and not start_room.canAdd(len(data["members"]))):
                start_room = self.rooms[random.choice(self.rooms.keys())]
                try_limit = try_limit-1
            newTeam = Team(data["team"], data["members"],
                           start_room, self.people, client_id, self.turn_limit / 24)
        except KeyError as e:
            return (False, {"status": "Failure", "errors": [{"KeyError": e.message}]})
            
        # TODO: Make all error objects uniform
        self.result_buffer[client_id] = []
        self.teams[client_id] = newTeam
        response = {
            "status": "Success", 
            "team": newTeam.get_team_members(),
            "team_id": newTeam.my_id,
            "team_name": newTeam.name,
            "map": self.teams[client_id].get_visible_map(),
            "turns_per_hour": self.turn_limit / 24
        }

        return (True, response)

    ## Processes a turn, executing all client queued actions, incrementing
    #  the turn and running the turn tick behavior
    # @return
    #   True if the game is running, False if the game ended
    def execute_turn(self):
        #print self.turn
        self.events = list()
        if len(self.people) == 0:
            return False
        for person in self.people:
            person.acted = None
        action_handler.handleTurn(self, self.action_buffer)
        self.action_buffer = []
        for person in self.people:
            person.update()
        if not self.practice_games and self.turn >= self.turn_limit / 2:
            self.practice_games = True
            for r in self.rooms.values():
                if r.isAvailable("PROJECTOR"):
                    r.addResource("PRACTICE")
            self.event_notification("PRACTICE", "The projectors are now showing practice games")
        # If professor, see if we can despawn
        if self.professorroom != "":
            self.professortime -= 1
            if self.professortime < 1:
                self.rooms[self.professorroom].removeResource("PROFESSOR")
                #self.rooms[self.professorroom].people.remove("Professor")
                self.event_notification("NOPROFESSOR", self.professorroom)
                self.professorroom = ""
        # Add new spawns
        if self.professorroom == "" and random.random() < self.spawnchance:
            while self.professorroom == "":
                possibleroom = random.choice(self.rooms.keys())
                room = self.rooms[possibleroom]
                if len(room.people) + 1 > len(room.chairs + room.stand):
                    continue
                #room.people.add("Professor")
                self.professorroom = possibleroom
            self.professortime = self.professorhours * self.turn_limit / 24
            self.rooms[self.professorroom].addResource("PROFESSOR")
            self.event_notification("PROFESSOR", self.professorroom)
        self.turn += 1
        sys.stderr.write('\rTurn: \033[92m{}\033[0m/{}'.format(
            self.turn,
            self.turn_limit))
        if self.turn >= self.turn_limit:
            return False
        return True

    ## Notify all teams of an event that just occurred
    def event_notification(self, code, message):
        self.events.append({"name":code, "message":message})

    ## called by server to receive events for that turn
    def get_events(self):
        newevents = self.events
        #self.events = list()
        return newevents

    ## Queues all of the actions one client is attempting to execute this turn
    # @param action_list
    #   A list of actions the client wishes to perform
    # @param client_id
    #   The ID of the client sending these actions
    # @return
    #   A list of errors for invalid actions
    def queue_turn(self, action_list, client_id):
        error_list = []
        if action_list is None:
            return [{"error": "no actions",
                     "action": None}]
        for action in action_list:
            try:
                action_handler.bufferAction(
                    self.action_buffer, action["action"], action, client_id)
            except KeyError:
                if "action" not in action:
                    error_list.append({"error": "invalid action: No action field!",
                                   "action": "None"})
                else:
                    error_list.append({"error": "invalid action",
                                   "action": action["action"]})
        return error_list

    ## Provides the information to be sent to a client each turn.
    #  If the game is over, send end-of-game stuff
    # @param client_id
    #   the client to which the information will be provided
    # @return
    #   A dictionary containing the info to be sent to the player
    def get_info(self, client_id):
        if self.turn >= self.turn_limit:
            winner = self.find_victor()
            win = False
            if winner == client_id:
                win = True
            return {"winner": win, "score": self.calc_score(client_id)}
        response = {"aiStats": self.teams[client_id].ai.output_dict(),
                    "score": self.calc_score(client_id),
                    "events": self.get_events(),
                    "map": self.teams[client_id].get_visible_map(),
                    "messages": self.result_buffer[client_id],
                    "people": self.teams[client_id].get_info_on_people(self.people)}
        self.result_buffer[client_id] = []
        return response

    ##  At endgame, find the winner
    # @return
    #   the id of the team that has won
    def find_victor(self):
        victor = 0
        score = -1
        for ident, team in self.teams.iteritems():
            team_score = self.calc_score(ident)
            if team_score > score:
                victor = ident
                score = team_score
        return victor

    ##  Calculate score for a team
    # @param client_id
    #   the id of the team to check
    # @return
    #   the score for that team
    def calc_score(self, client_id):
        ai = self.teams[client_id].ai
        return ((ai.implementation - ai.optimization) *
                self.unoptimized_weight + ai.optimization *
                self.optimized_weight) * ai.stability

class TestGame(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip("Not yet implemented")
    def testInit(self):
        self.assertTrue(False)

    @unittest.skip("Not yet implemented")
    def testAddTeam(self):
        self.assertTrue(False)

    @unittest.skip("Not yet implemented")
    def testQueueTurn(self):
        self.assertTrue(False)

    @unittest.skip("Not yet implemented")
    def testGetInfo(self):
        self.assertTrue(False)

    @unittest.skip("Not yet implemented")
    def testExecuteTurn(self):
        self.assertTrue(False)

    @unittest.skip("Not yet implemented")
    def testProfessorSpawn(self):
        self.assertTrue(False)

    @unittest.skip("Not yet implemented")
    def testProfessorDespawn(self):
        self.assertTrue(False)

    @unittest.skip("Not yet implemented")
    def testPractice(self):
        self.assertTrue(False)

    @unittest.skip("Not yet implemented")
    def testFindvictor(self):
        self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()
