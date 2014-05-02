from objects.team import Team
import map_functions
import action_handler
import config.handle_constants

STARTING_ROOM = "72 0 255 255"  # For testing purposes only


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
    def __init__(self, map_file):
        self.rooms = map_functions.map_reader(map_file)
        self.turn = 0
        defaults = config.handle_constants.retrieveConstants('generalInfo')
        self.turn_limit = defaults["TICKSINHOUR"] * 24
        self.unoptimized_weight = defaults["UNOPTWEIGHT"]
        self.optimized_weight = defaults["OPTWEIGHT"]
        self.team_limit = defaults["TEAMSIZE"]
        self.action_buffer = []
        self.result_buffer = {}
        self.teams = {}
        self.people = []

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
                return (False, {"status": "Failure", "errors": ["Number of team members exceeds team size"]})
            newTeam = Team(data["team"], data["members"],
                           self.rooms[STARTING_ROOM], self.people, client_id)
        except KeyError:
            return (False, {"status": "Failure", "errors": ["KeyError"]})
        # TODO: Make all error objects uniform
        self.result_buffer[client_id] = []
        self.teams[client_id] = newTeam
        response = {"status": "Success", "team": newTeam.get_team_members()}

        return (True, response)

    ## Processes a turn, executing all client queued actions, incrementing
    #  the turn and running the turn tick behavior
    # @return
    #   True if the game is running, False if the game ended
    def execute_turn(self):
        if len(self.people) == 0:
            return False
        action_handler.handleTurn(self, self.action_buffer)
        self.action_buffer = []
        for person in self.people:
            person.update()
        self.turn += 1
        if self.turn >= self.turn_limit:
            return False
        return True

    ## Queues all of the actions one client is attempting to execute this turn
    # @param action_list
    #   A list of actions the client wishes to perform
    # @param client_id
    #   The ID of the client sending these actions
    # @return
    #   A list of errors for invalid actions
    def queue_turn(self, action_list, client_id):
        error_list = []
        if action_list == None:
            return [{"error": "no actions",
                                   "action": None}]
        for action in action_list:
            try:
                action_handler.bufferAction(
                    self.action_buffer, action["action"], action, client_id)
            except KeyError:
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
            return {"winner": win}
        response = {"aiStats": self.teams[client_id].ai.output_dict(),
                    "map": self.teams[client_id].get_visible_map(),
                    "messages": self.result_buffer[client_id]}
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
