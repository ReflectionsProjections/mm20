from objects.room import Room
from objects.team import Team
from objects.team_member import TeamMember
from map_functions import getRoomsFromMap as map_reader
import action_handler

class Game(object):

    # Initial values
    rooms = []
    turn = 0
    action_buffer = []
    msg_buffer = {}

    # Initialize the server (only called once)
    def __init__(self, file_url):
        
        # Get a list of rooms
        self.rooms = map_reader(file_url)
        
    def add_new_team(self):
        pass

    ##  Actually execute queued actions
    #   @return True if the game is running, False if the game ended
    def execute_turn(self):
        action_handler.handleTurn(self, action_list)
        action_list = []
        return False

    ##  Get these actions ready to execute
    #   @param action_list A list of actions to be queued
    #   @param player_id The ID of the player sending those actions
    #   @return A list of errors for invalid actions
    def queue_turn(self, action_list, player_id):
        error_list = []
        for action in action_list:
            try:
                action_handler.bufferAction(action_buffer, action["action"],
                                            action, playerID)
            except KeyError:
                error_list.append({"error": "invalid action",
                                   "action": action["action"]})
        return error_list

    ##  Given player_id, returns the data to be sent back to the player.
    #   If the game is over, send end-of-game stuff
    #   @param player_id the identifier for the player to give info to
    #   @return A dictionary containing the info to be sent to the player
    def get_info(self, player_id):
        return {"warnings": [], "map": []}