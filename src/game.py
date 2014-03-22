from objects.room import Room
from objects.team import Team
from objects.team_member import TeamMember
from map_functions import getRoomsFromMap as map_reader

class Game(object):

    def __init__(self, file_url):
        """
        This is called once to init the server
        the map reader will return a list of rooms that have been
        linked together as defined in the design doc.
        """
        self.rooms = map_reader(file_url)
        self.turn = 0
        
    def add_new_team(self):
        pass

    ##  Actually execute queued actions
    #   @return True if the game is running, False if the game ended
    def execute_turn(self):
        return True

    ##  Get these actions ready to execute
    #   @param action_list A list of actions to be queued
    #   @param player_id The ID of the player sending those actions
    #   @return A list of errors for invalid actions
    def queue_turn(self, action_list, player_id):
        error_list = []
        return error_list

    ##  Given player_id, returns the data to be sent back to the player.
    #   If the game is over, send end-of-game stuff
    #   @param player_id the identifier for the player to give info to
    #   @return A dictionary containing the info to be sent to the player
    def get_info(self, player_id):
        return {"warnings": [], "map": []}