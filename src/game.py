from objects.room import Room
from objects.team import Team
from objects.team_member import TeamMember
from map_functions import getRoomsFromMap as map_reader
from config.handle_constants import retrieveConstants
import action_handler

class Game(object):

    # Initialize the server (only called once)

    def __init__(self, file_url):

        # the map reader will return a list of rooms that have bee
        # linked together as defined in the design doc.
        self.rooms = map_reader(file_url)
        self.turn = 0
        #self.turn_limit = retrieveConstants("generalInfo")["TURNLIMIT"]
        self.turn_limit = 80
        self.action_buffer = []
        self.msg_buffer = {}
        self.teams = []

    ##  Adds a new team and returns success / failure message
    #   @param data The data sent by the player to set up state
    #   @param client_id The ID assigned to that player by the server
    #   @return A (bool, dict) tuple stating success or failure and listing errors or sending starting info to the player
    def add_new_team(self, data, client_id):
        response = {}
        try:
            newTeam = Team(data["team"], data["members"], Room())
        except KeyError:
            return (False, response)
        self.msg_buffer[client_id] = []
        return (True, response)

    ##  Actually execute queued actions
    #   @return True if the game is running, False if the game ended
    def execute_turn(self):
        action_handler.handleTurn(self, self.action_buffer)
        self.action_buffer = []
        self.turn += 1
        if self.turn >= self.turn_limit:
            return False
        return True

    ##  Get these actions ready to execute
    #   @param action_list A list of actions to be queued
    #   @param client_id The ID of the player sending those actions
    #   @return A list of errors for invalid actions
    def queue_turn(self, action_list, client_id):
        error_list = []
        for action in action_list:
            try:
                action_handler.bufferAction(self.action_buffer, action["action"],
                                            action, client_id)
            except KeyError:
                error_list.append({"error": "invalid action",
                                   "action": action["action"]})
        return error_list

    ##  Given client_id, returns the data to be sent back to the player.
    #   If the game is over, send end-of-game stuff
    #   @param client_id the identifier for the player to give info to
    #   @return A dictionary containing the info to be sent to the player
    def get_info(self, client_id):
        return {"warnings": [], "map": []}
